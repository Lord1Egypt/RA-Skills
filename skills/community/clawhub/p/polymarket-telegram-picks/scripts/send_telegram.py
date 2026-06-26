#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将文本消息发送到配置的 Telegram 聊天。
支持从命令行参数或 stdin 读取内容。
需要环境变量 TELEGRAM_BOT_TOKEN、TELEGRAM_CHAT_ID，或 config/config.json。
"""
import json
import os
import sys
from pathlib import Path

# 技能根目录（脚本在 scripts/ 下）
SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config" / "config.json"


def get_config():
    """从环境变量或 config.json 读取配置。"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        return token.strip(), chat_id.strip()
    if CONFIG_PATH.is_file():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            token = (data.get("telegram_bot_token") or data.get("TELEGRAM_BOT_TOKEN") or "").strip()
            chat_id = (data.get("telegram_chat_id") or data.get("TELEGRAM_CHAT_ID") or "").strip()
            if token and chat_id:
                return token, chat_id
        except Exception:
            pass
    return None, None


def send_message(text: str, token: str, chat_id: str) -> bool:
    """通过 Telegram Bot API 发送文本。"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        body = urlencode({"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"}).encode()
        req = Request(url, data=body, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urlopen(req, timeout=15) as r:
            resp = json.loads(r.read().decode())
            return resp.get("ok") is True
    except Exception as e:
        print(f"[错误] 发送 Telegram 失败: {e}", file=sys.stderr)
        return False


def main():
    token, chat_id = get_config()
    if not token or not chat_id:
        print(
            "未配置 Telegram。请设置环境变量 TELEGRAM_BOT_TOKEN 与 TELEGRAM_CHAT_ID，"
            "或在 config/config.json 中配置 telegram_bot_token、telegram_chat_id。",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read().strip()

    if not text:
        print("无内容可发送。请通过参数或 stdin 传入消息。", file=sys.stderr)
        sys.exit(1)

    # Telegram 单条消息长度限制约 4096
    if len(text) > 4000:
        text = text[:3997] + "..."

    if send_message(text, token, chat_id):
        print("已推送到 Telegram。", file=sys.stderr)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
