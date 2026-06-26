#!/usr/bin/env python3
"""
消息推送模块（pusher.py）—— v1.0.0
支持：钉钉（dingtalk）、飞书（feishu）、Telegram（tg）。
全部使用标准库 urllib，零第三方依赖。
"""

__version__ = "1.0.0"

import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import urllib.request


def format_markdown(emails: list[dict], keyword_desc: str = "") -> tuple[str, str]:
    """
    将邮件列表渲染为 (title, markdown_body)。
    供各平台 Markdown 消息类型使用。
    """
    count = len(emails)
    title = f"📬 邮件抓取结果：共 {count} 封"
    if keyword_desc:
        title += f"（过滤：{keyword_desc}）"

    if count == 0:
        body = f"### {title}\n\n今日无匹配邮件。"
        return title, body

    lines = [f"### {title}", ""]
    for idx, m in enumerate(emails, 1):
        lines.append(f"**{idx}. {m.get('subject', '（无主题）')}**")
        lines.append(f"- 发件人：{m.get('from', '')}")
        ts = m.get("timestamp_local") or m.get("timestamp") or m.get("date", "")
        lines.append(f"- 时间：{ts}")
        ext = m.get("extracted_data") or {}
        if ext:
            kv = "，".join(f"{k}={v}" for k, v in ext.items() if v is not None)
            if kv:
                lines.append(f"- 提取：{kv}")
        preview = (m.get("preview") or "").replace("\n", " ").strip()
        if preview:
            lines.append(f"- 预览：{preview}")
        lines.append("")
    return title, "\n".join(lines)


def _http_post(url: str, payload: dict, timeout: int = 10) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw": raw, "status": resp.status}


# ─── 钉钉 ────────────────────────────────────────────────────────────────────

def _dingtalk_sign(secret: str) -> str:
    ts = str(round(time.time() * 1000))
    s  = f"{ts}\n{secret}"
    mac = hmac.new(secret.encode("utf-8"), s.encode("utf-8"), hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(mac))
    return f"&timestamp={ts}&sign={sign}"


def push_dingtalk(webhook_url: str, secret: str, title: str, md_body: str) -> dict:
    url = webhook_url + (_dingtalk_sign(secret) if secret else "")
    payload = {
        "msgtype":  "markdown",
        "markdown": {"title": title, "text": md_body},
    }
    return _http_post(url, payload)


# ─── 飞书 ────────────────────────────────────────────────────────────────────

def _feishu_sign(secret: str) -> tuple[str, str]:
    ts = str(int(time.time()))
    s  = f"{ts}\n{secret}"
    mac = hmac.new(s.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return ts, base64.b64encode(mac).decode("utf-8")


def push_feishu(webhook_url: str, secret: str, title: str, md_body: str) -> dict:
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": title}},
            "elements": [{"tag": "markdown", "content": md_body}],
        },
    }
    if secret:
        ts, sign = _feishu_sign(secret)
        payload["timestamp"] = ts
        payload["sign"] = sign
    return _http_post(webhook_url, payload)


# ─── Telegram ────────────────────────────────────────────────────────────────

def push_telegram(webhook_url: str, chat_id: str, title: str, md_body: str) -> dict:
    """
    webhook_url 格式：https://api.telegram.org/bot<TOKEN>/sendMessage
    chat_id 通过 push_secret 传入。
    """
    text = f"*{title}*\n\n{md_body}"
    payload = {
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": "Markdown",
    }
    return _http_post(webhook_url, payload)


# ─── 统一入口 ────────────────────────────────────────────────────────────────

def push(
    platform: str,
    webhook_url: str,
    secret: str,
    emails: list[dict],
    keyword_desc: str = "",
) -> dict:
    """
    platform: dingtalk | feishu | tg
    secret:   钉钉加签密钥 / 飞书加签密钥 / TG 的 chat_id
    """
    platform = (platform or "").strip().lower()
    if not platform:
        return {"pushed": False, "reason": "platform 未配置"}
    if not webhook_url:
        return {"pushed": False, "reason": "webhook_url 为空"}

    title, md_body = format_markdown(emails, keyword_desc)

    try:
        if platform == "dingtalk":
            resp = push_dingtalk(webhook_url, secret, title, md_body)
        elif platform == "feishu":
            resp = push_feishu(webhook_url, secret, title, md_body)
        elif platform == "tg":
            resp = push_telegram(webhook_url, secret, title, md_body)
        else:
            return {"pushed": False, "reason": f"不支持的平台：{platform}"}
        return {"pushed": True, "platform": platform, "response": resp}
    except Exception as exc:
        return {"pushed": False, "platform": platform, "error": str(exc)}
