#!/usr/bin/env python3
"""SMTP 发信助手：支持 TLS/SSL、多附件、HTML 正文。凭据走参数/环境变量，绝不落盘。"""
import argparse, os, smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formataddr
from email import encoders


def send(to, subject, body, smtp_host, port, user, pwd,
         attach=None, html=False, sender_name=None, cc=None):
    msg = MIMEMultipart()
    msg["From"] = formataddr((sender_name or user, user))
    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    msg["Subject"] = Header(subject, "utf-8")
    subtype = "html" if html else "plain"
    msg.attach(MIMEText(body, subtype, "utf-8"))

    for path in (attach or []):
        if not os.path.exists(path):
            print(f"⚠️ 附件不存在，跳过：{path}", file=sys.stderr)
            continue
        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        fname = os.path.basename(path)
        # 中文文件名编码
        part.add_header("Content-Disposition", "attachment",
                        filename=("utf-8", "", fname))
        msg.attach(part)

    use_ssl = (port == 465)
    try:
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_host, port, timeout=30) as s:
                s.login(user, pwd)
                s.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, port, timeout=30) as s:
                s.starttls()
                s.login(user, pwd)
                s.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError(f"SMTP 认证失败（检查授权码/应用专用密码）：{e}")
    except Exception as e:
        raise RuntimeError(f"发送失败：{type(e).__name__}: {e}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body", default="")
    ap.add_argument("--body-file", help="从文件读取正文（优先于 --body）")
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--attach", action="append", default=[])
    ap.add_argument("--cc", default=None)
    ap.add_argument("--smtp-host", default=os.environ.get("MAIL_HOST", "smtp.qq.com"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("MAIL_PORT", 465)))
    ap.add_argument("--user", default=os.environ.get("MAIL_USER"))
    ap.add_argument("--pass", dest="pwd", default=os.environ.get("MAIL_PASS"))
    ap.add_argument("--sender-name", default=None)
    args = ap.parse_args()

    if not args.user or not args.pwd:
        print("❌ 缺少 --user/--pass（或用环境变量 MAIL_USER/MAIL_PASS）", file=sys.stderr)
        sys.exit(2)
    body = args.body
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    try:
        send(args.to, args.subject, body, args.smtp_host, args.port,
             args.user, args.pwd, args.attach, args.html,
             args.sender_name, args.cc)
        print(f"✅ 已发送至 {args.to}（主题：{args.subject}）")
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
