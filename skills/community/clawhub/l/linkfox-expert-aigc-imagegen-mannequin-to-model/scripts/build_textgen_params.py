#!/usr/bin/env python3
"""
build_textgen_params.py — 人台换模特 textgen 参数文件构建器

从 templates/mannequin.txt 读取 system prompt，填充 {customer_keywords}，
生成 textgen 链式调用所需的 JSON 参数文件。

Usage:
  python <本skill根目录>/scripts/build_textgen_params.py \\
    --image-urls '["https://example.com/mannequin.jpg"]' \\
    --customer-keywords "Asian female model, studio lighting" \\
    --out "$DATADIR/textgen_mannequin.json"
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")
TEMPLATE_NAME = "mannequin.txt"

MODEL = "GEM_3_1_PRO"
THINKING_LEVEL = "medium"


def _read_template() -> str:
    template_path = os.path.join(TEMPLATES_DIR, TEMPLATE_NAME)
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    with open(template_path, encoding="utf-8") as f:
        return f.read()


def build_params(image_urls: list, *, customer_keywords: str = "") -> dict:
    """构建 textgen 参数 dict（供 CLI 与 run_mannequin.py 共用）。"""
    if not isinstance(image_urls, list):
        raise ValueError("image_urls 必须是 list")
    if not image_urls:
        raise ValueError("image_urls 不能为空")

    customer_keywords = customer_keywords or ""
    template = _read_template()
    prompt = template.replace("{customer_keywords}", customer_keywords)

    return {
        "prompt": prompt,
        "imageUrls": image_urls,
        "model": MODEL,
        "thinkingLevel": THINKING_LEVEL,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="人台换模特 textgen 参数文件构建器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--image-urls",
        required=True,
        help="JSON 数组格式的图片 URL 列表（须为公开 https 地址）",
    )
    parser.add_argument(
        "--customer-keywords",
        default="",
        help="用户补充提示词，映射 {customer_keywords}",
    )
    parser.add_argument("--out", required=True, help="输出 JSON 文件路径")

    args = parser.parse_args()

    try:
        image_urls = json.loads(args.image_urls)
        if not isinstance(image_urls, list):
            raise ValueError("imageUrls 必须是 JSON 数组")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: --image-urls 解析失败: {e}", file=sys.stderr)
        return 1

    try:
        params = build_params(image_urls, customer_keywords=args.customer_keywords)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(params, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"ERROR: 写出参数文件失败: {e}", file=sys.stderr)
        return 1

    print(f"TEXTGEN_PARAMS_PATH={out_path}")
    print(f"  model         : {MODEL}")
    print(f"  thinkingLevel : {THINKING_LEVEL}")
    print(f"  prompt_length : {len(params['prompt'])} chars")
    print(f"  image_urls    : {len(image_urls)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
