#!/usr/bin/env python3
"""Notification adapter for Mail Assistant."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def send_notification(markdown: str, reply_channel: str = "current", output_dir: str | None = None) -> Path:
    out_dir = Path(output_dir or Path(__file__).resolve().parent.parent / ".temp")
    out_dir.mkdir(parents=True, exist_ok=True)
    last_path = out_dir / "last_notification.md"
    timestamp_path = out_dir / f"notification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    payload = markdown.strip() + "\n"
    last_path.write_text(payload, encoding="utf-8")
    timestamp_path.write_text(payload, encoding="utf-8")
    print(payload)
    if reply_channel and reply_channel != "current":
        print(f"\n[邮箱智能体] 结果已准备回推到通道：{reply_channel}")
    return timestamp_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Send notification")
    parser.add_argument("markdown_file")
    parser.add_argument("--reply-channel", default="current")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    markdown = Path(args.markdown_file).read_text(encoding="utf-8")
    send_notification(markdown, args.reply_channel, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
