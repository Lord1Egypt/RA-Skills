#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人邮箱邮件回复：优先网页邮箱定位；备选 SMTP（与 IMAP 同账号密码）。

配置：smtp_host、smtp_port（email / email_password 与 IMAP 共用）。
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr, make_msgid, parseaddr
from pathlib import Path
from typing import Any, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(_SCRIPT_DIR))

from imap_mail import (  # noqa: E402
    _decode_password,
    decode_mime_header,
    default_skill_dir,
    fetch_raw_by_preview_token,
    load_imap_config,
    load_preview_config,
    parse_for_preview,
)
from webmail_locate import build_webmail_locate  # noqa: E402

logger = logging.getLogger("mail_reply")

# 常见 IMAP → SMTP 默认（用户仍可在 config 覆盖 host/port）
_IMAP_SMTP_DEFAULTS: dict[str, tuple[str, int]] = {
    "imap.gmail.com": ("smtp.gmail.com", 465),
    "imap.googlemail.com": ("smtp.gmail.com", 465),
    "imap.qq.com": ("smtp.qq.com", 465),
    "imap.exmail.qq.com": ("smtp.exmail.qq.com", 465),
    "imap.163.com": ("smtp.163.com", 465),
    "imap.126.com": ("smtp.126.com", 465),
    "imap.yeah.net": ("smtp.yeah.net", 465),
    "imap-mail.outlook.com": ("smtp-mail.outlook.com", 587),
    "outlook.office365.com": ("smtp.office365.com", 587),
    "imap.aliyun.com": ("smtp.aliyun.com", 465),
    "imap.qiye.aliyun.com": ("smtp.qiye.aliyun.com", 465),
}


def infer_smtp_host(imap_host: str) -> str:
    h = (imap_host or "").strip().lower()
    if h in _IMAP_SMTP_DEFAULTS:
        return _IMAP_SMTP_DEFAULTS[h][0]
    if h.startswith("imap."):
        return "smtp." + h[5:]
    return ""


def infer_smtp_port(imap_host: str, explicit_port: int | None = None) -> int:
    if explicit_port:
        return int(explicit_port)
    h = (imap_host or "").strip().lower()
    if h in _IMAP_SMTP_DEFAULTS:
        return _IMAP_SMTP_DEFAULTS[h][1]
    return 465


def load_smtp_config() -> dict[str, Any]:
    imap = load_imap_config()
    cfg_path = default_skill_dir() / "config.json"
    cfg: dict[str, Any] = {}
    if cfg_path.is_file():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg = data
        except (json.JSONDecodeError, OSError):
            pass

    imap_host = str(imap.get("imap_host") or "").strip()
    host = str(cfg.get("smtp_host") or os.environ.get("SMTP_HOST") or "").strip()
    if not host:
        host = infer_smtp_host(imap_host)

    port_raw = cfg.get("smtp_port") or os.environ.get("SMTP_PORT")
    port = infer_smtp_port(imap_host, int(port_raw) if port_raw not in (None, "") else None)

    use_ssl = cfg.get("smtp_use_ssl")
    if use_ssl is None:
        use_ssl = os.environ.get("SMTP_USE_SSL", "").strip().lower() in ("1", "true", "yes")
        if os.environ.get("SMTP_USE_SSL", "").strip() == "":
            use_ssl = port == 465

    user = str(imap.get("email") or "").strip()
    password = _decode_password(str(imap.get("email_password") or ""))

    return {
        "smtp_host": host,
        "smtp_port": port,
        "smtp_use_ssl": bool(use_ssl),
        "email": user,
        "email_password": password,
        "imap_host": imap_host,
    }


def smtp_is_configured() -> bool:
    c = load_smtp_config()
    return bool(c.get("smtp_host") and c.get("email") and c.get("email_password"))


def build_reply_url(preview_token: str, base_url: str | None = None) -> str:
    base = (base_url or load_preview_config()["mail_preview_base_url"]).rstrip("/")
    return f"{base}/mail/reply/{preview_token}"


