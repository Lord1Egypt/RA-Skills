#!/usr/bin/env python3
"""
IMAP 邮件读取模块（reader.py）—— v1.0.0
核心能力：
  1. 极端字符串归一化匹配：剥离全角/半角空格、换行、零宽字符等，精准命中
  2. 精确时间窗（start_datetime ~ end_datetime）：本地时区严格比对，跨日跨时区零漏件
  3. 内置主流邮箱服务器路由表（provider）：aliyun/qq/gmail/outlook 等开箱即用
  4. 正则结构化字段提取（extract_patterns）
"""

__version__ = "1.0.0"

import imaplib
import email
import email.utils
from email import message
import re
import json
from email.header import decode_header, make_header
from datetime import datetime, timedelta, timezone


# ─── 内置主流邮箱服务商路由表 ───────────────────────────────────────────────
PROVIDER_ROUTES: dict[str, tuple[str, int]] = {
    # 国内
    "aliyun":      ("imap.qiye.aliyun.com", 993),   # 阿里云企业邮箱
    "aliyun_mail": ("imap.aliyun.com",      993),   # 阿里云个人邮箱
    "qq":          ("imap.qq.com",          993),   # QQ 邮箱
    "exmail":      ("imap.exmail.qq.com",   993),   # 腾讯企业邮箱
    "tencent":     ("imap.exmail.qq.com",   993),   # 别名
    "163":         ("imap.163.com",         993),   # 网易 163
    "126":         ("imap.126.com",         993),   # 网易 126
    "yeah":        ("imap.yeah.net",        993),   # 网易 yeah
    "sina":        ("imap.sina.com",        993),   # 新浪
    "sohu":        ("imap.sohu.com",        993),   # 搜狐
    "139":         ("imap.139.com",         993),   # 中国移动
    # 国际
    "gmail":       ("imap.gmail.com",       993),
    "outlook":     ("outlook.office365.com", 993),  # Outlook / Hotmail / Office365
    "hotmail":     ("outlook.office365.com", 993),
    "office365":   ("outlook.office365.com", 993),
    "yahoo":       ("imap.mail.yahoo.com",  993),
    "icloud":      ("imap.mail.me.com",     993),
    "fastmail":    ("imap.fastmail.com",    993),
    "zoho":        ("imap.zoho.com",        993),
    "protonmail":  ("127.0.0.1",            1143),  # 需 ProtonMail Bridge 本地代理
}

DEFAULT_PROVIDER = "aliyun"


def resolve_server(provider: str = "", imap_host: str = "", imap_port: int = 0) -> tuple[str, int]:
    """
    优先级：provider > imap_host/imap_port > 默认（aliyun）
    """
    p = (provider or "").strip().lower()
    if p:
        if p not in PROVIDER_ROUTES:
            raise ValueError(
                f"未知的 provider：{provider}。支持列表：{', '.join(sorted(PROVIDER_ROUTES.keys()))}"
            )
        return PROVIDER_ROUTES[p]

    host = (imap_host or "").strip()
    port = int(imap_port or 0)
    if host:
        return host, (port or 993)

    return PROVIDER_ROUTES[DEFAULT_PROVIDER]


# ─── 极端字符串归一化 ─────────────────────────────────────────────────────────
# 覆盖：
#   - \s       —— Python re.UNICODE 下涵盖半角空格、\t \n \r \f \v、以及 \u00A0、\u2028、\u3000 等
#   - \u200B-\u200F —— 零宽空格 / 零宽连接 / 左右标记
#   - \u202A-\u202E —— 双向格式控制符（LRE/RLE/PDF/LRO/RLO）
#   - \u2060        —— Word Joiner
#   - \uFEFF        —— BOM / ZWNBSP
_NORMALIZE_PATTERN = re.compile(r"[\s\u200B-\u200F\u202A-\u202E\u2060\uFEFF]+")


def _normalize(text: str) -> str:
    """彻底清除所有空白与不可见字符，用于裸字符串匹配。"""
    if not text:
        return ""
    return _NORMALIZE_PATTERN.sub("", str(text))


# ─── 基础工具 ────────────────────────────────────────────────────────────────

