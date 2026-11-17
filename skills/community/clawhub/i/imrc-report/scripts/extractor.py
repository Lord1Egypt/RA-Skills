#!/usr/bin/env python3
"""
IMRC 页面数据提取脚本

从 IMRC 系统 10 个页面提取装备所运营数据。
支持浏览器自动化提取和 API 提取两种方式。
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 配置路径
SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
PAGES_CONFIG = CONFIG_DIR / "pages.json"


def load_pages_config():
    """加载页面配置"""
    with open(PAGES_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def get_data_dir(config):
    """获取数据存储目录"""
    workspace = Path(__file__).parent.parent.parent.parent  # workspace root
    data_dir = workspace / config.get("data_dir", "memory/imrc_data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def extract_page_data(page_config, month=None):
    """
    提取单个页面数据
    
    Args:
        page_config: 页面配置 dict
        month: 数据月份 (YYYY-MM)，默认当前月
    
    Returns:
        dict: 提取的数据
    """
    page_name = page_config["name"]
    page_url = page_config["url"]
    unit = page_config["unit"]
    
    print(f"[提取] {page_name} ({page_url})")
    
    # 模拟数据提取（实际使用时通过 browser 工具或 API）
    data = {
        "page_id": page_config["id"],
        "page_name": page_name,
        "url": page_url,
        "unit": unit,
        "month": month or datetime.now().strftime("%Y-%m"),
        "extracted_at": datetime.now().isoformat(),
        "data": {}  # 实际数据由浏览器提取填充
    }
    
    return data


def extract_all_pages(month=None, output_dir=None):
    """
    提取所有 10 个页面数据
    
    Args:
        month: 数据月份 (YYYY-MM)
        output_dir: 输出目录
    
    Returns:
        dict: 所有页面数据
    """
    config = load_pages_config()
    pages = config["pages"]
    
    if output_dir is None:
        output_dir = get_data_dir(config)
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    month = month or datetime.now().strftime("%Y-%m")
    
    all_data = {
        "month": month,
        "extracted_at": datetime.now().isoformat(),
        "pages": []
    }
    
    for page in pages:
        page_data = extract_page_data(page, month)
        all_data["pages"].append(page_data)
        
        # 保存单个页面数据
        page_file = output_dir / f"page_{page['id']}_{page['name']}.json"
        with open(page_file, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)
        print(f"  -> 已保存: {page_file}")
    
    # 保存汇总数据
    summary_file = output_dir / f"imrc_data_{month}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n[完成] 汇总数据已保存: {summary_file}")
    
    return all_data


def main():
    parser = argparse.ArgumentParser(description="IMRC 页面数据提取")
    parser.add_argument("--month", type=str, help="数据月份 (YYYY-MM)，默认当前月")
    parser.add_argument("--output", type=str, help="输出目录")
    args = parser.parse_args()
    
    print(f"=== IMRC 数据提取 ===")
    print(f"月份: {args.month or datetime.now().strftime('%Y-%m')}")
    print()
    
    extract_all_pages(month=args.month, output_dir=args.output)


if __name__ == "__main__":
    main()
