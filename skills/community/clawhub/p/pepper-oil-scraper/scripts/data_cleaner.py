#!/usr/bin/env python3
"""
data_cleaner.py — 数据清洗与标准化
功能：去重、单位统一、异常值检测、数据合并
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base_scraper import convert_unit


def load_merged(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def deduplicate(records: list[dict]) -> list[dict]:
    """基于 (metric, value, period, region) 去重，保留置信度最高的"""
    seen = {}
    confidence_order = {"high": 3, "medium": 2, "low": 1}

    for rec in records:
        key = (
            rec.get("metric", ""),
            str(rec.get("value", "")),
            rec.get("period", ""),
            rec.get("region", ""),
        )
        existing = seen.get(key)
        if existing is None:
            seen[key] = rec
        else:
            # 保留置信度更高的
            if confidence_order.get(rec.get("confidence", "low"), 0) > \
               confidence_order.get(existing.get("confidence", "low"), 0):
                seen[key] = rec

    return list(seen.values())


def standardize_units(records: list[dict]) -> list[dict]:
    """统一所有记录的单位"""
    for rec in records:
        if rec.get("value") is not None and rec.get("unit"):
            try:
                new_val, new_unit = convert_unit(float(rec["value"]), rec["unit"])
                rec["value_standardized"] = round(new_val, 4)
                rec["unit_standardized"] = new_unit
            except (ValueError, TypeError):
                rec["value_standardized"] = rec["value"]
                rec["unit_standardized"] = rec["unit"]
    return records


def detect_outliers(records: list[dict]) -> list[dict]:
    """标记可能的异常值"""
    # 按 metric 分组
    groups = defaultdict(list)
    for rec in records:
        if rec.get("value") is not None:
            groups[rec.get("metric", "")].append(rec)

    for metric, group in groups.items():
        values = [r["value"] for r in group if r["value"] is not None]
        if len(values) < 3:
            continue
        avg = sum(values) / len(values)
        std = (sum((v - avg) ** 2 for v in values) / len(values)) ** 0.5
        if std == 0:
            continue
        for rec in group:
            if rec["value"] is not None and abs(rec["value"] - avg) > 3 * std:
                rec["outlier_flag"] = True
                rec["outlier_note"] = f"偏离均值{avg:.2f}超过3σ({std:.2f})"

    return records


def group_by_dimension(records: list[dict]) -> dict:
    """按维度分组整理"""
    dimensions = {
        "market_size": [],      # 市场规模
        "price": [],            # 价格
        "production": [],       # 产量/面积
        "company_finance": [],  # 企业财务
        "trade": [],            # 进出口
        "standards": [],        # 标准
        "channel": [],          # 渠道占比
        "links": [],            # 文章链接
        "other": [],
    }

    for rec in records:
        metric = rec.get("metric", "").lower()
        if any(k in metric for k in ["市场规模", "market", "cagr"]):
            dimensions["market_size"].append(rec)
        elif any(k in metric for k in ["价格", "报价", "指数", "price"]):
            dimensions["price"].append(rec)
        elif any(k in metric for k in ["面积", "产量", "消费量", "种植"]):
            dimensions["production"].append(rec)
        elif any(k in metric for k in ["营业", "净利", "毛利", "产能"]):
            dimensions["company_finance"].append(rec)
        elif any(k in metric for k in ["进出口", "出口", "进口", "海关", "hs"]):
            dimensions["trade"].append(rec)
        elif any(k in metric for k in ["标准", "gb", "db"]):
            dimensions["standards"].append(rec)
        elif any(k in metric for k in ["渠道", "占比"]):
            dimensions["channel"].append(rec)
        elif rec.get("extra", {}).get("type") in ("article_link", "report_link", "news_link", "media_article"):
            dimensions["links"].append(rec)
        else:
            dimensions["other"].append(rec)

    return dimensions


def clean_pipeline(filepath: str, output_path: str = None) -> dict:
    """执行完整清洗流程"""
    data = load_merged(filepath)
    records = data.get("records", [])

    print(f"原始记录数: {len(records)}")

    # 1. 去重
    records = deduplicate(records)
    print(f"去重后: {len(records)}")

    # 2. 标准化
    records = standardize_units(records)
    print(f"标准化完成")

    # 3. 异常值检测
    records = detect_outliers(records)
    outliers = [r for r in records if r.get("outlier_flag")]
    print(f"异常值: {len(outliers)}")

    # 4. 分组
    grouped = group_by_dimension(records)
    for dim, recs in grouped.items():
        if recs:
            print(f"  {dim}: {len(recs)} records")

    result = {
        "summary": data.get("summary", {}),
        "clean_stats": {
            "original_count": len(data.get("records", [])),
            "deduplicated_count": len(records),
            "outlier_count": len(outliers),
        },
        "grouped": grouped,
        "all_records": records,
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n清洗结果保存到: {output_path}")

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="数据清洗")
    parser.add_argument("input", help="merged JSON 文件路径")
    parser.add_argument("-o", "--output", default=None, help="输出路径")
    args = parser.parse_args()

    output = args.output or args.input.replace(".json", "_cleaned.json")
    clean_pipeline(args.input, output)
