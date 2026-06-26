# -*- coding: utf-8 -*-
"""
Light Reading 邮件 Webhook 接收端点
接收企业微信邮箱转发的邮件，保存为 HTML 文件
"""

import http.server
import socketserver
import json
import os
import re
import email
import base64
import quopri
from datetime import datetime
from urllib.parse import parse_qs

PORT = 5087
SAVE_DIR = os.path.join(os.path.dirname(__file__), 'emails')

# 确保保存目录存在
os.makedirs(SAVE_DIR, exist_ok=True)

class EmailWebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # 记录原始数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 尝试解析为邮件
        email_html = None
        email_subject = 'unknown'
        
        try:
            # 尝试解析为 MIME 邮件
            msg = email.message_from_bytes(post_data)
            email_subject = msg.get('Subject', 'unknown')
            
            # 提取 HTML 内容
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/html':
                        try:
                            payload = part.get_payload(decode=True)
                            if payload:
                                email_html = payload.decode('utf-8', errors='ignore')
                                break
                        except:
                            pass
            else:
                content_type = msg.get_content_type()
                if content_type == 'text/html':
                    try:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            email_html = payload.decode('utf-8', errors='ignore')
                    except:
                        pass
                
                # 如果是 text/plain，尝试查找其中的 HTML 片段
                if not email_html:
                    try:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            text = payload.decode('utf-8', errors='ignore')
                            # 查找 HTML 片段
                            html_match = re.search(r'<html[^>]*>.*?</html>', text, re.DOTALL | re.IGNORECASE)
                            if html_match:
                                email_html = html_match.group(0)
                            else:
                                # 保存纯文本
                                email_html = f'<pre>{text}</pre>'
                    except:
                        pass
        except Exception as e:
            print(f"解析邮件失败：{e}")
            # 尝试直接保存为 HTML
            try:
                email_html = post_data.decode('utf-8', errors='ignore')
            except:
                email_html = f'<pre>{post_data}</pre>'
        
        # 清理文件名
        safe_subject = re.sub(r'[^\w\s-]', '', email_subject)[:50].strip()
        safe_subject = safe_subject.replace(' ', '_') if safe_subject else 'unknown'
        filename = f"{timestamp}_{safe_subject}.html"
        filepath = os.path.join(SAVE_DIR, filename)
        
        # 保存邮件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(email_html if email_html else str(post_data))
        
        print(f"✅ 收到邮件：{email_subject}")
        print(f"   保存到：{filepath}")
        
        # 返回成功响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'status': 'ok', 'filename': filename, 'subject': email_subject}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_GET(self):
        """健康检查端点"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {
            'status': 'running',
            'port': PORT,
            'save_dir': SAVE_DIR,
            'emails': os.listdir(SAVE_DIR) if os.path.exists(SAVE_DIR) else []
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        print(f"[Webhook] {args[0]}")

def run_server():
    with socketserver.TCPServer(("", PORT), EmailWebhookHandler) as httpd:
        print("[Webhook] Light Reading 邮件 Webhook 服务器已启动")
        print("[Webhook]   监听端口：http://localhost:{}".format(PORT))
        print("[Webhook]   保存目录：{}".format(SAVE_DIR))
        print("[Webhook]   按 Ctrl+C 停止服务")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
