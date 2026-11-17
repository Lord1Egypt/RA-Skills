#!/usr/bin/env python3
"""
蓝鲸选品 - 目录链接查询脚本
调用 /catalogs/search, /catalog/info, /catalog/daily 接口。

用法:
  python catalog_search.py --token <TOKEN> --site MLM                          # 搜索目录链接
  python catalog_search.py --token <TOKEN> --product-id <ID>                    # 目录详情
  python catalog_search.py --token <TOKEN> --product-id <ID> --daily            # 目录每日数据
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    get_token, request_post, request_get, check_response, output_json, output_html,
    print_page_info, print_item_brief, SITE_NAMES, VALID_SITES
)


def print_catalog_info(data):
    """打印目录链接详情"""
    print(f"\n{'='*60}")
    print(f"产品ID:      {data.get('productId', 'N/A')}")
    print(f"名称:        {data.get('name', 'N/A')}")
    print(f"站点:        {data.get('siteId', 'N/A')}")
    print(f"类目ID:      {data.get('categoryId', 'N/A')}")
    print(f"状态:        {data.get('status', 'N/A')}")
    print(f"总销量:      {data.get('soldQuantity', 'N/A')}")
    print(f"关注数:      {data.get('followCount', 'N/A')}")
    print(f"创建时间:    {data.get('dateCreated', 'N/A')}")
    print(f"{'='*60}")

    # 图片
    pics = data.get("pictures", [])
    if pics:
        print(f"\n--- 图片 ({len(pics)}张) ---")
        for p in pics[:5]:
            print(f"  {p.get('url', '')}")

    # 跟卖商品
    follow_items = data.get("followItems", [])
    if follow_items:
        print(f"\n--- 跟卖商品 ({len(follow_items)}个) ---")
        for i, fi in enumerate(follow_items, 1):
            print(f"\n  [{i}] ID: {fi.get('id','')} | 卖家: {fi.get('sellerName','')} "
                  f"| 价格: {fi.get('price','')} | 7天销量: {fi.get('sale7','')} "
                  f"| 30天销量: {fi.get('sale30d','')} | 库存: {fi.get('availableQuantity','')}")

    print(f"\n链接: {data.get('permalink', 'N/A')}")


def print_catalog_daily(items):
    """打印目录每日数据"""
    print(f"\n{'='*60}")
    print(f"{'日期':<12} {'BSR':>8} {'销量':>8} {'价格':>10}")
    print(f"{'-'*60}")
    for d in items:
        print(f"{d.get('date',''):<12} {d.get('bsr',''):>8} {d.get('soldQuantity',''):>8} {d.get('price',''):>10}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 目录链接查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --token YOUR_TOKEN --site MLM
  %(prog)s --token YOUR_TOKEN --site MLM --search-text "phone" --page-size 20
  %(prog)s --token YOUR_TOKEN --product-id PROD123456
  %(prog)s --token YOUR_TOKEN --product-id PROD123456 --daily
        """
    )
    parser.add_argument("--token", default=None, help="Authorization Token。⚠️ [不推荐] 会暴露在 shell 历史/进程列表/共享终端日志；优先使用环境变量 LJXP_TOKEN 传入")

    # 搜索模式
    parser.add_argument("--site", default=None, choices=VALID_SITES, help="站点")
    parser.add_argument("--search-text", default=None, help="搜索文本")
    parser.add_argument("--category-id", default=None, help="类目ID")
    parser.add_argument("--seller-id", default=None, help="店铺ID")
    parser.add_argument("--sku-id", default=None, help="SKU ID")
    parser.add_argument("--bland", default=None, help="品牌名称")
    parser.add_argument("--month", default=None, help="查询月份，格式 YYYYMM")
    parser.add_argument("--sort-key", default=None, help="排序字段")
    parser.add_argument("--sort-order", default=None, choices=["asc", "desc"], help="排序方向")
    parser.add_argument("--page-no", type=int, default=1, help="页码")
    parser.add_argument("--page-size", type=int, default=50, help="每页条数")

    # 详情模式
    parser.add_argument("--product-id", default=None, help="目录链接ID（进入详情模式）")
    parser.add_argument("--daily", action="store_true", help="查询目录每日数据（需 --product-id）")

    parser.add_argument("--output", default="table", choices=["table", "json", "html"], help="输出格式: table, json, html")

    args = parser.parse_args()
    token = get_token(args.token)

    json_output = args.output == "json"
    html_output = args.output == "html"

    # 详情/每日模式
    if args.product_id:
        if args.daily:
            print(f"正在查询目录每日数据...", file=sys.stderr)
            resp = request_get("/catalog/daily", token, {"productId": args.product_id})
            check_response(resp)
            if json_output:
                output_json(resp)
            else:
                print_catalog_daily(resp.get("data", []))
        else:
            print(f"正在查询目录链接详情...", file=sys.stderr)
            resp = request_get("/catalog/info", token, {"productId": args.product_id})
            check_response(resp)
            if json_output:
                output_json(resp)
            else:
                print_catalog_info(resp.get("data", {}))
        return

    # 搜索模式
    if not args.site:
        print("错误: 搜索模式需要 --site 参数", file=sys.stderr)
        sys.exit(1)

    body = {
        "siteId": args.site,
        "pageNo": args.page_no,
        "pageSize": args.page_size,
        "searchText": args.search_text,
        "categoryId": args.category_id,
        "sellerId": args.seller_id,
        "skuId": args.sku_id,
        "bland": args.bland,
        "month": args.month,
        "sortKey": args.sort_key,
        "sortOrder": args.sort_order,
    }

    print(f"正在搜索 {SITE_NAMES.get(args.site, args.site)} 目录链接...", file=sys.stderr)
    response = request_post("/catalogs/search", token, body)
    check_response(response)

    if json_output:
        output_json(response)
    elif html_output:
        output_html(response, body)
    else:
        data = response.get("data", {})
        items = data.get("data", []) if isinstance(data, dict) else []
        print_page_info(data, "目录链接搜索结果")
        if not items:
            print("未找到符合条件的目录链接")
        else:
            for i, item in enumerate(items, 1):
                print_item_brief(item, i)

    # 提示关联操作
    data_resp = response.get("data", {})
    items_list = data_resp.get("data", []) if isinstance(data_resp, dict) else []
    if items_list and not json_output:
        first_product_id = items_list[0].get("productId")
        if first_product_id:
            print(f"\n💡 提示: 获取 productId 后，可查看目录详情:")
            print(f"   python catalog_search.py --token <TOKEN> --product-id {first_product_id}")


if __name__ == "__main__":
    main()
