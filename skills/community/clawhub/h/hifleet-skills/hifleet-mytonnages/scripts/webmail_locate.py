#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在网页邮箱中定位原始邮件（方式 B）。

原理：在默认浏览器打开邮箱网页的「搜索」深链，利用发件人、主题、时间、Message-ID 等
构造唯一性尽量高的检索条件。依赖用户浏览器中**已登录**的邮箱会话（未登录时需手动登录一次）。

说明：
- 无法在服务端替用户自动填密码登录（安全与厂商限制）。
- Gmail 支持 rfc822msgid 运算符，通常可唯一定位到单封邮件。
- 其他厂商多为「搜索页」深链，结果通常只剩 1 条时需用户点一下打开。
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import webbrowser
from datetime import datetime, timedelta, timezone
from email.utils import parseaddr
from pathlib import Path
from typing import Any, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent


def default_skill_dir() -> Path:
    env_path = os.environ.get("HIFLEET_MYTONNAGES_DIR", "").strip()
    if env_path:
        return Path(env_path).expanduser()
    return _SCRIPT_DIR.parent


def _load_mail_config() -> dict[str, str]:
    cfg_path = default_skill_dir() / "config.json"
    cfg: dict[str, Any] = {}
    if cfg_path.is_file():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg = data
        except (json.JSONDecodeError, OSError):
            pass
    host = str(cfg.get("imap_host") or os.environ.get("IMAP_HOST") or "").strip().lower()
    email = str(cfg.get("email") or cfg.get("imap_user") or os.environ.get("IMAP_USER") or "").strip().lower()
    return {"imap_host": host, "email": email}


def extract_email_address(from_addr: str) -> str:
    """从 'Name <user@x.com>' 或裸地址提取邮箱。"""
    _name, addr = parseaddr(from_addr or "")
    if addr:
        return addr.strip().lower()
    m = re.search(r"[\w.+-]+@[\w.-]+\.\w+", from_addr or "", re.I)
    return (m.group(0) if m else "").lower()


def _normalize_message_id(message_id: str) -> str:
    mid = (message_id or "").strip()
    if not mid or mid.startswith("generated-@"):
        return ""
    if not (mid.startswith("<") and mid.endswith(">")):
        mid = f"<{mid.strip('<>')}>"
    return mid


