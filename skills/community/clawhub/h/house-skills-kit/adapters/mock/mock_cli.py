#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mock 适配器演示 CLI — 全部为编造样例数据，仅用于演示接口契约，严禁用于真实咨询。"""
import argparse
import json
import sys

# 样例数据 —— 明确标注为虚构
MOCK_LISTINGS = [
    {"id": "MOCK-001", "name": "示例花园", "district": "五华区", "price_wan": 118,
     "area_sqm": 89, "layout": "3室2厅", "year": 2018, "tags": ["近地铁", "满五唯一"]},
    {"id": "MOCK-002", "name": "样例苑", "district": "盘龙区", "price_wan": 96,
     "area_sqm": 76, "layout": "2室2厅", "year": 2012, "tags": ["低总价", "南北通透"]},
    {"id": "MOCK-003", "name": "演示里", "district": "官渡区", "price_wan": 135,
     "area_sqm": 105, "layout": "4室2厅", "year": 2021, "tags": ["次新", "带学位指标(以官方为准)"]},
]


def cmd_search(args):
    results = MOCK_LISTINGS
    if args.district:
        results = [r for r in results if args.district in r["district"]]
    if args.max_price:
        results = [r for r in results if r["price_wan"] <= args.max_price]
    return {"total": len(results), "disclaimer": "以下为演示用虚构数据",
            "items": results}


def cmd_detail(args):
    for r in MOCK_LISTINGS:
        if r["id"].lower() == args.id.lower():
            return dict(r, disclaimer="演示用虚构数据",
                        risk_notes=["产权/抵押状态请以官方核验为准"])
    return {"error": f"未找到 {args.id}", "hint": "试试 MOCK-001"}


def cmd_resblock(args):
    return {"name": args.name, "avg_price_wan": 128, "sample_size": 3,
            "disclaimer": "演示用虚构数据，不代表真实行情",
            "trend_note": "样例：近12个月窄幅震荡"}


def main():
    ap = argparse.ArgumentParser(description="house-skills-kit mock adapter (虚构数据)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search", help="搜索房源(虚构)")
    p.add_argument("--city", default="昆明")
    p.add_argument("--district", default=None)
    p.add_argument("--min-price", type=int, default=None)
    p.add_argument("--max-price", type=int, default=None)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("detail", help="房源详情(虚构)")
    p.add_argument("--id", required=True)
    p.set_defaults(fn=cmd_detail)

    p = sub.add_parser("resblock", help="小区信息(虚构)")
    p.add_argument("--name", required=True)
    p.set_defaults(fn=cmd_resblock)

    args = ap.parse_args()
    print(json.dumps(args.fn(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
