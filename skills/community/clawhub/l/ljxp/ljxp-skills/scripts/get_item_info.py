#!/usr/bin/env python3
"""
蓝鲸选品 - 商品详情及关联查询脚本
调用 /item/info, /item/daily, /item/monthly, /item/review, /item/keyword/reverse

用法:
  python get_item_info.py --token <TOKEN> --item-id <ID>                    # 商品详情
  python get_item_info.py --token <TOKEN> --item-id <ID> --daily             # 每日数据
  python get_item_info.py --token <TOKEN> --item-id <ID> --monthly           # 每月数据
  python get_item_info.py --token <TOKEN> --item-id <ID> --reviews           # 评价
  python get_item_info.py --token <TOKEN> --item-id <ID> --keywords          # 流量词反查
  python get_item_info.py --token <TOKEN> --item-id <ID> --all               # 全部查询
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import get_token, request_get, check_response, output_json


def print_item_info(item):
    """打印商品详情"""
    rating = item.get("rating", {}) or {}
    seller = item.get("sellerInfo", {}) or {}
    shipping = item.get("shipping", {}) or {}
    weight_info = item.get("weightInfo", {}) or {}

    print(f"\n{'='*60}")
    print(f"商品ID:      {item.get('id', 'N/A')}")
    print(f"标题:        {item.get('title', 'N/A')}")
    print(f"站点:        {item.get('siteId', 'N/A')}")
    print(f"类目:        {item.get('categoryName', 'N/A')} ({item.get('categoryNameZn', 'N/A')})")
    print(f"类目路径:    {' > '.join([p.get('name','') for p in item.get('pathFromRoot',[])])}")
    print(f"{'='*60}")
    print(f"\n--- 价格信息 ---")
    print(f"单价:        {item.get('price', 'N/A')} {item.get('currencyId', 'N/A')}")
    print(f"原价:        {item.get('basePrice', 'N/A')}")
    print(f"最低/最高:   {item.get('minPrice', 'N/A')} / {item.get('maxPrice', 'N/A')}")
    print(f"平均单价:    {item.get('avgPrice', 'N/A')}")
    print(f"佣金:        {item.get('saleFeeAmount', 'N/A')}")

    print(f"\n--- 销售数据 ---")
    print(f"7天:  销量={item.get('sale7','N/A')}  GMV={item.get('gmv7','N/A')}  转化率={item.get('saleRate7','N/A')}")
    print(f"30天: 销量={item.get('sale30','N/A')} GMV={item.get('gmv30','N/A')} 转化率={item.get('saleRate30','N/A')}")
    print(f"60天: 销量={item.get('sale60','N/A')} GMV={item.get('gmv60','N/A')}")
    print(f"90天: 销量={item.get('sale90','N/A')} GMV={item.get('gmv90','N/A')}")
    print(f"总销量:      {item.get('soldQuantity', 'N/A')} (概数: {item.get('soldStock', 'N/A')})")
    print(f"总访问量:    {item.get('visitTotal', 'N/A')}")

    print(f"\n--- 库存与状态 ---")
    print(f"库存:        {item.get('availableQuantity', 'N/A')} (期初: {item.get('initialQuantity', 'N/A')})")
    print(f"状态:        {item.get('itemStatus', 'N/A')} | 曝光级别: {item.get('listingMode', 'N/A')}")
    print(f"变体数量:    {item.get('variationsCount', 'N/A')}")
    print(f"上架时间:    {item.get('startTime', 'N/A')}")
    print(f"健康度:      {item.get('health', 'N/A')} | BSR: N/A")
    print(f"评分:        {rating.get('stars', 'N/A')} ({rating.get('amount', 0)}评)")

    print(f"\n--- 店铺信息 ---")
    print(f"名称:        {seller.get('name', 'N/A')} (ID: {item.get('sellerId', 'N/A')})")
    print(f"类型:        {seller.get('sellerType', 'N/A')} | 等级: {seller.get('levelId', 'N/A')}")
    print(f"注册日期:    {seller.get('registrationDate', 'N/A')}")
    print(f"店铺商品数:  {seller.get('itemTotal', 'N/A')} | 近一年销量: {seller.get('saleTotal', 'N/A')}")
    print(f"店铺链接:    {seller.get('permalink', 'N/A')}")

    print(f"\n--- 物流信息 ---")
    print(f"运输模式:    {shipping.get('mode', 'N/A')} | 包邮: {shipping.get('freeShipping', 'N/A')}")
    print(f"仓储类型:    {item.get('logisticType', 'N/A')} | 物流类型: {item.get('shippingHtmlType', 'N/A')}")
    print(f"包裹重量:    {item.get('packetWeight', 'N/A')}g")

    if weight_info.get("finalFreight"):
        print(f"\n--- 运费估算 ---")
        print(f"重量:        {weight_info.get('weight', 'N/A')}")
        print(f"最终运费:    {weight_info.get('finalFreight', 'N/A')}")
        print(f"附加费:      {weight_info.get('additionalCost', 'N/A')}")

    # 汇率
    rate_site = item.get("rateSite", {}) or {}
    rate_rmb = item.get("rateRmb", {}) or {}
    if rate_site.get("rate"):
        print(f"\n--- 汇率 ---")
        print(f"美金汇率:    {rate_site.get('rate', 'N/A')} ({rate_site.get('rateDate', 'N/A')})")
        print(f"人民币汇率:  {rate_rmb.get('rate', 'N/A')} ({rate_rmb.get('rateDate', 'N/A')})")

    # 变体
    variations = item.get("variations", [])
    if variations:
        print(f"\n--- 变体列表 ({len(variations)}个) ---")
        for i, v in enumerate(variations):
            attrs = ", ".join([f"{a.get('name')}:{a.get('valueName')}" for a in v.get("attrs", [])])
            print(f"  [{i+1}] {attrs} | 价格:{v.get('price')} | 库存:{v.get('availableQuantity')} | 30天销量:{v.get('sale30')}")

    print(f"\n商品链接: {item.get('url', 'N/A')}")


def print_daily_data(items):
    """打印每日数据表格"""
    print(f"\n{'='*70}")
    print(f"{'日期':<12} {'价格':>10} {'销量':>8} {'库存':>8} {'访问量':>8}")
    print(f"{'-'*70}")
    for d in items:
        print(f"{d.get('date',''):<12} {d.get('price',''):>10} {d.get('soldQuantity',''):>8} "
              f"{d.get('availableQuantity',''):>8} {d.get('visit',''):>8}")
    print(f"{'='*70}")


def print_monthly_data(items):
    """打印每月数据表格"""
    print(f"\n{'='*60}")
    print(f"{'月份':<10} {'销售额':>12} {'销量':>8} {'访问量':>10} {'币种':>6}")
    print(f"{'-'*60}")
    for d in items:
        print(f"{d.get('month',''):<10} {d.get('amount',''):>12} {d.get('soldQuantity',''):>8} "
              f"{d.get('visit',''):>10} {d.get('currencyId',''):>6}")
    print(f"{'='*60}")


def print_reviews(reviews):
    """打印评价列表"""
    for i, r in enumerate(reviews, 1):
        print(f"\n--- 评价 {i} ---")
        print(f"评分: {'⭐'*int(r.get('rate', 0))} ({r.get('rate')})")
        print(f"时间: {r.get('createTime', 'N/A')}")
        print(f"原文: {r.get('content', 'N/A')[:200]}")
        if r.get("contentZh"):
            print(f"翻译: {r.get('contentZh')[:200]}")


def print_keywords(data):
    """打印流量词反查结果"""
    item_info = data.get("itemInfo", {})
    print(f"\n--- 商品信息 ---")
    print(f"ID: {item_info.get('id')} | 标题: {item_info.get('title')}")
    print(f"价格: {item_info.get('price')} | 30天销量: {item_info.get('sale30')} | 访问量: {item_info.get('visit30')}")

    key_list = data.get("keyList", [])
    print(f"\n--- 流量关键词 ({len(key_list)}个) ---")
    print(f"{'排名':<6} {'关键词':<30} {'中文':<20} {'流量占比':<10} {'30天销量':<10} {'商品数':<8}")
    print(f"{'-'*90}")
    for kw in key_list:
        print(f"{kw.get('paiming', kw.get('ranking', '')):<6} "
              f"{kw.get('key', '')[:28]:<30} "
              f"{kw.get('keyCn', '')[:18]:<20} "
              f"{kw.get('bgl', ''):<10} "
              f"{kw.get('sale30', ''):<10} "
              f"{kw.get('totalItem', ''):<8}")


def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 商品详情及关联查询",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --token YOUR_TOKEN --item-id MLB123456789
  %(prog)s --token YOUR_TOKEN --item-id MLB123456789 --daily
  %(prog)s --token YOUR_TOKEN --item-id MLB123456789 --all
        """
    )
    parser.add_argument("--token", default=None, help="Authorization Token (也可通过环境变量 LJXP_TOKEN)。⚠️ [不推荐] 会暴露在 shell 历史/进程列表；优先使用环境变量 LJXP_TOKEN")
    parser.add_argument("--item-id", required=True, help="商品ID (必填)")
    parser.add_argument("--product-id", default=None, help="目录链接ID (可选)")

    # 查询选项
    parser.add_argument("--all", action="store_true", help="查询全部: 详情+每日+每月+评价+关键词")
    parser.add_argument("--daily", action="store_true", help="查询商品每日数据")
    parser.add_argument("--monthly", action="store_true", help="查询商品每月数据")
    parser.add_argument("--reviews", action="store_true", help="查询商品评价")
    parser.add_argument("--keywords", action="store_true", help="查询流量词反查")
    parser.add_argument("--output", default="table", choices=["table", "json"],
                        help="输出格式: table, json")

    args = parser.parse_args()
    token = get_token(args.token)
    item_id = args.item_id
    product_id = args.product_id

    # 确定查询范围
    do_all = args.all
    do_info = do_all or not any([args.daily, args.monthly, args.reviews, args.keywords])
    do_daily = do_all or args.daily
    do_monthly = do_all or args.monthly
    do_reviews = do_all or args.reviews
    do_keywords = do_all or args.keywords

    # 构建公共参数
    params = {"itemId": item_id}
    if product_id:
        params["productId"] = product_id

    json_output = args.output == "json"

    if do_info:
        print(f"正在查询商品详情...", file=sys.stderr)
        resp = request_get("/item/info", token, params)
        check_response(resp)
        if json_output:
            print("=== 商品详情 ===")
            output_json(resp)
        else:
            print_item_info(resp.get("data", {}))

    if do_daily:
        print(f"\n正在查询每日数据...", file=sys.stderr)
        resp = request_get("/item/daily", token, params)
        check_response(resp)
        if json_output:
            print("=== 每日数据 ===")
            output_json(resp)
        else:
            print_daily_data(resp.get("data", []))

    if do_monthly:
        print(f"\n正在查询每月数据...", file=sys.stderr)
        resp = request_get("/item/monthly", token, params)
        check_response(resp)
        if json_output:
            print("=== 每月数据 ===")
            output_json(resp)
        else:
            print_monthly_data(resp.get("data", []))

    if do_reviews:
        print(f"\n正在查询商品评价...", file=sys.stderr)
        resp = request_get("/item/review", token, {"itemId": item_id, "pageNo": 1, "pageSize": 20})
        check_response(resp)
        review_data = resp.get("data", {})
        if json_output:
            print("=== 商品评价 ===")
            output_json(resp)
        else:
            reviews = review_data.get("reviewList", [])
            print(f"\n总评价数: {review_data.get('total', 0)}")
            print_reviews(reviews[:10])

    if do_keywords:
        print(f"\n正在查询流量词反查...", file=sys.stderr)
        resp = request_get("/item/keyword/reverse", token, {"itemId": item_id})
        check_response(resp)
        if json_output:
            print("=== 流量词反查 ===")
            output_json(resp)
        else:
            print_keywords(resp.get("data", {}))


if __name__ == "__main__":
    main()
