#!/usr/bin/env python3
"""
filter_recent.py - 过滤即刻 Topic JSON，仅保留最近 24 小时内的 post

用法：
  autocli jike topic {topic_id} --limit 50 -f json | python3 filter_recent.py
  python3 filter_recent.py --input posts.json
  python3 filter_recent.py --input posts.json --hours 48
  python3 filter_recent.py --input posts.json --output filtered.json

输出：过滤后的 JSON 数组（stdout）及统计摘要（stderr）
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="过滤最近 N 小时内的即刻 posts")
    parser.add_argument(
        "--input", "-i",
        help="输入 JSON 文件路径（不指定则从 stdin 读取）",
    )
    parser.add_argument(
        "--output", "-o",
        help="输出 JSON 文件路径（不指定则输出到 stdout）",
    )
    parser.add_argument(
        "--hours",
        type=float,
        default=24.0,
        help="时间窗口（小时），默认 24",
    )
    return parser.parse_args()


def load_posts(input_path):
    if input_path:
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return json.load(sys.stdin)


def filter_posts(posts, hours):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    recent = []
    skipped = []

    for post in posts:
        raw_time = post.get("time", "")
        try:
            # 兼容带 Z 后缀的 ISO 8601 格式
            post_time = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            print(f"[WARN] 无法解析时间字段：{raw_time!r}，跳过", file=sys.stderr)
            skipped.append(post)
            continue

        if post_time >= cutoff:
            recent.append(post)
        else:
            skipped.append(post)

    return recent, skipped


def main():
    args = parse_args()

    posts = load_posts(args.input)
    if not isinstance(posts, list):
        print("[ERROR] 输入 JSON 应为数组格式", file=sys.stderr)
        sys.exit(1)

    recent, skipped = filter_posts(posts, args.hours)

    # 统计输出到 stderr，不污染 stdout 的 JSON
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cutoff_str = (datetime.now(timezone.utc) - timedelta(hours=args.hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[INFO] 执行时间：{now_str}", file=sys.stderr)
    print(f"[INFO] 时间窗口：最近 {args.hours} 小时（{cutoff_str} 之后）", file=sys.stderr)
    print(f"[INFO] 原始 posts：{len(posts)} 条", file=sys.stderr)
    print(f"[INFO] 保留（24h 内）：{len(recent)} 条", file=sys.stderr)
    print(f"[INFO] 过滤掉：{len(skipped)} 条", file=sys.stderr)

    result = json.dumps(recent, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[INFO] 结果已写入：{args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
