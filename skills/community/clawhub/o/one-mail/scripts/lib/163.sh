#!/bin/bash
# 网易邮箱适配器

require_command curl
require_command openssl

# IMAP 连接
imap_connect() {
    local server="$1"
    local port="${2:-993}"
    
    exec 3<>/dev/tcp/"$server"/"$port"
    openssl s_client -quiet -connect "$server:$port" <&3 >&3 2>/dev/null &
    IMAP_PID=$!
    sleep 1
}

# IMAP 命令
imap_command() {
    local tag="$1"
    local command="$2"
    
    echo "$tag $command" >&3
    
    # 读取响应
    local response=""
    while IFS= read -r line <&3; do
        response="$response$line\n"
        if [[ "$line" =~ ^$tag\ (OK|NO|BAD) ]]; then
            break
        fi
    done
    
    echo -e "$response"
}

# IMAP 登录
imap_login() {
    local email="$1"
    local password="$2"
    
    imap_command "A001" "LOGIN $email $password"
}

# 收取网易邮箱邮件
fetch_163() {
    local account="$1"
    local unread_only="$2"
    local query="$3"
    local limit="$4"
    
    local email=$(echo "$account" | jq -r '.email')
    local imap_server=$(echo "$account" | jq -r '.imap_server')
    local account_type=$(echo "$account" | jq -r '.type // "163"')
    local creds=$(get_credentials "$account_type" "$email")
    local password=$(echo "$creds" | jq -r '.password')
    
    # 使用 Python 脚本处理 IMAP（更可靠）
    python3 - <<PYTHON_EOF
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime
import sys

# 扩展 IMAP4_SSL 类以支持 ID 命令
class IMAP4_SSL_ID(imaplib.IMAP4_SSL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加 ID 命令支持
        imaplib.Commands['ID'] = ('AUTH',)
    
    def id_(self, *args):
        """发送 ID 命令"""
        name = 'ID'
        typ, dat = self._simple_command(name, *args)
        return self._untagged_response(typ, dat, name)

try:
    # 连接 IMAP（使用支持 ID 的类）
    mail = IMAP4_SSL_ID('$imap_server')
    
    # 先登录
    mail.login('$email', '$password')
    
    # 网易邮箱要求发送 ID 命令（登录后）
    try:
        # 发送 ID 命令标识客户端
        mail.id_('("name" "one-mail" "version" "1.0.1" "vendor" "OpenClaw" "support-email" "support@openclaw.ai")')
    except Exception as e:
        # 如果不支持 ID 命令，记录但继续
        print(f"Warning: ID command failed: {e}", file=sys.stderr)
    
    mail.select('INBOX')
    
    # 搜索邮件
    search_criteria = 'ALL'
    if '$unread_only' == 'true':
        search_criteria = 'UNSEEN'
    
    if '$query':
        search_criteria = f'({search_criteria} SUBJECT "$query")'
    
    status, messages = mail.search(None, search_criteria)
    email_ids = messages[0].split()
    
    # 限制数量
    email_ids = email_ids[-int('$limit'):][::-1]
    
    emails = []
    for email_id in email_ids:
        # 获取邮件内容和 FLAGS
        status, msg_data = mail.fetch(email_id, '(RFC822 FLAGS)')
        
        # 解析 FLAGS
        flags = []
        for response_part in msg_data:
            if isinstance(response_part, bytes):
                flags_str = response_part.decode()
                if 'FLAGS' in flags_str:
                    # 提取 FLAGS
                    import re
                    flags_match = re.search(r'FLAGS \(([^)]+)\)', flags_str)
                    if flags_match:
                        flags = flags_match.group(1).split()
        
        # 检查是否未读
        is_unread = r'\\Seen' not in flags
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # 解码主题
                subject = ''
                if msg['Subject']:
                    decoded = decode_header(msg['Subject'])[0]
                    if isinstance(decoded[0], bytes):
                        subject = decoded[0].decode(decoded[1] or 'utf-8')
                    else:
                        subject = decoded[0]
                
                # 获取发件人
                from_addr = msg.get('From', '')
                
                # 获取收件人
                to_addr = msg.get('To', '')
                
                # 获取日期
                date_str = msg.get('Date', '')
                
                # 获取正文预览
                snippet = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            try:
                                snippet = part.get_payload(decode=True).decode()[:200]
                            except:
                                pass
                            break
                else:
                    try:
                        snippet = msg.get_payload(decode=True).decode()[:200]
                    except:
                        pass
                
                # 检查是否有附件
                has_attachments = False
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_disposition() == 'attachment':
                            has_attachments = True
                            break
                
                emails.append({
                    'id': email_id.decode(),
                    'account': '163',
                    'from': from_addr,
                    'to': to_addr,
                    'subject': subject,
                    'date': date_str,
                    'unread': is_unread,
                    'has_attachments': has_attachments,
                    'snippet': snippet.strip()
                })
    
    mail.close()
    mail.logout()
    
    print(json.dumps(emails, ensure_ascii=False))

except Exception as e:
    print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)
PYTHON_EOF
}

# 发送网易邮箱邮件
send_163() {
    local account="$1"
    local to="$2"
    local cc="$3"
    local bcc="$4"
    local subject="$5"
    local body="$6"
    local attach="$7"
    local reply_to="$8"
    
    local email=$(echo "$account" | jq -r '.email')
    local smtp_server=$(echo "$account" | jq -r '.smtp_server')
    local account_type=$(echo "$account" | jq -r '.type // "163"')
    local creds=$(get_credentials "$account_type" "$email")
    local password=$(echo "$creds" | jq -r '.password')
    
    # 使用 Python 脚本发送邮件
    python3 - <<EOF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# 创建邮件
msg = MIMEMultipart()
msg['From'] = '$email'
msg['To'] = '$to'
msg['Subject'] = '$subject'

if '$cc':
    msg['Cc'] = '$cc'

if '$bcc':
    msg['Bcc'] = '$bcc'

# 添加正文
msg.attach(MIMEText('''$body''', 'plain', 'utf-8'))

# 添加附件
if '$attach':
    with open('$attach', 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename("$attach")}')
        msg.attach(part)

# 发送邮件
server = smtplib.SMTP_SSL('$smtp_server', 465)
server.login('$email', '$password')

recipients = ['$to']
if '$cc':
    recipients.append('$cc')
if '$bcc':
    recipients.append('$bcc')

server.sendmail('$email', recipients, msg.as_string())
server.quit()

print('邮件已发送')
EOF
}
