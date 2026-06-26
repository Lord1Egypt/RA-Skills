#!/usr/bin/env python3
"""
main_crawler.py — 花椒油/藤椒油产业数据爬虫主调度器
用法：
  python main_crawler.py --all                     # 全量采集
  python main_crawler.py --category price           # 按类别
  python main_crawler.py --site cnhnb --site cnr    # 指定站点
  python main_crawler.py --list                     # 列出所有站点
  python main_crawler.py --all --output /tmp/data/  # 指定输出目录
"""

import argparse
import json
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# 确保能 import 本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_scraper import load_config
from adapters import ADAPTER_REGISTRY, CATEGORY_MAP, get_adapter, get_adapters_by_category

logger = logging.getLogger("crawler.main")


def list_sites(config):
    """列出所有可用站点"""
    print(f"\n{'='*70}")
    print(f"  花椒油/藤椒油产业数据爬虫 — 共 {len(ADAPTER_REGISTRY)} 个站点")
    print(f"{'='*70}\n")
    for cat, ids in CATEGORY_MAP.items():
        cat_names = {
            "price": "A. 原料价格与供需",
            "market": "B. 行业研究报告",
            "company": "C. 企业与财报",
            "gov": "D. 政府与标准",
            "media": "E. 财经媒体",
            "global": "F. 全球市场",
        }
        print(f"  [{cat_names.get(cat, cat)}]")
        for aid in ids:
            site = config["sites"].get(aid, {})
            name = site.get("name", aid)
            domain = site.get("base_url", "").replace("https://", "").replace("http://", "").rstrip("/")
            js = " 🔧JS" if site.get("needs_js") else ""
            print(f"    {aid:<20s} {name:<15s} {domain}{js}")
        print()


def run_crawl(adapter_ids: list[str], config: dict, output_dir: str) -> list[str]:
    """执行爬取，返回输出文件路径列表"""
    results = []
    total = len(adapter_ids)

    for i, aid in enumerate(adapter_ids, 1):
        print(f"\n{'─'*50}")
        print(f"  [{i}/{total}] {aid} — {config['sites'].get(aid, {}).get('name', '?')}")
        print(f"{'─'*50}")

        try:
            scraper = get_adapter(aid, config)
            path = scraper.run(output_dir)
            results.append(path)

            output = scraper.get_output()
            print(f"  ✓ {output['record_count']} records, {output['request_count']} requests → {path}")

        except Exception as e:
            logger.error(f"Failed to run {aid}: {e}", exc_info=True)
            print(f"  ✗ Error: {e}")

    return results


def merge_results(file_paths: list[str], output_dir: str) -> str:
    """合并所有结果到一个汇总 JSON"""
    all_records = []
    summary = {"total_records": 0, "by_category": {}, "by_site": {}, "crawl_time": datetime.now().isoformat()}

    for fp in file_paths:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            cat = data.get("category", "unknown")
            site = data.get("adapter_id", "unknown")
            count = data.get("record_count", 0)

            summary["by_category"][cat] = summary["by_category"].get(cat, 0) + count
            summary["by_site"][site] = count
            summary["total_records"] += count

            for rec in data.get("records", []):
                rec["_source_adapter"] = site
                rec["_source_category"] = cat
                all_records.append(rec)
        except Exception as e:
            logger.warning(f"Cannot read {fp}: {e}")

    merged = {
        "summary": summary,
        "records": all_records
    }

    out_path = Path(output_dir) / f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    return str(out_path)


def main():
    parser = argparse.ArgumentParser(description="花椒油/藤椒油产业数据爬虫")
    parser.add_argument("--all", action="store_true", help="爬取所有站点")
    parser.add_argument("--category", "-c", action="append", help="按类别爬取 (price|market|company|gov|media|global)")
    parser.add_argument("--site", "-s", action="append", help="爬取指定站点 (adapter_id)")
    parser.add_argument("--output", "-o", default=None, help="输出目录")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用站点")
    parser.add_argument("--no-merge", action="store_true", help="不合并结果文件")
    args = parser.parse_args()

    config = load_config()
    output_dir = args.output or config["global_settings"]["output_dir"]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if args.list:
        list_sites(config)
        return

    # 确定要爬的站点
    adapter_ids = []
    if args.all:
        adapter_ids = list(ADAPTER_REGISTRY.keys())
    elif args.category:
        for cat in args.category:
            adapter_ids.extend(CATEGORY_MAP.get(cat, []))
    elif args.site:
        adapter_ids = args.site
    else:
        parser.print_help()
        print("\n请指定 --all, --category 或 --site 参数")
        return

    # 去重保序
    seen = set()
    unique_ids = []
    for aid in adapter_ids:
        if aid not in seen:
            seen.add(aid)
            unique_ids.append(aid)
    adapter_ids = unique_ids

    # 验证
    invalid = [a for a in adapter_ids if a not in ADAPTER_REGISTRY]
    if invalid:
        print(f"未知站点: {invalid}")
        print(f"可用站点: {list(ADAPTER_REGISTRY.keys())}")
        return

    print(f"\n🌶  花椒油/藤椒油产业数据爬虫")
    print(f"   待采集站点: {len(adapter_ids)}")
    print(f"   输出目录: {output_dir}\n")

    # 执行
    file_paths = run_crawl(adapter_ids, config, output_dir)

    # 合并
    if file_paths and not args.no_merge:
        merged_path = merge_results(file_paths, output_dir)
        print(f"\n{'='*50}")
        print(f"  📊 合并结果: {merged_path}")

    print(f"\n{'='*50}")
    print(f"  ✅ 完成！共 {len(file_paths)} 个站点数据文件")
    print(f"  📁 输出目录: {output_dir}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
