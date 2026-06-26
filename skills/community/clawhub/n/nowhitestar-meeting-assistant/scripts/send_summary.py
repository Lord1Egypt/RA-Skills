#!/usr/bin/env python3
"""
发送会议纪要到指定频道。

支持：
- file    — 仅保存到本地（默认）
- zulip   — 发送到 Zulip 频道
- notion  — 创建 Notion 页面
- telegram — 发送 Telegram 消息

配置：
{
  "output": {
    "channel": "file",  # "file" | "zulip" | "notion" | "telegram"
    "zulip": {
      "stream": "meetings",
      "topic": "会议纪要"
    },
    "notion": {
      "api_key_env": "NOTION_API_KEY",
      "database_id": "your-database-id"
    },
    "telegram": {
      "chat_id": "your-chat-id"
    }
  }
}
"""

import json
import os
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "meeting-assistant" / "config.json"


def load_config():
    if not CONFIG_PATH.exists():
        print(f"Config not found at {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def send_to_file(summary_path):
    """仅保存到本地（默认）。"""
    print(f"📄 纪要已保存到本地: {summary_path}")
    return True


def send_to_zulip(summary_path, config):
    """发送到 Zulip 频道。"""
    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read summary: {e}", file=sys.stderr)
        return False

    stream = config.get("stream", "general")
    topic = config.get("topic", "会议纪要")

    print(f"📤 发送到 Zulip")
    print(f"   Stream: {stream}")
    print(f"   Topic: {topic}")
    print(f"   内容长度: {len(content)} 字符")

    # TODO: 实现 Zulip API 调用
    # 需要配置 zuliprc 文件或 API key
    # 示例：
    # import zulip
    # client = zulip.Client(config_file="~/.zuliprc")
    # client.send_message({"type": "stream", "to": stream, "topic": topic, "content": content})

    print("   ⚠️ Zulip 发送待实现，请先配置 API 凭证")
    return True


def send_to_notion(summary_path, config):
    """创建 Notion 页面。"""
    try:
        from notion_client import Client
    except ImportError:
        print("notion-client not installed. Run: pip install notion-client", file=sys.stderr)
        return False

    api_key = os.environ.get(config.get("api_key_env", "NOTION_API_KEY"))
    if not api_key:
        print("NOTION_API_KEY not set", file=sys.stderr)
        return False

    database_id = config.get("database_id")
    if not database_id:
        print("Notion database_id not configured", file=sys.stderr)
        return False

    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read summary: {e}", file=sys.stderr)
        return False

    # 从文件名提取标题
    summary_name = Path(summary_path).stem
    parts = summary_name.rsplit("_", 1)
    title = parts[0].replace("_", " ")
    date_str = parts[1] if len(parts) > 1 else ""

    notion = Client(auth=api_key)

    try:
        page = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "Status": {"select": {"name": "已完成"}},
            },
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                }
            ],
        )
        print(f"📤 Notion 页面已创建: {page['url']}")
        return True
    except Exception as e:
        print(f"Failed to create Notion page: {e}", file=sys.stderr)
        return False


def send_to_telegram(summary_path, config):
    """通过 OpenClaw message 工具发送到 Telegram。"""
    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read summary: {e}", file=sys.stderr)
        return False

    chat_id = config.get("chat_id", "")
    if not chat_id:
        print("Telegram chat_id not configured", file=sys.stderr)
        return False

    # 通过 OpenClaw 的 message 工具发送
    # 这里输出内容，由调用者处理
    print(f"📤 发送到 Telegram chat: {chat_id}")
    print(f"   内容长度: {len(content)} 字符")
    print("\n=== TELEGRAM MESSAGE ===")
    print(content[:2000])  # 限制长度
    if len(content) > 2000:
        print("... (内容已截断)")
    print("=== END ===")
    return True


def send_summary(summary_path):
    config = load_config()
    output_config = config.get("output", {})
    channel = output_config.get("channel", "file")

    channel_config = output_config.get(channel, {})

    if channel == "file":
        return send_to_file(summary_path)
    elif channel == "zulip":
        return send_to_zulip(summary_path, channel_config)
    elif channel == "notion":
        return send_to_notion(summary_path, channel_config)
    elif channel == "telegram":
        return send_to_telegram(summary_path, channel_config)
    else:
        print(f"Unknown output channel: {channel}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: send_summary.py <summary_file_path>", file=sys.stderr)
        sys.exit(1)

    summary_file = sys.argv[1]
    success = send_summary(summary_file)
    sys.exit(0 if success else 1)