def reply_to_address(from_header: str, reply_to_header: str = "") -> str:
    if reply_to_header:
        _name, addr = parseaddr(decode_mime_header(reply_to_header))
        if addr:
            return addr
    _name, addr = parseaddr(decode_mime_header(from_header or ""))
    return addr or (from_header or "").strip()


def re_subject(subject: str) -> str:
    s = (subject or "").strip() or "(无主题)"
    if re.match(r"^re:\s", s, re.I):
        return s
    return f"Re: {s}"


def _normalize_msg_id(mid: str) -> str:
    m = (mid or "").strip()
    if not m:
        return ""
    if not (m.startswith("<") and m.endswith(">")):
        m = f"<{m.strip('<>')}>"
    return m


def build_references(original_msg: Any, message_id: str) -> str:
    refs: list[str] = []
    prior = str(original_msg.get("References") or "").strip()
    if prior:
        refs.extend(prior.split())
    mid = _normalize_msg_id(message_id or str(original_msg.get("Message-ID") or ""))
    if mid and mid not in refs:
        refs.append(mid)
    return " ".join(refs)


def quote_original_for_reply(parsed: dict[str, Any], meta: dict[str, Any]) -> str:
    from_line = parsed.get("from_addr") or meta.get("from_addr") or ""
    date_line = parsed.get("date") or meta.get("email_date_utc") or ""
    body = (parsed.get("text_body") or "").strip()
    if not body and parsed.get("html_body"):
        body = re.sub(r"<[^>]+>", " ", str(parsed.get("html_body")))
        body = re.sub(r"\s+", " ", body).strip()
    quoted = "\n".join(f"> {line}" if line.strip() else ">" for line in body.splitlines())
    header = f"On {date_line}, {from_line} wrote:"
    return f"\n\n{header}\n{quoted}\n" if quoted else f"\n\n{header}\n"


def prepare_reply_draft(
    preview_token: str,
    *,
    db_path: Path | None = None,
) -> dict[str, Any]:
    raw, meta = fetch_raw_by_preview_token(preview_token, db_path=db_path)
    parsed = parse_for_preview(raw, preview_token)
    import email
    from email import policy

    msg = email.message_from_bytes(raw, policy=policy.default)
    message_id = str(meta.get("message_id") or msg.get("Message-ID") or "")
    to_addr = reply_to_address(parsed.get("from_addr") or "", str(msg.get("Reply-To") or ""))
    subject = re_subject(parsed.get("subject") or meta.get("subject") or "")
    locate = build_webmail_locate(
        message_id=message_id,
        from_addr=str(parsed.get("from_addr") or meta.get("from_addr") or ""),
        subject=str(parsed.get("subject") or meta.get("subject") or ""),
        email_date_utc=str(meta.get("email_date_utc") or parsed.get("date") or ""),
    )
    smtp_ok = smtp_is_configured()
    methods: list[str] = []
    if locate.get("webmail_url"):
        methods.append("webmail")
    if smtp_ok:
        methods.append("smtp")

    return {
        "preview_token": preview_token,
        "message_id": message_id,
        "to": to_addr,
        "subject": subject,
        "from_email": load_imap_config().get("email") or "",
        "in_reply_to": _normalize_msg_id(message_id),
        "references": build_references(msg, message_id),
        "quote_suffix": quote_original_for_reply(parsed, meta),
        "webmail": locate,
        "smtp_configured": smtp_ok,
        "reply_methods": methods,
        "preferred_method": "webmail" if "webmail" in methods else ("smtp" if smtp_ok else "none"),
        "reply_url": build_reply_url(preview_token),
    }


