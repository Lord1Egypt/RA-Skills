#!/usr/bin/env python3
"""关键词按搜索意图聚类——把关键词映射到 信息/商业/交易 三组。

纯标准库。对齐 references/growth-channel-matrix.md 的「关键词按意图聚类」。
用于判断需求类型：信息型 / 商业型 / 交易型，便于内容规划与落地页承接。

用法:
    # 默认示例
    python3 scripts/keyword_cluster.py

    # 自定义
    python3 scripts/keyword_cluster.py --pair "项目管理软件" "商业" --pair "项目管理是什么" "信息"

    # 从 STDIN 读：每行 "关键词,意图"
    printf "项目管理软件价格,交易\n项目管理是什么,信息\n" | python3 scripts/keyword_cluster.py
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict

DEFAULT = {
    "项目管理软件": "商业", "好用的项目管理工具": "商业",
    "项目管理是什么": "信息", "如何做项目排期": "信息",
    "项目管理软件价格": "交易", "项目管理软件免费版": "交易",
}


def cluster(kws: dict) -> dict:
    out: dict[str, list[str]] = defaultdict(list)
    for k, intent in kws.items():
        out[intent].append(k)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="关键词按搜索意图聚类")
    ap.add_argument("--pair", nargs=2, action="append", metavar=("KW", "INTENT"),
                    help="关键词 意图，可多次传入")
    args = ap.parse_args()

    data = dict(DEFAULT)
    if args.pair:
        data = {k: v for k, v in args.pair}

    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.strip()
            if not line or "," not in line:
                continue
            k, _, v = line.partition(",")
            data[k.strip()] = v.strip()

    for intent, words in cluster(data).items():
        print(f"[{intent}] " + " / ".join(words))


if __name__ == "__main__":
    main()
