#!/usr/bin/env python3
"""
OpenClaw 团队协作服务器 - 入口文件
"""

import os
import json
import hashlib
import base64
import secrets
import socket
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
from cryptography.fernet import Fernet

# ====== 配置 ======
GATEWAY_URL = "http://127.0.0.1:18789"
GATEWAY_TOKEN = "9d2a452dbb739cbf940a5794181a280453dda9ed99367b6a"
PORT = 8888
DATA_DIR = os.path.expanduser("~/Desktop/alldata")
CREDENTIAL_FILE = "credential.enc"
INVITE_CODE = os.environ.get("INVITE_CODE", "OPENCLAW2026")  # 邀请码，可通过环境变量自定义
BRAND_NAME = os.environ.get("BRAND_NAME", "OPENCLAW-TEAM")  # 品牌名称，可通过环境变量自定义
# ==================

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()
print(f"📡 本地IP: {LOCAL_IP}")

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app, origins=[f"http://{LOCAL_IP}:{PORT}", f"http://127.0.0.1:{PORT}"], supports_credentials=True)

# 导入并注册上传路由
from upload import register_upload_routes
register_upload_routes(app, DATA_DIR, CREDENTIAL_FILE, LOCAL_IP, PORT)

# ====== 工具函数 =====
def encrypt_data(data: str, password: str) -> str:
    key = hashlib.sha256(password.encode()).digest()
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted: str, password: str) -> str:
    key = hashlib.sha256(password.encode()).digest()
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.decrypt(encrypted.encode()).decode()

def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def get_user_dir(username: str) -> str:
    safe_name = username.replace(" ", "_")
    return os.path.join(DATA_DIR, safe_name)

# ====== 路由 =====
@app.route('/')
def index():
    # 读取HTML文件
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取前端配置"""
    return jsonify({
        "brand_name": BRAND_NAME
    })

@app.route('/api/check_invite', methods=['POST'])
def check_invite():
    data = request.get_json()
    code = data.get('code', '')
    return jsonify({"valid": code == INVITE_CODE})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    invite_code = data.get('invite_code', '')
    
    if invite_code != INVITE_CODE:
        return jsonify({"success": False, "error": "邀请码错误"}), 400
    if len(username) > 15 or not username:
        return jsonify({"success": False, "error": "用户名需要1-15字符"}), 400
    if len(password) < 4:
        return jsonify({"success": False, "error": "密码至少4个字符"}), 400
    
    user_dir = get_user_dir(username)
    if os.path.exists(os.path.join(user_dir, CREDENTIAL_FILE)):
        return jsonify({"success": False, "error": "用户已存在"}), 400
    
    os.makedirs(user_dir, exist_ok=True)
    
    # 创建加密凭证
    encrypted = encrypt_data(f"OPENCLAW_USER:{username}", password)
    with open(os.path.join(user_dir, CREDENTIAL_FILE), 'w') as f:
        f.write(encrypted)
    
    # 保存配置
    config = {"username": username, "created": datetime.now().isoformat()}
    with open(os.path.join(user_dir, "config.json"), 'w') as f:
        json.dump(config, f, indent=2)
    
    # 创建用户文件
    for name, content in [("soul.enc", ""), ("memory.enc", ""), ("history.enc", encrypt_data("[]", password))]:
        with open(os.path.join(user_dir, name), 'w') as f:
            f.write(content)
    
    print(f"✅ 新用户注册: {username}")
    return jsonify({"success": True, "username": username})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    user_dir = get_user_dir(username)
    cred_file = os.path.join(user_dir, CREDENTIAL_FILE)
    
    if not os.path.exists(cred_file):
        return jsonify({"success": False, "error": "用户不存在"}), 401
    
    try:
        with open(cred_file, 'r') as f:
            encrypted = f.read()
        cipher = Fernet(generate_key(password))
        decrypted = cipher.decrypt(encrypted.encode())
        if decrypted.decode() == f"OPENCLAW_USER:{username}":
            print(f"✅ 用户登录: {username}")
            return jsonify({"success": True, "username": username})
    except:
        pass
    
    return jsonify({"success": False, "error": "密码错误"}), 401

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not user_message or not username:
        return jsonify({"error": "消息或用户名为空"}), 400
    
    # 验证用户
    user_dir = os.path.join(DATA_DIR, username)
    cred_file = os.path.join(user_dir, CREDENTIAL_FILE)
    
    if not os.path.exists(cred_file):
        return jsonify({"error": "用户不存在"}), 401
    
    try:
        with open(cred_file, 'r') as f:
            encrypted = f.read()
        cipher = Fernet(generate_key(password))
        decrypted = cipher.decrypt(encrypted.encode())
        if not decrypted.decode().startswith("OPENCLAW_USER:" + username):
            return jsonify({"error": "验证失败"}), 401
    except:
        return jsonify({"error": "验证失败"}), 401
    
    # 获取历史
    history = []
    history_file = os.path.join(user_dir, "history.enc")
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                decrypted = decrypt_data(f.read(), password)
            history = eval(decrypted)
        except:
            pass
    
    messages = [{"role": "user", "content": msg["content"]} for msg in history]
    messages.append({"role": "user", "content": user_message})
    
    # 调用 API
    try:
        response = requests.post(
            f"{GATEWAY_URL}/v1/chat/completions",
            headers={"Authorization": f"Bearer {GATEWAY_TOKEN}", "Content-Type": "application/json"},
            json={"model": "openclaw:main", "messages": messages, "stream": False},
            timeout=120
        )
        
        if response.status_code != 200:
            return jsonify({"error": f"API错误: {response.status_code}"}), 500
        
        result = response.json()
        assistant_message = result['choices'][0]['message']['content']
        
        # 保存历史
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})
        history = history[-40:]
        
        with open(history_file, 'w') as f:
            f.write(encrypt_data(str(history), password))
        
        return jsonify({"response": assistant_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"🚀 OpenClaw 团队协作平台启动!")
    print(f"   访问: http://0.0.0.0:{PORT}")
    print(f"   数据目录: {DATA_DIR}")
    print(f"   邀请码: {INVITE_CODE}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
