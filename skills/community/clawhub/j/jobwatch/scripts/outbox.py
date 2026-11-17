#!/usr/bin/env python3
"""待播报消息队列（notify 的 agent 模式）。

用法：
  python3 scripts/outbox.py list     # 打印待发送消息（agent 读它，用自己的渠道发给主人）
  python3 scripts/outbox.py archive  # 发送完成后归档清空
"""
import json
import sys
from datetime import datetime

from common import OUTBOX_FILE


def entries():
    if not OUTBOX_FILE.exists():
        return []
    return [json.loads(l) for l in OUTBOX_FILE.read_text().splitlines() if l.strip()]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    es = entries()
    if cmd == "list":
        print(json.dumps({"count": len(es), "messages": es}, ensure_ascii=False, indent=1))
    elif cmd == "archive":
        if es:
            archive = OUTBOX_FILE.parent / "archive"
            archive.mkdir(exist_ok=True)
            OUTBOX_FILE.rename(archive / f"outbox.{datetime.now():%Y%m%d-%H%M%S}.jsonl")
        print(json.dumps({"archived": len(es)}))
    else:
        sys.exit("usage: outbox.py [list|archive]")


if __name__ == "__main__":
    main()
