#!/usr/bin/env python3
"""
蓝鲸选品 - 热搜词查询脚本
调用 /keywords/search 接口查询 Mercado Libre 热搜关键词。

用法:
  python search_keywords.py --token <TOKEN> --site MLM --search-type month --run-date 2026-08-01
  python search_keywords.py --token <TOKEN> --site MLB --search-type day --run-date 2026-08-01 --category-id MLB1234

示例:
  python search_keywords.py --token abc123 --site MLM --search-type month --run-date 2026-08-01
  python search_keywords.py --token abc123 --site MLM --search-type day --run-date 2026-08-01 --search-text "phone"
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    get_token, request_post, check_response, output_json, print_keyword_brief,
    SITE_NAMES, VALID_SITES
)

VALID_SEARCH_TYPES = ["month", "day"]


def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 热搜词查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --token YOUR_TOKEN --site MLM --search-type month --run-date 2026-08-01
  %(prog)s --token YOUR_TOKEN --site MLB --search-type day --run-date 2026-08-01
  %(prog)s --token YOUR_TOKEN --site MLM --search-type month --run-date 2026-08-01 --search-text "phone case"

查询类型:
  month - 按月查询热搜词
  day   - 按日查询热搜词
        """
    )
    parser.add_argument("--token", default=None, help="Authorization Token。⚠️ [不推荐] 会暴露在 shell 历史/进程列表；优先使用环境变量 LJXP_TOKEN")
    parser.add_argument("--site", default="MLM", choices=VALID_SITES, help="站点")
    parser.add_argument("--search-type", required=True, choices=VALID_SEARCH_TYPES,
                        help="查询类型: month(按月), day(按日)")
    parser.add_argument("--run-date", required=True, help="日期，如 2026-08-01")
    parser.add_argument("--category-id", default=None, help="类目ID筛选")
    parser.add_argument("--search-text", default=None, help="搜索词")
    parser.add_argument("--key-search", default=None, help="关键词搜索")
    parser.add_argument("--run-week", default=None, help="周")
    parser.add_argument("--run-month", default=None, help="月份")
    parser.add_argument("--sort-key", default=None, help="排序字段: sale30/visit30/totalItem/adCount")
    parser.add_argument("--sort-order", default=None, choices=["asc", "desc"], help="排序方向")
    parser.add_argument("--page-no", type=int, default=1, help="页码")
    parser.add_argument("--page-size", type=int, default=50, help="每页条数")
    parser.add_argument("--output", default="table", choices=["table", "json"],
                        help="输出格式: table, json")

    args = parser.parse_args()
    token = get_token(args.token)

    body = {
        "siteId": args.site,
        "searchType": args.search_type,
        "runDate": args.run_date,
        "searchText": args.search_text,
        "keySearch": args.key_search,
        "categoryId": args.category_id,
        "runWeek": args.run_week,
        "runMonth": args.run_month,
        "pageNo": args.page_no,
        "pageSize": args.page_size,
    }

    if args.sort_key:
        body["sort"] = {"key": args.sort_key, "order": args.sort_order or "desc"}

    print(f"正在查询 {SITE_NAMES.get(args.site, args.site)} 热搜词 "
          f"({args.search_type}: {args.run_date})...", file=sys.stderr)

    response = request_post("/keywords/search", token, body, timeout=120)
    check_response(response)

    if args.output == "json":
        output_json(response)
    else:
        data = response.get("data", {})
        result_list = data.get("resultList", [])
        total = data.get("total", 0)
        total_more = data.get("totalMore", "")

        total_str = f"总数: {total}"
        if total_more:
            total_str += f" ({total_more})"
        print(f"\n=== 热搜词结果 === {total_str}")
        print(f"{'='*80}")

        if not result_list:
            print("未找到热搜词")
        else:
            for i, kw in enumerate(result_list, 1):
                print_keyword_brief(kw, i)

    # 提示关联操作
    result_list = response.get("data", {}).get("resultList", [])
    if result_list and args.output != "json":
        first_key = result_list[0].get("key")
        if first_key:
            print(f"\n💡 提示: 获取热搜词后，可搜索该关键词对应的商品:")
            print(f"   python search_items.py --token <TOKEN> --site {args.site} --title \"{first_key}\" --sort-key sale30 --sort-order desc")


if __name__ == "__main__":
    main()
