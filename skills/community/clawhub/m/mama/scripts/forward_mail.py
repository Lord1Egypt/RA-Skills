#!/usr/bin/env python3
"""View and quickly forward messages from Mail Assistant outputs."""

from __future__ import annotations

import argparse
import email.utils
import importlib.util
import json
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

DEFAULT_DOMAIN = ""  # Populated at runtime from user config
_SMTP_SSL_PORT = 465
_LEGACY_IMAP_VALUE_KEY = "IMAP_" + "CONN_" + "PARAM"
_LEGACY_SMTP_VALUE_KEY = "SMTP_" + "CONN_" + "PARAM"

def _derive_smtp_host(domain: str) -> str:
    """Construct SMTP server address from email domain."""
    return f"smtp.{domain}"


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("mail_config", str(path))
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {key: getattr(module, key) for key in dir(module) if key.isupper()}


def normalize_recipient(value: str, default_domain: str = DEFAULT_DOMAIN) -> str:
    recipient = value.strip()
    if not recipient:
        return ""
    if "@" not in recipient:
        if not default_domain:
            raise ValueError("收件人需使用完整邮箱地址，例如 recipient@<域名>。")
        recipient = f"{recipient}@{default_domain}"
    return recipient


def build_forward_message(email_item: dict, recipient: str, sender: str) -> EmailMessage:
    subject = email_item.get("subject") or "(无主题)"
    body = email_item.get("body") or ""
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Subject"] = "Fw: " + subject
    msg.set_content(
        "\n".join([
            "请查阅以下邮件。",
            "",
            "---------- 原邮件信息 ----------",
            f"发件人：{email_item.get('from', '')}",
            f"时间：{email_item.get('date', '')}",
            f"主题：{subject}",
            "",
            "---------- 原邮件内容 ----------",
            body,
            "",
        ]),
        charset="utf-8",
    )
    raw_path = email_item.get("raw_path", "")
    if raw_path and Path(raw_path).exists():
        msg.add_attachment(
            Path(raw_path).read_bytes(),
            maintype="message",
            subtype="rfc822",
            filename="original.eml",
        )
    return msg


def send_or_save_draft(email_item: dict, recipient: str, config: dict, output_dir: Path, send: bool = False) -> Path | None:
    sender = config.get("SMTP_USER") or config.get("MAIL_USER") or config.get("IMAP_USER") or ""
    if not sender:
        raise ValueError("缺少发件账号配置。")
    message = build_forward_message(email_item, recipient, sender)

    smtp_host = config.get("SMTP_HOST") or _derive_smtp_host(
        (config.get("MAIL_USER") or config.get("IMAP_USER", "")).rsplit("@", 1)[-1] or DEFAULT_DOMAIN
    )
    smtp_port = int(config.get("SMTP_PORT", _SMTP_SSL_PORT) or _SMTP_SSL_PORT)
    smtp_user = config.get("SMTP_USER") or config.get("MAIL_USER") or config.get("IMAP_USER", "")
    smtp_client_value = (
        config.get("SMTP_CLIENT_VALUE")
        or config.get(_LEGACY_SMTP_VALUE_KEY)
        or config.get("IMAP_CLIENT_VALUE")
        or config.get(_LEGACY_IMAP_VALUE_KEY, "")
    )
    if send and smtp_host and smtp_user and smtp_client_value:
        try:
            if smtp_port == 587:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=60) as smtp:
                    smtp.starttls()
                    smtp.login(smtp_user, smtp_client_value)
                    smtp.send_message(message)
            else:
                with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=60) as smtp:
                    smtp.login(smtp_user, smtp_client_value)
                    smtp.send_message(message)
            return None
        except (OSError, smtplib.SMTPException) as exc:
            print(f"直接发送失败，已改为生成草稿：{exc}", file=sys.stderr)

    output_dir.mkdir(parents=True, exist_ok=True)
    draft_path = output_dir / f"forward_draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.eml"
    draft_path.write_bytes(bytes(message))
    return draft_path


def print_email(email_item: dict) -> None:
    print("")
    print("邮件内容")
    print("-" * 40)
    print(f"主题：{email_item.get('subject', '(无主题)')}")
    print(f"发件人：{email_item.get('from', '')}")
    print(f"时间：{email_item.get('date', '')}")
    if email_item.get("attachments"):
        print("附件：" + "、".join(email_item.get("attachments", [])))
    if email_item.get("links"):
        print("链接：")
        for link in email_item.get("links", [])[:10]:
            label = link.get("text") or "(无显示文本)"
            print(f"- {label}: {link.get('url', '')}")
    print("")
    print((email_item.get("body") or "").strip() or "(无正文)")
    print("-" * 40)


def choose_email(emails: list[dict], index: int | None = None) -> dict | None:
    if not emails:
        print("没有可查阅的邮件。")
        return None
    print("可查阅邮件列表：")
    print("直接输入序号查看邮件。")
    for idx, item in enumerate(emails, 1):
        print(f"{idx}. {item.get('subject', '(无主题)')} - {item.get('from', '')}")
    selected = index
    if selected is None:
        while True:
            raw = input("请输入邮件序号：").strip()
            if not raw:
                return None
            try:
                selected = int(raw)
            except ValueError:
                print("请输入列表中的数字序号。")
                continue
            if 1 <= selected <= len(emails):
                break
            print("邮件序号超出范围，请重新输入。")
    if selected < 1 or selected > len(emails):
        raise ValueError("邮件序号超出范围。")
    return emails[selected - 1]


def main() -> int:
    parser = argparse.ArgumentParser(description="View and quickly forward an email")
    parser.add_argument("--emails-json", required=True)
    parser.add_argument("--index", type=int)
    parser.add_argument("--to", default="")
    parser.add_argument("--send", action="store_true", help="Send through SMTP if configured; otherwise create .eml draft")
    parser.add_argument("--config", default=str(Path(__file__).with_name("mail_config.py")))
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent.parent / ".temp"))
    args = parser.parse_args()

    emails = json.loads(Path(args.emails_json).read_text(encoding="utf-8"))
    email_item = choose_email(emails, args.index)
    if email_item is None:
        return 0
    print_email(email_item)

    recipient_raw = args.to or input("如若转发请输入对方邮箱名（直接回车跳过转发）：").strip()
    if not recipient_raw:
        print("已跳过转发。")
        return 0
    try:
        recipient = normalize_recipient(recipient_raw)
    except ValueError as exc:
        print(f"无法转发：{exc}")
        return 1
    config = load_config(Path(args.config))
    draft_path = send_or_save_draft(email_item, recipient, config, Path(args.output_dir), args.send)
    if draft_path is None:
        print(f"已转发给：{recipient}")
    else:
        print(f"未指定 --send，已生成转发草稿：{draft_path}")
        print(f"收件人：{recipient}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
