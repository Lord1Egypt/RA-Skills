#!/usr/bin/env python3
"""
lunheng 数据下载工具

下载需要额外获取的数据集（因版权原因不随仓库分发）：
- 要素式文书 PDF 分块（用于案由模板）
- 形与神原书扫描页（用于 OCR/检索）

用法：
    python3 scripts/download_data.py
    python3 scripts/download_data.py --skip-if-exists
"""

import os
import sys
import urllib.request
import json
from pathlib import Path

# ─── 路径 ───────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
CHARTS_DIR = DATA_DIR / "pdf_chunks"
PAGES_DIR = DATA_DIR / "pdf_pages"

# ─── 数据源配置（TODO: 替换为实际发布链接）────────
DATA_SOURCES = {
    "pdf_chunks": {
        "url": "",
        "size_mb": 182,
        "destination": CHARTS_DIR,
        "description": "要素式文书模板 PDF 分块（用于案由模板生成）",
    },
    "pdf_pages": {
        "url": "",
        "size_mb": 49,
        "destination": PAGES_DIR,
        "description": "形与神原书扫描页（用于 OCR 检索）",
    },
}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="下载 lunheng 依赖数据")
    parser.add_argument("--skip-if-exists", action="store_true",
                       help="跳过已存在的数据目录")
    args = parser.parse_args()

    has_data = False
    for name, src in DATA_SOURCES.items():
        dest = src["destination"]
        if dest.exists() and any(dest.iterdir()):
            print(f"  ✅ {name}: 已存在 ({src['size_mb']}MB)")
            has_data = True
            continue

        if args.skip_if_existing:
            continue

        if not src["url"]:
            print(f"  ⏳ {name}: 数据源 URL 未配置，请从项目 releases 页面下载")
            print(f"     https://github.com/lunheng/lunheng/releases")
            print(f"     {src['description']} ({src['size_mb']}MB)")
            continue

        print(f"  📥 下载 {name} ({src['size_mb']}MB)...")
        dest.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(src["url"], dest / "data.zip")
            print(f"  ✅ {name}: 下载完成")
            has_data = True
        except Exception as e:
            print(f"  ❌ {name}: 下载失败: {e}")

    if not has_data:
        print("\n⚠️  未检测到数据文件。运行流程会降级为纯模板模式（无分析增强）。")
        print("   详见 README.md 的 Data 章节。")

    print("\n✅ 数据检查完成")


if __name__ == "__main__":
    main()
