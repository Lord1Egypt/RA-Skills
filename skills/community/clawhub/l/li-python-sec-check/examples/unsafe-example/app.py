#!/usr/bin/env python3
"""
⚠️ 警告：此文件包含故意编写的不安全代码，仅用于测试！
"""

import os
from flask import Flask, request

app = Flask(__name__)

# ❌ 硬编码密码
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

# ❌ 使用 DES 加密
from Crypto.Cipher import DES
def encrypt(data):
    cipher = DES.new(b'8bytekey', DES.MODE_ECB)
    return cipher.encrypt(data)

# ❌ SQL 注入
def get_user(user_id):
    query = "SELECT * FROM users WHERE id=%s" % user_id
    return query

# ❌ 命令注入
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    os.system("ping -c 1 " + host)

# ❌ eval 注入
@app.route('/calc')
def calc():
    expr = request.args.get('expr', '1+1')
    return str(eval(expr))

if __name__ == '__main__':
    # ❌ 调试模式开启
    app.run(debug=True, host='0.0.0.0')
