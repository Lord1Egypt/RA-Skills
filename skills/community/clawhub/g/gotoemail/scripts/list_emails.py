#!/usr/bin/env python3
"""
GoToEmail — list_emails.py
获取收件箱邮件列表（最新优先）。

输入（JSON via stdin）：
{
  "email":       "user@163.com",
  "password":    "授权码",
  "imap_host":   "imap.163.com",
  "imap_port":   993,           // 可选，默认 993
  "folder":      "INBOX",       // 可选，默认 INBOX
  "limit":       20,            // 可选，默认 20，最大 100
  "unread_only": false          // 可选，默认 false
}

输出（JSON）：
{
  "ok": true,
  "folder": "INBOX",
  "total": 142,
  "returned": 20,
  "emails": [
    {"uid":"567","subject":"会议通知","from":"boss@corp.com","date":"Mon, 20 May 2026 09:00:00 +0800","unread":true}
  ]
}
"""

import imaplib
import ssl
import json
import sys
import email as emaillib
from email.header import decode_header as _decode_header


def decode_str(raw) -> str:
    """将 RFC2047 编码的邮件头解码为 Unicode 字符串。"""
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


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    email_addr = data.get("email", "").strip()
    password   = data.get("password", "")
    imap_host  = data.get("imap_host", "").strip()
    imap_port  = int(data.get("imap_port", 993))
    folder     = data.get("folder", "INBOX")
    limit      = min(int(data.get("limit", 20)), 100)
    unread_only = bool(data.get("unread_only", False))

    if not all([email_addr, password, imap_host]):
        print(json.dumps({"ok": False, "error": "缺少必要字段：email / password / imap_host"}, ensure_ascii=False))
        sys.exit(1)

    try:
        ctx  = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(imap_host, imap_port, ssl_context=ctx)
        conn.login(email_addr, password)
        conn.select(folder, readonly=True)

        criteria = "UNSEEN" if unread_only else "ALL"
        status, data_raw = conn.search(None, criteria)
        if status != "OK":
            raise RuntimeError(f"搜索失败: {status}")

        all_uids = data_raw[0].split()
        total    = len(all_uids)

        # 取最后 N 封（最新的），倒序排列
        recent_uids = all_uids[-limit:][::-1]

        emails = []
        for uid in recent_uids:
            st, msg_data = conn.fetch(uid, "(FLAGS BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if st != "OK" or not msg_data or msg_data[0] is None:
                continue

            raw_header = msg_data[0][1]
            msg        = emaillib.message_from_bytes(raw_header)
            flags_raw  = msg_data[0][0].decode(errors="replace")

            emails.append({
                "uid":     uid.decode(),
                "subject": decode_str(msg.get("Subject", "(无主题)")),
                "from":    decode_str(msg.get("From", "")),
                "date":    str(msg.get("Date", "")),
                "unread":  "\\Seen" not in flags_raw,
            })

        conn.logout()

        print(json.dumps({
            "ok":       True,
            "folder":   folder,
            "total":    total,
            "returned": len(emails),
            "emails":   emails,
        }, ensure_ascii=False))

    except imaplib.IMAP4.error as e:
        print(json.dumps({"ok": False, "error": f"IMAP认证失败: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
