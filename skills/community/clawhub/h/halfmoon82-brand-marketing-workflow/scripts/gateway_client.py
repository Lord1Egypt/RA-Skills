#!/usr/bin/env python3
"""
gateway_client.py - brand-marketing-workflow gateway 消息发送模块

提供：
  load_config()    - 读取 ~/.openclaw/openclaw.json
  gateway_send()   - 通过本地 gateway 发送 Telegram/Feishu 消息
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

# ─── 常量 ────────────────────────────────────────────────────────────────────

OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
GATEWAY_URL = "http://127.0.0.1:18789"

# ─── 配置加载 ─────────────────────────────────────────────────────────────────

_config_cache: dict | None = None


def load_config() -> dict:
    """读取 ~/.openclaw/openclaw.json，返回完整配置 dict。单次读取后缓存。"""
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            _config_cache = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"配置文件不存在: {OPENCLAW_CONFIG_PATH}") from None
    except json.JSONDecodeError as e:
        raise RuntimeError(f"配置文件 JSON 格式错误: {e}") from None
    return _config_cache


def _get_gateway_token() -> str:
    cfg = load_config()
    token = cfg.get("gateway", {}).get("auth", {}).get("token", "")
    if not token:
        raise RuntimeError("gateway.auth.token 未在 openclaw.json 中配置")
    return token


# ─── Gateway 消息发送 ────────────────────────────────────────────────────────

def gateway_send(
    channel: str,
    account_id: str,
    to: str,
    message: str,
) -> bool:
    """
    通过本地 gateway 发送消息（Telegram / Feishu）。

    参数：
      channel    - 渠道名称，如 "telegram" 或 "feishu"
      account_id - Bot 账号 ID，如 "bot1" 或 "bot4"
      to         - 目标用户/群组 ID
      message    - 消息内容

    返回：True 成功，False 失败（不 raise）
    """
    try:
        token = _get_gateway_token()
    except RuntimeError:
        return False

    body = json.dumps({
        "channel": channel,
        "accountId": account_id,
        "to": to,
        "message": message,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{GATEWAY_URL}/api/messages/send",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status not in (200, 201, 202):
                return False
            try:
                body_data = json.loads(resp.read().decode("utf-8", errors="replace"))
                if body_data.get("ok", True) is False:
                    return False
            except (json.JSONDecodeError, AttributeError):
                pass
            return True
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return False
