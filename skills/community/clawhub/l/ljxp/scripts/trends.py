#!/usr/bin/env python3
"""
蓝鲸选品 - 行业趋势查询脚本
调用 /trends/* 系列接口，包括统计、销量、价格、竞争等9个子命令。

用法:
  python trends.py --token <TOKEN> --type <TYPE> --site MLM --category-id MLM458037 [其他参数]

子命令 (--type):
  statistical      - 行业趋势统计概览
  sold_his         - 销量历史趋势
  sale_list        - 子类目销量分布（需 --month）
  price_list       - 价格区间分布
  inventory_type   - 仓储类型分布（需 --month）
  new_items        - 新品机会指数
  top_sellers      - 竞争店铺排行
  top_items        - 竞争商品排行
  top_brands       - 竞争品牌排行

示例:
  python trends.py --token abc123 --type statistical --site MLM --category-id MLM458037
  python trends.py --token abc123 --type sold_his --site MLM --category-id MLM458037
  python trends.py --token abc123 --type sale_list --site MLM --category-id MLM458037 --month 202608
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    get_token, request_get, check_response, output_json,
    SITE_NAMES, VALID_SITES
)

# 子命令映射
TYPE_MAP = {
    "statistical":    ("/trends/statistical",       "行业趋势统计"),
    "sold_his":       ("/trends/sold/his",          "销量历史"),
    "sale_list":      ("/trends/sale/list",         "销量分布"),
    "price_list":     ("/trends/price/list",        "价格分布"),
    "inventory_type": ("/trends/store/inventoryType","仓储类型分布"),
    "new_items":      ("/trends/new/items",         "新品机会指数"),
    "top_sellers":    ("/trends/brand/top/sellers", "竞争店铺"),
    "top_items":      ("/trends/brand/top/items",   "竞争商品"),
    "top_brands":     ("/trends/brand/top/brands",  "竞争品牌"),
}


def print_statistical(data):
    """打印统计概览"""
    print(f"\n{'='*60}")
    print(f"行业趋势统计概览")
    print(f"{'='*60}")
    print(f"总商品数:       {data.get('total', 'N/A'):>10}  (月环比: {data.get('hbTotal', 'N/A')}  日环比: {data.get('rhbTotal', 'N/A')})")
    print(f"活跃商品数:     {data.get('itemCount', 'N/A'):>10}  (月环比: {data.get('hbItemCount', 'N/A')}  日环比: {data.get('rhbItemCount', 'N/A')})")
    print(f"总销量:         {data.get('soldTotal', 'N/A'):>10}  (月环比: {data.get('hbSoldTotal', 'N/A')}  日环比: {data.get('rhbSoldTotal', 'N/A')})")
    print(f"总销售额:       {data.get('amountTotal', 'N/A'):>10}  (月环比: {data.get('hbAmountTotal', 'N/A')}  日环比: {data.get('rhbAmountTotal', 'N/A')})")
    print(f"日均销量:       {data.get('avgSold', 'N/A'):>10}  (月环比: {data.get('hbAvgSold', 'N/A')})")
    print(f"平均成交价:     {data.get('avgAmount', 'N/A'):>10}  (月环比: {data.get('hbAvgAmount', 'N/A')}  日环比: {data.get('rhbAvgAmount', 'N/A')})")
    print(f"月销量环比增长: {data.get('monthGrowth', 'N/A')}")


def print_sold_his(data):
    """打印销量历史"""
    data_list = data.get("dataList", [])
    print(f"\n{'='*70}")
    print(f"销量历史趋势 (币种: {data.get('currencyId', 'N/A')})")
    print(f"{'日期':<12} {'销量':>10} {'销售额':>12} {'单价':>10}")
    print(f"{'-'*70}")
    for d in data_list:
        print(f"{d.get('date',''):<12} {d.get('sold',''):>10} {d.get('amount',''):>12} {d.get('price',''):>10}")
    print(f"{'='*70}")


def print_sale_list(items):
    """打印销量分布"""
    print(f"\n{'='*60}")
    print(f"子类目销量分布")
    print(f"{'类目ID':<20} {'名称':<20} {'中文名':<15} {'总销量':>10}")
    print(f"{'-'*60}")
    total_sold = 0
    for d in items:
        sold = d.get('soldTotal', 0)
        total_sold += sold
        print(f"{d.get('categoryId',''):<20} {d.get('name','')[:18]:<20} {d.get('nameZn','')[:13]:<15} {sold:>10}")
    print(f"{'-'*60}")
    print(f"{'合计':>40} {total_sold:>10}")


def print_price_list(items):
    """打印价格分布"""
    print(f"\n{'='*60}")
    print(f"价格区间分布")
    print(f"{'价格区间':<20} {'商品数量':>10} {'数值':>10} {'价格':>10}")
    print(f"{'-'*60}")
    for d in items:
        print(f"{d.get('key',''):<20} {d.get('count',''):>10} {d.get('value',''):>10} {d.get('price',''):>10}")
    print(f"{'='*60}")


def print_inventory_type(data):
    """打印仓储类型分布"""
    all_data = data.get("all", {}) or {}
    print(f"\n{'='*60}")
    print(f"仓储类型分布")
    print(f"{'='*60}")
    print(f"FBM占比: {data.get('fbm', 'N/A')}")
    print(f"\n总体: 销售额={all_data.get('amount','N/A')}  30天销量={all_data.get('sale30','N/A')}  "
          f"均价={all_data.get('avgPrice','N/A')}  商品数={all_data.get('totalItems','N/A')}")

    for key, label in [("full", "FULL"), ("cbt", "CBT"), ("cbtFull", "CBT-FULL"),
                        ("cbtNotFull", "CBT-非FULL"), ("localFull", "本土-FULL"),
                        ("localNotFull", "本土-非FULL")]:
        sub = data.get(key, {}) or {}
        if sub:
            print(f"  {label:<12}: 销量={sub.get('sum',''):>8}  数量={sub.get('count',''):>8}  均价={sub.get('price',''):>10}")

    usa = data.get("usa", {}) or {}
    if usa:
        print(f"\n美国仓: CBT商品数={usa.get('usaCbtCount','')}  FULL商品数={usa.get('usaFullCount','')}  "
              f"CBT销量={usa.get('usaCbtSale','')}  FULL销量={usa.get('usaFullSale','')}")


def print_new_items(data):
    """打印新品机会"""
    print(f"\n{'='*60}")
    print(f"新品机会指数")
    print(f"{'='*60}")
    print(f"总销量:   30天={data.get('sale30','N/A')}  60天={data.get('sale60','N/A')}  "
          f"90天={data.get('sale90','N/A')}  180天={data.get('sale180','N/A')}")
    print(f"新品销量: 30天={data.get('newSale30','N/A')}  60天={data.get('newSale60','N/A')}  "
          f"90天={data.get('newSale90','N/A')}  180天={data.get('newSale180','N/A')}")
    print(f"新品占比: 30天={data.get('newRate30','N/A')}  60天={data.get('newRate60','N/A')}  "
          f"90天={data.get('newRate90','N/A')}  180天={data.get('newRate180','N/A')}")

    daily = data.get("dailySaleList", [])
    if daily:
        print(f"\n每日上架趋势 (最近{daily[-1]['date'] if daily else ''}):")
        for d in daily[-30:]:
            bar = "█" * min(int(d.get("value", 0) / max(1, max(x.get("value", 1) for x in daily)) * 40), 40)
            print(f"  {d.get('date','')} {d.get('value',0):>5} {bar}")


def print_top_list(data, kind="seller"):
    """打印排行列表（店铺/商品/品牌）"""
    label_map = {"seller": "竞争店铺", "item": "竞争商品", "brand": "竞争品牌"}
    print(f"\n{'='*70}")
    print(f"{label_map.get(kind, '排行')} - {data.get('categoryName', 'N/A')} ({data.get('categoryNameCn', 'N/A')})")
    print(f"类目30天销量: {data.get('sale30','N/A')} | 汇总: {data.get('sumSale30','N/A')} "
          f"| 全部商品: {data.get('allCount','N/A')} | {label_map.get(kind, '')}数量: {data.get('sellerCount','N/A')}")
    print(f"{'='*70}")

    top_list = data.get("topList", [])
    if kind == "seller":
        print(f"{'排名':<5} {'店铺名':<25} {'商品数':>8} {'均价':>8} {'销量':>10} {'类型':<10}")
        for i, s in enumerate(top_list, 1):
            print(f"{i:<5} {s.get('key','')[:23]:<25} {s.get('count',''):>8} "
                  f"{s.get('price',''):>8} {s.get('volume',''):>10} {s.get('sellerType',''):<10}")
    elif kind == "item":
        print(f"{'排名':<5} {'商品名':<30} {'品牌':<15} {'价格':>8} {'销量':>10}")
        for i, s in enumerate(top_list, 1):
            print(f"{i:<5} {s.get('title','')[:28]:<30} {s.get('key','')[:13]:<15} "
                  f"{s.get('price',''):>8} {s.get('volume',''):>10}")
    else:
        print(f"{'排名':<5} {'品牌名':<30} {'商品数':>8} {'均价':>8} {'销量':>10}")
        for i, s in enumerate(top_list, 1):
            print(f"{i:<5} {s.get('key','')[:28]:<30} {s.get('count',''):>8} "
                  f"{s.get('price',''):>8} {s.get('volume',''):>10}")

    print(f"币种: {data.get('currencyId', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 行业趋势查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  statistical     - 统计概览: 总商品数/活跃数/销量/销售额/均价
  sold_his        - 销量历史: 每日销量/销售额/单价趋势
  sale_list       - 销量分布: 子类目销量排行（需 --month）
  price_list      - 价格分布: 各价格区间商品数量
  inventory_type  - 仓储类型: FBM/FULL/CBT/本地分布（需 --month）
  new_items       - 新品机会: 新品销量占比 + 上架趋势
  top_sellers     - 竞争店铺: 类目Top店铺
  top_items       - 竞争商品: 类目Top商品
  top_brands      - 竞争品牌: 类目Top品牌

示例:
  %(prog)s --token YOUR_TOKEN --type statistical --site MLM --category-id MLM458037
  %(prog)s --token YOUR_TOKEN --type sold_his --site MLM --category-id MLM458037
  %(prog)s --token YOUR_TOKEN --type sale_list --site MLM --category-id MLM458037 --month 202608
        """
    )
    parser.add_argument("--token", default=None, help="Authorization Token。⚠️ [不推荐] 会暴露在 shell 历史/进程列表；优先使用环境变量 LJXP_TOKEN")
    parser.add_argument("--type", required=True, choices=list(TYPE_MAP.keys()),
                        help="趋势查询类型")
    parser.add_argument("--site", default="MLM", choices=VALID_SITES, help="站点")
    parser.add_argument("--category-id", required=True, help="类目ID (必填)")
    parser.add_argument("--month", default=None, help="月份 (YYYYMM)，sale_list和inventory_type需要")
    parser.add_argument("--output", default="table", choices=["table", "json"],
                        help="输出格式: table, json")

    args = parser.parse_args()
    token = get_token(args.token)

    path, label = TYPE_MAP[args.type]
    params = {"siteId": args.site, "categoryId": args.category_id}
    if args.month:
        params["month"] = args.month

    print(f"正在查询 {SITE_NAMES.get(args.site, args.site)} {label}...", file=sys.stderr)
    response = request_get(path, token, params)
    check_response(response)

    if args.output == "json":
        output_json(response)
        return

    data = response.get("data", {})
    t = args.type

    if t == "statistical":
        print_statistical(data)
    elif t == "sold_his":
        print_sold_his(data)
    elif t == "sale_list":
        print_sale_list(data if isinstance(data, list) else [])
    elif t == "price_list":
        print_price_list(data if isinstance(data, list) else [])
    elif t == "inventory_type":
        print_inventory_type(data)
    elif t == "new_items":
        print_new_items(data)
    elif t == "top_sellers":
        print_top_list(data, "seller")
    elif t == "top_items":
        print_top_list(data, "item")
    elif t == "top_brands":
        print_top_list(data, "brand")

    # 提示关联操作
    print(f"\n💡 提示: 获取类目洞察后，可在该类目下搜索商品:")
    print(f"   python search_items.py --token <TOKEN> --site {args.site} --category-id {args.category_id} --sort-key sale30 --sort-order desc")


if __name__ == "__main__":
    main()