def _decode_str(raw) -> str:
    if raw is None:
        return ""
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        parts = decode_header(raw)
        out = []
        for content, charset in parts:
            if isinstance(content, bytes):
                out.append(content.decode(charset or "utf-8", errors="replace"))
            else:
                out.append(content)
        return "".join(out)


def _strip_html(html: str) -> str:
    html = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<(br|p|div|tr|li)[^>]*/?>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<[^>]+>", "", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def _extract_plain_text(msg: message.Message) -> str:
    plain_parts, html_parts = [], []
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if "attachment" in disp:
                continue
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            text = payload.decode(charset, errors="replace")
            if ct == "text/plain":
                plain_parts.append(text)
            elif ct == "text/html":
                html_parts.append(text)
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True)
        if payload:
            text = payload.decode(charset, errors="replace")
            if msg.get_content_type() == "text/plain":
                plain_parts.append(text)
            elif msg.get_content_type() == "text/html":
                html_parts.append(text)

    if plain_parts:
        return "\n".join(plain_parts).strip()
    if html_parts:
        return _strip_html("\n".join(html_parts)).strip()
    return ""


# ─── 关键字匹配（归一化后做 in 判定） ────────────────────────────────────────

def _parse_keywords(raw) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(k).strip() for k in raw if str(k).strip()]
    return [k.strip() for k in str(raw).split(",") if k.strip()]


def _match(text: str, keywords: list[str], logic: str) -> bool:
    """
    归一化后做大小写不敏感的 substring 匹配。
    空关键字组视为恒真。
    """
    if not keywords:
        return True
    haystack = _normalize(text).lower()
    hits = [_normalize(k).lower() in haystack for k in keywords if _normalize(k)]
    if not hits:
        return True
    return all(hits) if logic.upper() == "AND" else any(hits)


# ─── 时间窗解析 ──────────────────────────────────────────────────────────────

def _get_local_tz():
    """返回服务器本地时区（aware tzinfo）。"""
    return datetime.now().astimezone().tzinfo


def _parse_user_datetime(s: str, local_tz) -> datetime:
    """
    解析用户传入的 'YYYY-MM-DD HH:MM:SS' 或 'YYYY-MM-DD' 为 aware datetime。
    默认附加服务器本地时区。支持 ISO 8601 带 tz 的输入。
    """
    s = (s or "").strip()
    if not s:
        raise ValueError("日期时间字符串为空")

    # 允许 'YYYY-MM-DDTHH:MM:SS' 或带 tz 的 ISO 格式
    try:
        dt = datetime.fromisoformat(s.replace(" ", "T"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=local_tz)
        return dt
    except ValueError:
        pass

    # 兜底：仅日期
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=local_tz)
        except ValueError:
            continue

    raise ValueError(f"无法解析 datetime 字符串：{s!r}（期望格式 'YYYY-MM-DD HH:MM:SS'）")


