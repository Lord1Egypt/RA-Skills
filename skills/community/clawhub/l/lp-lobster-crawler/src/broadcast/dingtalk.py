"""钉钉机器人集成 — Webhook 对接。

支持：
- Markdown 格式消息
- 签名验证（加签模式）
- 失败重试
"""

import hashlib
import hmac
import base64
import logging
import os
import time
import urllib.parse
from typing import Any

import requests

logger = logging.getLogger(__name__)

# 重试配置
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒


def _get_webhook_url() -> str:
    """获取钉钉 Webhook URL。"""
    return os.environ.get("DINGTALK_WEBHOOK", "")


def _get_secret() -> str:
    """获取签名密钥。"""
    return os.environ.get("DINGTALK_SECRET", "")


def _sign(secret: str) -> tuple[str, str]:
    """生成签名参数。

    Args:
        secret: 签名密钥。

    Returns:
        (timestamp, sign) 元组。
    """
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_markdown(title: str, content: str, webhook_url: str = "", at_all: bool = False) -> bool:
    """发送 Markdown 格式钉钉消息。

    Args:
        title: 消息标题。
        content: Markdown 正文。
        webhook_url: Webhook URL，为空则从环境变量读取。
        at_all: 是否 @所有人。

    Returns:
        True 表示发送成功。
    """
    url = webhook_url or _get_webhook_url()
    if not url:
        logger.error("DingTalk webhook URL not configured")
        return False

    # 加签
    secret = _get_secret()
    if secret:
        timestamp, sign = _sign(secret)
        url = f"{url}&timestamp={timestamp}&sign={sign}"

    payload: dict[str, Any] = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": content,
        },
        "at": {
            "isAtAll": at_all,
        },
    }

    return _send_with_retry(url, payload)


def send_text(content: str, webhook_url: str = "") -> bool:
    """发送纯文本钉钉消息。

    Args:
        content: 文本内容。
        webhook_url: Webhook URL。

    Returns:
        True 表示发送成功。
    """
    url = webhook_url or _get_webhook_url()
    if not url:
        logger.error("DingTalk webhook URL not configured")
        return False

    secret = _get_secret()
    if secret:
        timestamp, sign = _sign(secret)
        url = f"{url}&timestamp={timestamp}&sign={sign}"

    payload = {
        "msgtype": "text",
        "text": {"content": content},
    }

    return _send_with_retry(url, payload)


def _send_with_retry(url: str, payload: dict[str, Any]) -> bool:
    """带重试的发送逻辑。"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(url, json=payload, timeout=10)
            data = resp.json()

            if data.get("errcode") == 0:
                logger.info("DingTalk message sent successfully")
                return True

            logger.warning(
                "DingTalk API error (attempt %d/%d): code=%s, msg=%s",
                attempt, MAX_RETRIES, data.get("errcode"), data.get("errmsg"),
            )
        except requests.RequestException as e:
            logger.warning(
                "DingTalk request failed (attempt %d/%d): %s",
                attempt, MAX_RETRIES, e,
            )

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY * attempt)

    logger.error("DingTalk message send failed after %d attempts", MAX_RETRIES)
    return False
