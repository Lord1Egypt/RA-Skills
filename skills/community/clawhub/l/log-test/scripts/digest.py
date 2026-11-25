#!/usr/bin/env python3
"""log-digest 辅助脚本：按级别筛选日志并输出 Markdown 摘要。"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]
LEVEL_ORDER = {name: i for i, name in enumerate(LEVELS)}
LINE_RE = re.compile(r"\[(DEBUG|INFO|WARN|ERROR)\]")


def classify(line):
    """从行内第一个 [LEVEL] 区块取级别；没有则返回 None。"""
    match = LINE_RE.search(line)
    return match.group(1) if match else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", required=True)
    parser.add_argument("--level", default="ERROR", choices=LEVELS)
    parser.add_argument("--max-lines", type=int, default=0,
                        help="最多输出条目数，0 表示不限制")
    args = parser.parse_args()

    path = Path(args.log_file)
    if not path.is_file():
        print("找不到日志文件：%s" % path, file=sys.stderr)
        return 2

    threshold = LEVEL_ORDER[args.level]
    counts = Counter()
    hits = []

    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            level = classify(line)
            if level is None:
                continue
            counts[level] += 1
            if LEVEL_ORDER[level] >= threshold:
                hits.append((level, line.rstrip()))

    if args.max_lines > 0:
        hits = hits[-args.max_lines:]

    print("# 日志摘要：%s" % path.name)
    print()
    print("- 过滤级别：%s 及以上" % args.level)
    print("- 命中条目：%d" % len(hits))
    print("- 各级计数：%s" % ", ".join(
        "%s=%d" % (name, counts[name]) for name in LEVELS))
    print()
    print("## 条目")
    for level, line in hits:
        print("- `%s` %s" % (level, line))

    return 0


if __name__ == "__main__":
    sys.exit(main())