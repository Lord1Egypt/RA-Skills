#!/usr/bin/env python3
"""
GoToEmail — read_email.py
读取单封邮件的完整内容。

输入（JSON via stdin）：
{
  "email":        "user@163.com",
  "password":     "授权码",
  "imap_host":    "imap.163.com",
  "imap_port":    993,        // 可选，默认 993
  "uid":          "1234",     // 必填，邮件 UID
  "folder":       "INBOX",    // 可选，默认 INBOX
  "mark_as_read": true        // 可选，默认 true
}

输出（JSON）：
{
  "ok": true,
  "uid": "1234",
  "subject": "会议通知",
  "from": "boss@corp.com",
  "to": "me@163.com",
  "cc": "",
  "date": "Mon, 20 May 2026 09:00:00 +0800",
  "body": "纯文本正文...",
  "html": "<p>HTML正文（截断至5000字）...</p>",
  "attachments": [{"filename":"附件.pdf","mime_type":"application/pdf"}],
  "has_attachments": true
}
"""

import imaplib
import ssl
import json
import sys
import email as emaillib
from email.header import decode_header as _decode_header


def decode_str(raw) -> str:
    if not raw:
        return ""
    parts = _decode_header(str(raw))
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(str(part))
    return "".join(result)


def extract_body(msg) -> tuple:
    """返回 (plain_text, html_text)。"""
    plain, html = "", ""

    if msg.is_multipart():
        for part in msg.walk():
            ct  = part.get_content_type()
            cd  = str(part.get("Content-Disposition", ""))
            if "attachment" in cd:
                continue
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            decoded = payload.decode(charset, errors="replace")
            if ct == "text/plain" and not plain:
                plain = decoded
            elif ct == "text/html" and not html:
                html = decoded
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True) or b""
        decoded = payload.decode(charset, errors="replace")
        if msg.get_content_type() == "text/html":
            html = decoded
        else:
            plain = decoded

    return plain, html


def extract_attachments(msg) -> list:
    items = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            items.append({
                "filename":  decode_str(part.get_filename() or ""),
                "mime_type": part.get_content_type(),
            })
    return items


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    email_addr   = data.get("email", "").strip()
    password     = data.get("password", "")
    imap_host    = data.get("imap_host", "").strip()
    imap_port    = int(data.get("imap_port", 993))
    uid          = str(data.get("uid", "")).strip()
    folder       = data.get("folder", "INBOX")
    mark_as_read = bool(data.get("mark_as_read", True))

    if not all([email_addr, password, imap_host, uid]):
        print(json.dumps({"ok": False, "error": "缺少必要字段：email / password / imap_host / uid"}, ensure_ascii=False))
        sys.exit(1)

    try:
        ctx  = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(imap_host, imap_port, ssl_context=ctx)
        conn.login(email_addr, password)
        conn.select(folder, readonly=not mark_as_read)

        if mark_as_read:
            conn.store(uid, "+FLAGS", "\\Seen")

        st, msg_data = conn.fetch(uid, "(RFC822)")
        if st != "OK" or not msg_data or msg_data[0] is None:
            raise ValueError(f"邮件 UID {uid} 不存在或无法获取")

        msg         = emaillib.message_from_bytes(msg_data[0][1])
        plain, html = extract_body(msg)
        attachments = extract_attachments(msg)

        conn.logout()

        print(json.dumps({
            "ok":              True,
            "uid":             uid,
            "subject":         decode_str(msg.get("Subject", "(无主题)")),
            "from":            decode_str(msg.get("From", "")),
            "to":              decode_str(msg.get("To", "")),
            "cc":              decode_str(msg.get("Cc", "")),
            "date":            str(msg.get("Date", "")),
            "body":            plain.strip(),
            "html":            html[:5000],          # 截断 HTML 避免过大
            "attachments":     attachments,
            "has_attachments": len(attachments) > 0,
        }, ensure_ascii=False))

    except imaplib.IMAP4.error as e:
        print(json.dumps({"ok": False, "error": f"IMAP认证失败: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
