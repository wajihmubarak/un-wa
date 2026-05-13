from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__, template_folder='../templates')
CORS(app)

HIDDEN_TEMPLATE = "Please allow me to access my old account. My account dates back to 2015, and this is my account number +{}"
SUPPORT_EMAILS = ["support@whatsapp.com", "android@support.whatsapp.com", "iphone@support.whatsapp.com", "smb@support.whatsapp.com", "accessibility@support.whatsapp.com"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify_account', methods=['POST'])
def verify_account():
    try:
        data = request.json
        email, password = data.get('e'), data.get('p')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
        return jsonify({"status": "success"})
    except Exception:
        return jsonify({"status": "error"}), 401

@app.route('/api/send_request', methods=['POST'])
def send_request():
    try:
        data = request.json
        all_accounts, phone = data.get('all_accounts'), data.get('phone')
        selected_acc = all_accounts[0] # نظام التدوير يمكن تطويره هنا
        
        msg = EmailMessage()
        msg['Subject'] = "Question about WhatsApp"
        msg['From'] = selected_acc['e']
        msg['To'] = ", ".join(SUPPORT_EMAILS)
        msg.set_content(HIDDEN_TEMPLATE.format(phone))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(selected_acc['e'], selected_acc['p'])
            smtp.send_message(msg)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# مهم جداً لـ Vercel
app = app
