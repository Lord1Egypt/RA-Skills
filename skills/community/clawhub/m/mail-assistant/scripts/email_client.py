#!/usr/bin/env python3
"""
SMTP/IMAP email client for 163 and QQ mailbox accounts.

Usage:
    python email_client.py <account-id> list-inbox [--limit N] [--unread]
    python email_client.py <account-id> read-mail <uid>
    python email_client.py <account-id> send <json-file> [--yes]
    python email_client.py <account-id> mark-read <uid> [--yes]
"""

import email
import email.policy
import imaplib
import json
import sys

# Force UTF-8 for console output (handle Unicode in email subjects/bodies)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
import smtplib
import sys
import time
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate

from data_dir import ACCOUNTS_DIR, confirm_action, secure_get

SMTP_CONFIGS = {
    "163": {"host": "smtp.163.com", "port": 465},
    "qq": {"host": "smtp.qq.com", "port": 465},
}
IMAP_CONFIGS = {
    "163": {"host": "imap.163.com", "port": 993},
    "qq": {"host": "imap.qq.com", "port": 993},
}


# ── Helpers ────────────────────────────────────────────────────────────────


def _load_account(account_id):
    path = os.path.join(ACCOUNTS_DIR, f"{account_id}.json")
    if not os.path.exists(path):
        print(f"[ERROR] Account not found: {account_id}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_secure(account, protocol):
    """
    Get auth credential for an SMTP or IMAP protocol.
    Tries system keyring first, falls back to JSON config.
    """
    acct_id = account.get("id", "")
    key = f"{acct_id}:{protocol}"
    val = data_dir.secure_get(key)
    if val is not None:
        return val
    return account.get(protocol, {}).get("auth", "")


def _decode_mime_header(value):
    if not value:
        return ""
    decoded_parts = decode_header(value)
    parts = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            try:
                parts.append(part.decode(charset or "utf-8", errors="replace"))
            except LookupError:
                parts.append(part.decode("utf-8", errors="replace"))
        else:
            parts.append(part)
    return " ".join(parts)


def _parse_email_body(msg):
    """Extract text/plain and text/html body from email message."""
    body_text = ""
    body_html = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain" and not body_text:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        body_text = payload.decode(charset, errors="replace")
                    except LookupError:
                        body_text = payload.decode("utf-8", errors="replace")
            elif ctype == "text/html" and not body_html:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        body_html = payload.decode(charset, errors="replace")
                    except LookupError:
                        body_html = payload.decode("utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            try:
                body_text = payload.decode(charset, errors="replace")
            except LookupError:
                body_text = payload.decode("utf-8", errors="replace")
    return body_text, body_html


def _fetch_emails(imap, limit=20, unread_only=False):
    """Fetch recent emails from INBOX, return list of parsed dicts."""
    status_code, select_data = imap.select("INBOX")
    if status_code != "OK":
        reason = ""
        if select_data:
            raw = select_data[0]
            if isinstance(raw, bytes):
                reason = raw.decode("utf-8", errors="replace")
            else:
                reason = str(raw)
        if "unsafe" in reason.lower():
            print(f"[ERROR] 邮箱 IMAP 安全检测拒绝访问: {reason}", file=sys.stderr)
            print("[HINT] 请检查：", file=sys.stderr)
            print("  1. 在网页邮箱设置中确认 IMAP 服务已开启", file=sys.stderr)
            print("  2. 重新生成一个授权码（旧的可能过期）", file=sys.stderr)
            print("  3. 部分 163 邮箱需开启「客户端授权密码」", file=sys.stderr)
        else:
            print(f"[ERROR] 无法选择收件箱: {reason}", file=sys.stderr)
        sys.exit(1)

    if unread_only:
        search_criterion = "UNSEEN"
    else:
        search_criterion = "ALL"

    status, message_ids = imap.search(None, search_criterion)
    if status != "OK":
        return []

    ids = message_ids[0].split()
    if not ids:
        return []

    # Fetch most recent N
    recent_ids = ids[-limit:]

    results = []
    for uid in recent_ids:
        status, msg_data = imap.fetch(uid, "(RFC822)")
        if status != "OK":
            continue

        if msg_data[0] is None:
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email, policy=email.policy.default)

        subject = _decode_mime_header(msg.get("Subject", ""))
        from_raw = _decode_mime_header(msg.get("From", ""))
        date_raw = msg.get("Date", "")
        body_text, body_html = _parse_email_body(msg)
        has_attachments = False
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is not None:
                    filename = part.get_filename()
                    if filename:
                        has_attachments = True
                        attachments.append({
                            "filename": _decode_mime_header(filename),
                            "content_type": part.get_content_type(),
                        })

        results.append({
            "uid": uid.decode() if isinstance(uid, bytes) else str(uid),
            "subject": subject,
            "from": from_raw,
            "date": date_raw,
            "body_text": body_text[:5000] if body_text else "",
            "body_html_preview": body_html[:500] if body_html else "",
            "has_attachments": has_attachments,
            "attachments": attachments,
        })

    return results


# ── Commands ───────────────────────────────────────────────────────────────


def cmd_list_inbox(account, args):
    limit = 20
    unread_only = False
    i = 2
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i] == "--unread":
            unread_only = True
            i += 1
        else:
            i += 1

    acct_type = account["type"]
    if acct_type not in IMAP_CONFIGS:
        print(f"[ERROR] Unsupported IMAP type: {acct_type}", file=sys.stderr)
        sys.exit(1)

    imap_cfg = IMAP_CONFIGS[acct_type]
    imap_user = account["user"]
    imap_pass = _get_secure(account, "imap")

    try:
        imap = imaplib.IMAP4_SSL(imap_cfg["host"], imap_cfg["port"])
        imap.login(imap_user, imap_pass)
        mails = _fetch_emails(imap, limit=limit, unread_only=unread_only)
        imap.logout()
    except imaplib.IMAP4.error as e:
        print(f"[ERROR] 邮箱登录/操作失败: {e}", file=sys.stderr)
        print("[HINT] 请检查授权码是否正确、是否已过期，或 IMAP 服务是否开启。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] IMAP operation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(mails, indent=2, ensure_ascii=False))


def cmd_read_mail(account, args):
    if len(args) < 3:
        print("[ERROR] Usage: email_client.py <account-id> read-mail <uid>", file=sys.stderr)
        sys.exit(1)
    target_uid = args[2]

    acct_type = account["type"]
    if acct_type not in IMAP_CONFIGS:
        print(f"[ERROR] Unsupported IMAP type: {acct_type}", file=sys.stderr)
        sys.exit(1)

    imap_cfg = IMAP_CONFIGS[acct_type]
    imap_user = account["user"]
    imap_pass = _get_secure(account, "imap")

    try:
        imap = imaplib.IMAP4_SSL(imap_cfg["host"], imap_cfg["port"])
        imap.login(imap_user, imap_pass)
        status_code, select_data = imap.select("INBOX")
        if status_code != "OK":
            reason = (select_data[0].decode("utf-8", errors="replace") if select_data and isinstance(select_data[0], bytes) else str(select_data))
            print(f"[ERROR] IMAP select INBOX 失败: {reason}", file=sys.stderr)
            sys.exit(1)
        fetch_uid = target_uid.encode() if isinstance(target_uid, str) else target_uid
        status, msg_data = imap.fetch(fetch_uid, "(RFC822)")
        imap.logout()
    except imaplib.IMAP4.error as e:
        print(f"[ERROR] 邮箱操作失败: {e}", file=sys.stderr)
        print("[HINT] 请检查授权码是否正确，或 IMAP 服务是否开启。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] IMAP operation failed: {e}", file=sys.stderr)
        sys.exit(1)

    if status != "OK" or not msg_data or not msg_data[0]:
        print("[ERROR] 未找到邮件。", file=sys.stderr)
        sys.exit(1)

    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email, policy=email.policy.default)
    subject = _decode_mime_header(msg.get("Subject", ""))
    from_raw = _decode_mime_header(msg.get("From", ""))
    to_raw = _decode_mime_header(msg.get("To", ""))
    date_raw = msg.get("Date", "")
    body_text, body_html = _parse_email_body(msg)
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            if part.get("Content-Disposition") is not None:
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        "filename": _decode_mime_header(filename),
                        "content_type": part.get_content_type(),
                    })

    result = {
        "uid": target_uid,
        "subject": subject,
        "from": from_raw,
        "to": to_raw,
        "date": date_raw,
        "body_text": body_text,
        "body_html_preview": body_html[:2000] if body_html else "",
        "attachments": attachments,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_send(account, args):
    if len(args) < 3:
        print("[ERROR] Usage: email_client.py <account-id> send <json-file> [--yes]", file=sys.stderr)
        sys.exit(1)

    json_path = args[2]
    if not os.path.exists(json_path):
        print(f"[ERROR] File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        email_data = json.load(f)

    # ⚠️ CONSENT: Require user confirmation before sending email
    acct_id = account.get("id", "?")
    to_list = email_data.get("to", [])
    subject = email_data.get("subject", "")
    desc = f"从账户 {acct_id} 发送邮件至 {', '.join(to_list)}，主题: {subject}"
    if not confirm_action(desc, args):
        print("[CANCELLED] 用户取消操作。")
        sys.exit(1)

    acct_type = account["type"]
    if acct_type not in SMTP_CONFIGS:
        print(f"[ERROR] Unsupported SMTP type: {acct_type}", file=sys.stderr)
        sys.exit(1)

    smtp_cfg = SMTP_CONFIGS[acct_type]
    smtp_user = account["user"]
    smtp_pass = _get_secure(account, "smtp")

    # Build MIME message
    msg = MIMEMultipart("mixed")
    msg["From"] = smtp_user
    msg["To"] = ", ".join(email_data.get("to", []))
    msg["Subject"] = email_data.get("subject", "")
    msg["Date"] = formatdate(localtime=True)

    if email_data.get("cc"):
        msg["Cc"] = ", ".join(email_data["cc"])

    # Body part
    body_text = email_data.get("body_text", email_data.get("body_html", ""))
    body_html = email_data.get("body_html", "")

    if body_html:
        # Multipart alternative for HTML+text
        alt_part = MIMEMultipart("alternative")
        if body_text:
            alt_part.attach(MIMEText(body_text, "plain", "utf-8"))
        alt_part.attach(MIMEText(body_html, "html", "utf-8"))
        msg.attach(alt_part)
    else:
        msg.attach(MIMEText(body_text, "plain", "utf-8"))

    # Attachments
    for att_path in email_data.get("attachments", []):
        if not os.path.exists(att_path):
            print(f"[WARN] Attachment not found, skipping: {att_path}", file=sys.stderr)
            continue
        with open(att_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        import base64
        from email import encoders
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(att_path),
        )
        msg.attach(part)

    # Build recipient list (To + Cc + Bcc)
    all_recipients = list(email_data.get("to", []))
    all_recipients.extend(email_data.get("cc", []))
    all_recipients.extend(email_data.get("bcc", []))

    try:
        smtp = smtplib.SMTP_SSL(smtp_cfg["host"], smtp_cfg["port"])
        smtp.login(smtp_user, smtp_pass)
        smtp.sendmail(smtp_user, all_recipients, msg.as_string())
        smtp.quit()
        print("[OK] Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] SMTP 登录失败：授权码错误或已过期。", file=sys.stderr)
        print("[HINT] 请检查邮箱授权码，在网页邮箱中重新生成。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] SMTP send failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_mark_read(account, args):
    if len(args) < 3:
        print("[ERROR] Usage: email_client.py <account-id> mark-read <uid> [--yes]", file=sys.stderr)
        sys.exit(1)
    target_uid = args[2]

    # ⚠️ CONSENT: Require user confirmation before modifying mailbox state
    acct_id = account.get("id", "?")
    desc = f"将账户 {acct_id} 中的邮件 {target_uid} 标记为已读"
    if not confirm_action(desc, args):
        print("[CANCELLED] 用户取消操作。")
        return

    acct_type = account["type"]
    if acct_type not in IMAP_CONFIGS:
        print(f"[ERROR] Unsupported IMAP type: {acct_type}", file=sys.stderr)
        sys.exit(1)

    imap_cfg = IMAP_CONFIGS[acct_type]
    imap_user = account["user"]
    imap_pass = _get_secure(account, "imap")

    try:
        imap = imaplib.IMAP4_SSL(imap_cfg["host"], imap_cfg["port"])
        imap.login(imap_user, imap_pass)
        status_code, select_data = imap.select("INBOX")
        if status_code != "OK":
            reason = (select_data[0].decode("utf-8", errors="replace") if select_data and isinstance(select_data[0], bytes) else str(select_data))
            print(f"[ERROR] IMAP select INBOX 失败: {reason}", file=sys.stderr)
            sys.exit(1)
        imap.store(target_uid.encode() if isinstance(target_uid, str) else target_uid, "+FLAGS", "\\Seen")
        imap.logout()
        print("[OK] Marked as read.")
    except imaplib.IMAP4.error as e:
        print(f"[ERROR] 邮箱操作失败: {e}", file=sys.stderr)
        print("[HINT] 请检查授权码。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] IMAP mark-read failed: {e}", file=sys.stderr)
        sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    account_id = sys.argv[1]
    action = sys.argv[2]
    args = sys.argv[3:]

    account = _load_account(account_id)

    actions = {
        "list-inbox": cmd_list_inbox,
        "read-mail": cmd_read_mail,
        "send": cmd_send,
        "mark-read": cmd_mark_read,
    }

    if action not in actions:
        print(f"[ERROR] Unknown action: {action}", file=sys.stderr)
        print(f"  Available: {', '.join(actions.keys())}", file=sys.stderr)
        sys.exit(1)

    actions[action](account, args)



# ── Module-level convenience functions (for import use) ────────────────────


def list_inbox(account_id, limit=20, unread_only=False):
    """List inbox emails. Returns parsed JSON."""
    account = _load_account(account_id)
    args = ["", ""]
    if limit != 20:
        args += ["--limit", str(limit)]
    if unread_only:
        args.append("--unread")
    cmd_list_inbox(account, args)


def read_mail(account_id, uid):
    """Read a single email by UID."""
    account = _load_account(account_id)
    cmd_read_mail(account, ["", "", uid])


def mark_read(account_id, uid):
    """Mark an email as read."""
    account = _load_account(account_id)
    cmd_mark_read(account, ["", "", uid])


if __name__ == "__main__":
    main()
