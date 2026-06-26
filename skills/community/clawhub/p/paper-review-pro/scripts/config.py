#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初始化配置文件

支持配置项：
- default_n: 默认检索数量
- default_k: 核心词汇返回数量
- min_year: 截止年份
- default_p: 每个扩展词保留数量
- authority_weight: 权威度分数权重（0.0-1.0）
- llm: LLM 相关配置
"""

import os
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="初始化配置文件")
    parser.add_argument("--default_n", type=int, default=10, help="默认检索数量")
    parser.add_argument("--default_k", type=int, default=2, help="核心词汇返回数量")
    parser.add_argument("--min_year", type=int, default=2025, help="截止年份")
    parser.add_argument("--default_p", type=int, default=2, help="每个扩展词保留数量")
    parser.add_argument("--authority-weight", type=float, default=0.3, dest="authority_weight",
                        help="权威度分数权重（0.0-1.0，默认 0.3）")
    parser.add_argument("--gateway-url", type=str, default="http://localhost:14940", dest="gateway_url",
                        help="OpenClaw Gateway URL")
    parser.add_argument("--model", type=str, default="qwen3.5-plus", help="Dashscope 模型名称")
    
    args = parser.parse_args()
    
    CONFIG_DIR = os.path.expanduser("~/.openclaw/paper-review-pro")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

    DEFAULT_CONFIG = {
        "default_n": args.default_n,  # 检索数量
        "default_k": args.default_k,  # 核心词汇返回数量
        "min_year": args.min_year,  # 截止年份
        "default_p": args.default_p,  # 每个扩展词保留数量
        "authority_weight": args.authority_weight,  # 权威度分数权重
        "storage": {
            "papers_dir": os.path.join(CONFIG_DIR, "papers"),
            "index_file": os.path.join(CONFIG_DIR, "index.json")
        },
        "llm": {
            "enabled": True,
            "gateway_url": args.gateway_url,
            "dashscope_model": args.model
        }
    }

    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

    print("✓ 配置完成:", CONFIG_FILE)
    print(f"\n当前配置:")
    print(f"  检索数量 (default_n): {args.default_n}")
    print(f"  核心论文数 (default_k): {args.default_k}")
    print(f"  截止年份 (min_year): {args.min_year}")
    print(f"  扩展词保留数 (default_p): {args.default_p}")
    print(f"  权威度权重 (authority_weight): {args.authority_weight}")
    print(f"  LLM 模型：{args.model}")


if __name__ == "__main__":
    main()
