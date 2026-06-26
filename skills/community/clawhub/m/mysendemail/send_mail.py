# /root/.openclaw/workspace/skills/send_email/send_mail.py
import smtplib
import sys
from email.mime.text import MIMEText

def send_email(receiver, subject, content):
    # 配置（根据你的企业邮箱修改）
    smtp_server = "smtp.cloudtrend.com.cn"
    smtp_port = 587
    sender = "ai_assistant@cloudtrend.com.cn"
    password = "A5b3C3D6!"

    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return "✅ 邮件发送成功！收件人：{}，主题：{}".format(receiver, subject)
    except Exception as e:
        return "❌ 邮件发送失败：{}".format(str(e))

# 支持命令行传参（方便OpenClaw调用）
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法：python3 send_mail.py <收件人邮箱> <邮件主题> <邮件内容>")
        sys.exit(1)
    receiver = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]
    print(send_email(receiver, subject, content))