def _parse_email_date(date_raw: str) -> datetime | None:
    if not date_raw:
        return None
    try:
        dt = email.utils.parsedate_to_datetime(date_raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


# ─── 结构化字段提取 ─────────────────────────────────────────────────────────

def _compile_patterns(patterns) -> dict:
    if not patterns:
        return {}
    if isinstance(patterns, str):
        try:
            patterns = json.loads(patterns)
        except json.JSONDecodeError:
            return {}
    if not isinstance(patterns, dict):
        return {}
    compiled = {}
    for name, expr in patterns.items():
        try:
            compiled[str(name)] = re.compile(str(expr), re.IGNORECASE | re.MULTILINE)
        except re.error:
            compiled[str(name)] = None
    return compiled


def _apply_patterns(body: str, compiled: dict) -> dict:
    out = {}
    for name, regex in compiled.items():
        if regex is None:
            out[name] = None
            continue
        m = regex.search(body or "")
        if not m:
            out[name] = None
        elif m.groups():
            out[name] = m.group(1)
        else:
            out[name] = m.group(0)
    return out


# ─── 主函数 ──────────────────────────────────────────────────────────────────

def fetch_emails(
    email_account: str,
    auth_password: str,
    start_datetime: str = "",
    end_datetime: str = "",
    subject_keywords=None,
    body_keywords=None,
    match_logic: str = "AND",
    extract_patterns=None,
    preview_length: int = 500,
    provider: str = "",
    imap_host: str = "",
    imap_port: int = 0,
) -> dict:
    """
    返回 {
      "server": "host:port",
      "window": {"from": "...", "to": "...", "tz": "..."},
      "emails": [...],
    }
    """
    host, port = resolve_server(provider, imap_host, imap_port)

    subj_list = _parse_keywords(subject_keywords)
    body_list = _parse_keywords(body_keywords)
    logic = (match_logic or "AND").upper()
    if logic not in ("AND", "OR"):
        logic = "AND"

    local_tz = _get_local_tz()
    now_local = datetime.now(local_tz)

    # 时间窗解析（默认：最近 24h）
    if end_datetime:
        end_dt = _parse_user_datetime(end_datetime, local_tz)
    else:
        end_dt = now_local
    if start_datetime:
        start_dt = _parse_user_datetime(start_datetime, local_tz)
    else:
        start_dt = end_dt - timedelta(hours=24)

    if start_dt > end_dt:
        raise ValueError(f"start_datetime ({start_dt}) 晚于 end_datetime ({end_dt})")

    compiled_patterns = _compile_patterns(extract_patterns)

    # IMAP SINCE 粒度为日期，用 start_dt 的本地日期做保守服务端粗筛
    since_date = start_dt.astimezone(local_tz).strftime("%d-%b-%Y")

    emails_out = []

    with imaplib.IMAP4_SSL(host, port) as imap:
        status, _ = imap.login(email_account, auth_password)
        if status != "OK":
            raise RuntimeError(f"IMAP 登录失败。status={status}")

        status, _ = imap.select("INBOX", readonly=True)
        if status != "OK":
            raise RuntimeError("无法选中收件箱（INBOX）。")

        status, uid_data = imap.uid("SEARCH", None, f"SINCE {since_date}")
        if status != "OK":
            raise RuntimeError(f"IMAP SEARCH 失败。status={status}")

        uid_list = uid_data[0].split() if uid_data and uid_data[0] else []

        for uid in uid_list:
            status, header_data = imap.uid(
                "FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])"
            )
            if status != "OK" or not header_data or not header_data[0]:
                continue
            raw_header = header_data[0][1] if isinstance(header_data[0], tuple) else b""
            if not raw_header:
                continue

            header_msg = email.message_from_bytes(raw_header)
            subject  = _decode_str(header_msg.get("Subject", "（无主题）"))
            sender   = _decode_str(header_msg.get("From", ""))
            date_raw = header_msg.get("Date", "")

            # 时间窗严格比对（转换到相同本地时区再比）
            mail_dt = _parse_email_date(date_raw)
            if mail_dt is None:
                continue
            mail_dt_local = mail_dt.astimezone(local_tz)
            if not (start_dt <= mail_dt_local <= end_dt):
                continue

            # 主题归一化匹配
            if not _match(subject, subj_list, logic):
                continue

            # 阶段二：拉完整邮件做正文匹配 + 字段提取
            status, msg_data = imap.uid("FETCH", uid, "(RFC822)")
            if status != "OK" or not msg_data or not msg_data[0]:
                continue
            raw_email = msg_data[0][1] if isinstance(msg_data[0], tuple) else b""
            full_msg = email.message_from_bytes(raw_email)
            body = _extract_plain_text(full_msg)

            if not _match(body, body_list, logic):
                continue

            extracted_data = _apply_patterns(body, compiled_patterns)

            emails_out.append({
                "uid":             uid.decode() if isinstance(uid, bytes) else str(uid),
                "from":            sender,
                "timestamp":       mail_dt_local.isoformat(),
                "timestamp_local": mail_dt_local.strftime("%Y-%m-%d %H:%M:%S %z"),
                "subject":         subject,
                "extracted_data":  extracted_data,
                "preview":         body[:preview_length] + ("…" if len(body) > preview_length else ""),
            })

    emails_out.sort(key=lambda x: x["timestamp"], reverse=True)

    return {
        "server": f"{host}:{port}",
        "window": {
            "from": start_dt.strftime("%Y-%m-%d %H:%M:%S %z"),
            "to":   end_dt.strftime("%Y-%m-%d %H:%M:%S %z"),
            "tz":   str(local_tz),
        },
        "emails": emails_out,
    }


# 兼容别名
fetch_recent_emails = fetch_emails
fetch_today_emails  = fetch_emails
