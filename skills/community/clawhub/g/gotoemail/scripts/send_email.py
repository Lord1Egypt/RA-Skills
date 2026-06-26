#!/usr/bin/env python3
"""
GoToEmail — send_email.py
通过 SMTP SSL 发送邮件。

输入（JSON via stdin）：
{
  "email":      "sender@163.com",
  "password":   "授权码",
  "smtp_host":  "smtp.163.com",
  "smtp_port":  465,                          // 可选，默认 465
  "to":         "recipient@example.com",      // 字符串或列表
  "subject":    "邮件主题",
  "body":       "纯文本正文",
  "html_body":  "<p>HTML正文</p>",            // 可选
  "cc":         ["cc1@example.com"],          // 可选，字符串或列表
  "bcc":        []                            // 可选，字符串或列表
}

输出（JSON）：
成功: {"ok": true, "message": "邮件已成功发送至 recipient@example.com"}
失败: {"ok": false, "error": "SMTP认证失败: ..."}
"""

import smtplib
import ssl
import json
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def to_list(val) -> list:
    """将字符串或列表统一转为列表，过滤空值。"""
    if not val:
        return []
    if isinstance(val, str):
        return [v.strip() for v in val.split(",") if v.strip()]
    return [str(v).strip() for v in val if str(v).strip()]


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    email_addr = data.get("email", "").strip()
    password   = data.get("password", "")
    smtp_host  = data.get("smtp_host", "").strip()
    smtp_port  = int(data.get("smtp_port", 465))

    to_list_   = to_list(data.get("to", []))
    cc_list    = to_list(data.get("cc", []))
    bcc_list   = to_list(data.get("bcc", []))
    subject    = data.get("subject", "（无主题）")
    body       = data.get("body", "")
    html_body  = data.get("html_body", "")

    if not all([email_addr, password, smtp_host]):
        print(json.dumps({"ok": False, "error": "缺少必要字段：email / password / smtp_host"}, ensure_ascii=False))
        sys.exit(1)

    if not to_list_:
        print(json.dumps({"ok": False, "error": "缺少收件人 (to)"}, ensure_ascii=False))
        sys.exit(1)

    # 构建邮件
    if html_body:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(body or "", "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))
    else:
        msg = MIMEText(body, "plain", "utf-8")

    msg["From"]    = email_addr
    msg["To"]      = ", ".join(to_list_)
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    all_recipients = to_list_ + cc_list + bcc_list

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx) as s:
            s.login(email_addr, password)
            s.sendmail(email_addr, all_recipients, msg.as_string())

        print(json.dumps({
            "ok":      True,
            "message": f"邮件已成功发送至 {', '.join(to_list_)}",
        }, ensure_ascii=False))

    except smtplib.SMTPAuthenticationError as e:
        print(json.dumps({"ok": False, "error": f"SMTP认证失败: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except smtplib.SMTPRecipientsRefused as e:
        print(json.dumps({"ok": False, "error": f"收件人被拒绝: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