def send_reply_smtp(
    *,
    to_addr: str,
    subject: str,
    body: str,
    in_reply_to: str = "",
    references: str = "",
    from_email: str | None = None,
    include_quote: bool = False,
    preview_token: str = "",
) -> dict[str, Any]:
    cfg = load_smtp_config()
    host = str(cfg.get("smtp_host") or "").strip()
    port = int(cfg.get("smtp_port") or 465)
    user = str(from_email or cfg.get("email") or "").strip()
    password = str(cfg.get("email_password") or "")
    if not host or not user or not password:
        return {"ok": False, "error": "smtp_not_configured", "hint": "请配置 smtp_host、smtp_port，以及 email / email_password"}

    to = (to_addr or "").strip()
    if not to:
        return {"ok": False, "error": "to_addr required"}

    text = (body or "").strip()
    if include_quote and preview_token:
        try:
            draft = prepare_reply_draft(preview_token)
            text = text + draft.get("quote_suffix", "")
        except Exception as e:
            logger.warning("quote original failed: %s", e)

    em = EmailMessage()
    em["From"] = user
    em["To"] = to
    em["Subject"] = re_subject(subject)
    mid = _normalize_msg_id(in_reply_to)
    if mid:
        em["In-Reply-To"] = mid
    refs = (references or "").strip() or mid
    if refs:
        em["References"] = refs
    em["Message-ID"] = make_msgid(domain=user.split("@")[-1] if "@" in user else "local")
    em.set_content(text or "")

    try:
        if cfg.get("smtp_use_ssl") or port == 465:
            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=ctx, timeout=90) as smtp:
                smtp.login(user, password)
                smtp.send_message(em)
        else:
            with smtplib.SMTP(host, port, timeout=90) as smtp:
                smtp.ehlo()
                smtp.starttls(context=ssl.create_default_context())
                smtp.ehlo()
                smtp.login(user, password)
                smtp.send_message(em)
    except Exception as e:
        logger.exception("SMTP send failed")
        return {"ok": False, "error": "smtp_send_failed", "detail": str(e)}

    return {
        "ok": True,
        "method": "smtp",
        "to": to,
        "subject": em["Subject"],
        "message_id": em["Message-ID"],
    }


def send_reply_by_token(
    preview_token: str,
    body: str,
    *,
    subject: str = "",
    include_quote: bool = True,
) -> dict[str, Any]:
    draft = prepare_reply_draft(preview_token)
    if not draft.get("smtp_configured"):
        webmail = draft.get("webmail") or {}
        if webmail.get("webmail_url"):
            return {
                "ok": False,
                "error": "smtp_not_configured",
                "preferred_method": "webmail",
                "webmail_url": webmail.get("webmail_url"),
                "hint": "未配置 SMTP，请在网页邮箱中打开原信并回复，或补充 config.json 中的 smtp_host / smtp_port。",
            }
        return {"ok": False, "error": "no_reply_method", "hint": "请配置 SMTP 或使用支持的网页邮箱"}

    subj = subject or str(draft.get("subject") or "")
    return send_reply_smtp(
        to_addr=str(draft.get("to") or ""),
        subject=subj,
        body=body,
        in_reply_to=str(draft.get("in_reply_to") or ""),
        references=str(draft.get("references") or ""),
        from_email=str(draft.get("from_email") or ""),
        include_quote=include_quote,
        preview_token=preview_token,
    )


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="回复邮件（SMTP）；网页邮箱请用 webmail_locate --open")
    p.add_argument("--token", required=True, help="preview_token（32 位 hex）")
    p.add_argument("--body", "-b", required=True, help="回复正文")
    p.add_argument("--subject", default="", help="覆盖主题（默认 Re: 原主题）")
    p.add_argument("--no-quote", action="store_true", help="不附引用原文")
    p.add_argument("--draft-json", action="store_true", help="仅输出回复草稿 JSON")
    args = p.parse_args(argv)

    if args.draft_json:
        print(json.dumps(prepare_reply_draft(args.token), ensure_ascii=False, indent=2, default=str))
        return 0

    result = send_reply_by_token(
        args.token,
        args.body,
        subject=args.subject,
        include_quote=not args.no_quote,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