def _parse_email_date(email_date_utc: str) -> Optional[datetime]:
    raw = (email_date_utc or "").strip()
    if not raw:
        return None
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(raw.replace("Z", "+0000"), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            continue
    return None


def _gmail_date_parts(dt: datetime) -> tuple[str, str]:
    """Gmail after:/before: 使用本地日历日，前后各扩 1 天以提高命中。"""
    day = dt.astimezone(timezone.utc).date()
    after = (day - timedelta(days=1)).strftime("%Y/%m/%d")
    before = (day + timedelta(days=2)).strftime("%Y/%m/%d")
    return after, before


def _quote_subject(subject: str) -> str:
    s = (subject or "").strip()
    if not s:
        return ""
    if any(c in s for c in ' \t"'):
        return '"' + s.replace('"', "") + '"'
    return s


def detect_webmail_provider(imap_host: str = "", email: str = "") -> str:
    host = (imap_host or "").lower()
    domain = ""
    if "@" in (email or ""):
        domain = email.split("@", 1)[1].lower()

    checks = [
        ("gmail", ("imap.gmail.com", "gmail.com", "googlemail.com")),
        ("outlook", ("imap-mail.outlook.com", "outlook.office365.com", "outlook.com", "hotmail.com", "live.com")),
        ("yahoo", ("imap.mail.yahoo.com", "yahoo.com")),
        ("qq", ("imap.qq.com", "qq.com", "foxmail.com")),
        ("163", ("imap.163.com", "163.com")),
        ("126", ("imap.126.com", "126.com")),
        ("yeah", ("imap.yeah.net", "yeah.net")),
        ("aliyun", ("imap.aliyun.com", "aliyun.com")),
        ("aliyun_enterprise", ("imap.qiye.aliyun.com", "qiye.aliyun.com")),
        ("exmail", ("imap.exmail.qq.com", "exmail.qq.com")),
    ]
    for name, keys in checks:
        if any(k in host or k == domain for k in keys):
            return name

    if domain:
        return "generic"
    return "unknown"


# 厂商搜索能力：operators=支持 from:/subject:/日期运算符；keyword=仅普通关键词
_PROVIDER_SEARCH_MODE: dict[str, str] = {
    "gmail": "operators",
    "outlook": "operators",
    "yahoo": "operators",
    "qq": "keyword",
    "exmail": "keyword",
    "163": "keyword",
    "126": "keyword",
    "yeah": "keyword",
    "aliyun": "keyword",
    "aliyun_enterprise": "keyword",
    "generic": "keyword",
    "unknown": "keyword",
}

_TIER_LABELS: dict[str, str] = {
    "rfc822msgid": "Message-ID（最精确）",
    "composite_full": "发件人 + 主题 + 时间",
    "composite": "发件人 + 主题",
    "subject_only": "仅主题",
    "from_only": "仅发件人",
    "subject_keyword": "主题关键词",
    "subject_truncated": "主题（缩短）",
    "sender_keyword": "发件人邮箱",
    "sender_local": "发件人前缀",
    "date_keyword": "仅日期",
    "message_id_keyword": "Message-ID 关键词",
}


def _dedupe_query_tiers(tiers: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for query, method in tiers:
        q = (query or "").strip()
        if not q or q in seen:
            continue
        seen.add(q)
        out.append((q, method))
    return out


def _subject_keywords(subject: str, *, max_len: int = 48) -> list[tuple[str, str]]:
    raw = (subject or "").strip()
    if not raw:
        return []
    tiers: list[tuple[str, str]] = [(raw, "subject_keyword")]
    if len(raw) > max_len:
        short = raw[:max_len].rstrip()
        if short and short != raw:
            tiers.append((short, "subject_truncated"))
    return tiers


def _build_operator_tiers(
    *,
    provider: str,
    mid: str,
    sender: str,
    subj_quoted: str,
    dt: Optional[datetime],
) -> list[tuple[str, str]]:
    """Gmail / Outlook / Yahoo：支持 from:、subject:、日期运算符。"""
    prov = provider.lower()
    tiers: list[tuple[str, str]] = []

    if prov == "gmail" and mid:
        tiers.append((f"rfc822msgid:{mid}", "rfc822msgid"))

    date_parts: list[str] = []
    date_keyword = ""
    if dt:
        after, before = _gmail_date_parts(dt)
        if prov in ("gmail", "outlook", "yahoo"):
            date_parts = [f"after:{after}", f"before:{before}"]
        date_keyword = dt.astimezone(timezone.utc).strftime("%Y-%m-%d")

    if sender and subj_quoted:
        if date_parts:
            tiers.append(
                (
                    " ".join([f"from:{sender}", f"subject:{subj_quoted}"] + date_parts),
                    "composite_full",
                )
            )
        tiers.append((f"from:{sender} subject:{subj_quoted}", "composite"))

    if mid and prov in ("outlook", "yahoo"):
        inner = mid.strip("<>")
        tiers.append((f'from:{sender} "{inner}"' if sender else f'"{inner}"', "message_id_keyword"))

    if subj_quoted:
        tiers.append((f"subject:{subj_quoted}", "subject_only"))
        # 部分 Outlook 网页对 subject: 支持不稳，再备一条裸主题
        bare = subj_quoted.strip('"')
        if bare:
            tiers.append((bare, "subject_keyword"))

    if sender:
        tiers.append((f"from:{sender}", "from_only"))

    if date_keyword and sender:
        tiers.append((f"from:{sender} {date_keyword}", "composite"))

    if date_keyword:
        tiers.append((date_keyword, "date_keyword"))

    return tiers


def _build_keyword_tiers(
    *,
    sender: str,
    subject: str,
    dt: Optional[datetime],
) -> list[tuple[str, str]]:
    """163 / QQ / 阿里邮等：通常只支持普通关键词，条件越多越容易搜不到。"""
    tiers: list[tuple[str, str]] = []

    # 国内网页邮箱：优先主题（命中率高），再发件人，最后日期
    tiers.extend(_subject_keywords(subject))

    if sender:
        tiers.append((sender, "sender_keyword"))
        local = sender.split("@", 1)[0]
        if local and local != sender:
            tiers.append((local, "sender_local"))

    if dt:
        tiers.append((dt.astimezone(timezone.utc).strftime("%Y-%m-%d"), "date_keyword"))

    return tiers


def build_search_query_tiers(
    *,
    message_id: str = "",
    from_addr: str = "",
    subject: str = "",
    email_date_utc: str = "",
    provider: str = "",
) -> list[tuple[str, str]]:
    """
    按「由严到宽」返回多档搜索条件；搜不到时可依次尝试下一档。
    每项为 (search_query, method)。
    """
    prov = (provider or "unknown").lower()
    mid = _normalize_message_id(message_id)
    sender = extract_email_address(from_addr)
    subj = _quote_subject(subject)
    dt = _parse_email_date(email_date_utc)
    mode = _PROVIDER_SEARCH_MODE.get(prov, "keyword")

    if mode == "operators":
        tiers = _build_operator_tiers(provider=prov, mid=mid, sender=sender, subj_quoted=subj, dt=dt)
    else:
        tiers = _build_keyword_tiers(sender=sender, subject=subject, dt=dt)

    return _dedupe_query_tiers(tiers)


def build_search_query(
    *,
    message_id: str = "",
    from_addr: str = "",
    subject: str = "",
    email_date_utc: str = "",
    provider: str = "",
) -> tuple[str, str]:
    """返回首选（最精确）的一档搜索条件。"""
    tiers = build_search_query_tiers(
        message_id=message_id,
        from_addr=from_addr,
        subject=subject,
        email_date_utc=email_date_utc,
        provider=provider,
    )
    if tiers:
        return tiers[0]
    return "", "none"


def build_webmail_url(
    search_query: str,
    provider: str,
    *,
    email_account: str = "",
) -> tuple[str, str]:
    """
    返回 (url, method_detail)。
    method_detail: search_deeplink | inbox_fallback
    """
    prov = (provider or "unknown").lower()
    q = (search_query or "").strip()
    enc = urllib.parse.quote(q, safe="")

    if prov == "gmail":
        account_index = 0
        if email_account and "@" in email_account:
            # 多账号时 Gmail /u/N/ 可能需用户自行切换；默认 u/0
            account_index = 0
        if q:
            return f"https://mail.google.com/mail/u/{account_index}/#search/{enc}", "search_deeplink"
        return f"https://mail.google.com/mail/u/{account_index}/", "inbox_fallback"

    if prov == "outlook":
        if q:
            return f"https://outlook.live.com/mail/0/search?q={enc}", "search_deeplink"
        return "https://outlook.live.com/mail/0/", "inbox_fallback"

    if prov == "yahoo":
        if q:
            return f"https://mail.yahoo.com/d/search/keyword={enc}", "search_deeplink"
        return "https://mail.yahoo.com/", "inbox_fallback"

    if prov == "qq":
        if q:
            return f"https://mail.qq.com/cgi-bin/mail_list?folderid=1&page=0&s={enc}", "search_deeplink"
        return "https://mail.qq.com/", "inbox_fallback"

    if prov in ("163", "126", "yeah"):
        base = {"163": "163", "126": "126", "yeah": "yeah"}.get(prov, "163")
        if q:
            return f"https://mail.{base}.com/js6/main.jsp#module=mbox.SearchModule|{enc}", "search_deeplink"
        return f"https://mail.{base}.com/", "inbox_fallback"

    if prov == "aliyun":
        if q:
            return f"https://mail.aliyun.com/alimail/search?q={enc}", "search_deeplink"
        return "https://mail.aliyun.com/", "inbox_fallback"

    if prov == "aliyun_enterprise":
        if q:
            return f"https://qiye.aliyun.com/alimail/search?q={enc}", "search_deeplink"
        return "https://qiye.aliyun.com/alimail/", "inbox_fallback"

    if prov == "exmail":
        if q:
            return f"https://exmail.qq.com/cgi-bin/mail_list?folderid=1&s={enc}", "search_deeplink"
        return "https://exmail.qq.com/", "inbox_fallback"

    # generic: 尝试用邮箱域名拼网页入口
    if email_account and "@" in email_account:
        domain = email_account.split("@", 1)[1]
        return f"https://mail.{domain}/", "inbox_fallback"
    return "", "unsupported"


def build_webmail_locate(
    *,
    message_id: str = "",
    from_addr: str = "",
    subject: str = "",
    email_date_utc: str = "",
    imap_host: str = "",
    email_account: str = "",
    tier: int = 0,
) -> dict[str, Any]:
    cfg = _load_mail_config()
    host = imap_host or cfg.get("imap_host") or ""
    account = email_account or cfg.get("email") or ""
    provider = detect_webmail_provider(host, account)
    query_tiers = build_search_query_tiers(
        message_id=message_id,
        from_addr=from_addr,
        subject=subject,
        email_date_utc=email_date_utc,
        provider=provider,
    )

    search_tiers: list[dict[str, Any]] = []
    for level, (query, method) in enumerate(query_tiers):
        url, url_method = build_webmail_url(query, provider, email_account=account)
        if not url or url_method != "search_deeplink":
            continue
        search_tiers.append(
            {
                "level": level,
                "query": query,
                "method": method,
                "label": _TIER_LABELS.get(method, method),
                "url": url,
            }
        )

    if not search_tiers:
        url, url_method = build_webmail_url("", provider, email_account=account)
        if url:
            return {
                "webmail_url": url,
                "webmail_provider": provider,
                "webmail_method": "inbox_fallback",
                "webmail_search_query": "",
                "webmail_search_tiers": [],
                "webmail_tier": 0,
                "webmail_fallback_count": 0,
                "webmail_hint": "无法构造搜索条件，仅打开邮箱收件箱，请手动搜索发件人/主题。",
            }
        return {
            "webmail_url": "",
            "webmail_provider": provider,
            "webmail_method": "unsupported",
            "webmail_search_query": "",
            "webmail_search_tiers": [],
            "webmail_tier": 0,
            "webmail_fallback_count": 0,
            "webmail_hint": "无法识别邮箱厂商，请使用系统内 preview_url 预览，或手动在邮箱中搜索。",
        }

    tier_idx = max(0, min(int(tier), len(search_tiers) - 1))
    chosen = search_tiers[tier_idx]
    fallback_count = max(0, len(search_tiers) - 1)

    hints = {
        "rfc822msgid": "将在浏览器打开 Gmail 并按 Message-ID 搜索；若已登录，通常直接显示该邮件。",
        "search_deeplink": "将在浏览器打开邮箱搜索页；若未登录请先登录。",
    }
    hint = hints.get(chosen["method"], hints["search_deeplink"])
    if fallback_count:
        hint += (
            f" 若本页搜不到结果，请改用下方「放宽搜索」链接（共 {fallback_count} 档，"
            f"条件逐级减少：发件人/主题/时间/Message-ID）。"
        )

    return {
        "webmail_url": chosen["url"],
        "webmail_provider": provider,
        "webmail_method": chosen["method"],
        "webmail_search_query": chosen["query"],
        "webmail_search_tiers": search_tiers,
        "webmail_tier": tier_idx,
        "webmail_fallback_count": fallback_count,
        "webmail_hint": hint,
    }


def build_webmail_locate_from_row(row: dict[str, Any]) -> dict[str, Any]:
    return build_webmail_locate(
        message_id=str(row.get("message_id") or ""),
        from_addr=str(row.get("from_addr") or ""),
        subject=str(row.get("subject") or ""),
        email_date_utc=str(row.get("email_date_utc") or ""),
    )


def open_webmail_in_browser(
    *,
    message_id: str = "",
    from_addr: str = "",
    subject: str = "",
    email_date_utc: str = "",
    tier: int = 0,
) -> dict[str, Any]:
    info = build_webmail_locate(
        message_id=message_id,
        from_addr=from_addr,
        subject=subject,
        email_date_utc=email_date_utc,
        tier=tier,
    )
    url = info.get("webmail_url") or ""
    if not url:
        info["opened"] = False
        info["error"] = "no webmail_url"
        return info
    webbrowser.open(url, new=2)
    info["opened"] = True
    return info


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="在网页邮箱中定位并打开原始邮件（浏览器须已登录邮箱）")
    p.add_argument("--message-id", default="", help="Message-ID")
    p.add_argument("--from-addr", default="", help="发件人")
    p.add_argument("--subject", default="", help="主题")
    p.add_argument("--email-date-utc", default="", help="发件时间（UTC ISO）")
    p.add_argument("--tier", type=int, default=0, help="搜索档位 0=最精确，越大条件越少")
    p.add_argument("--open", action="store_true", help="用系统默认浏览器打开 webmail_url")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    args = p.parse_args(argv)

    if args.open:
        result = open_webmail_in_browser(
            message_id=args.message_id,
            from_addr=args.from_addr,
            subject=args.subject,
            email_date_utc=args.email_date_utc,
            tier=args.tier,
        )
    else:
        result = build_webmail_locate(
            message_id=args.message_id,
            from_addr=args.from_addr,
            subject=args.subject,
            email_date_utc=args.email_date_utc,
            tier=args.tier,
        )
        result = {"ok": True, **result}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("webmail_url") or result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
