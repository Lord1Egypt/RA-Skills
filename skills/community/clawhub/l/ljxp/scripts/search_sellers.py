#!/usr/bin/env python3
"""
蓝鲸选品 - 店铺查询脚本
调用 /seller/search 接口筛选 Mercado Libre 店铺。

用法:
  python search_sellers.py --token <TOKEN> --site MLM --seller-type LOCAL --level-id 5_green --power-type platinum
  python search_sellers.py --token <TOKEN> --site MLB --seller-type CBT --level-id 3_yellow --power-type gold

示例:
  python search_sellers.py --token abc123 --site MLM --seller-type LOCAL --level-id 5_green --power-type platinum
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    get_token, request_post, check_response, output_json,
    print_page_info, print_seller_brief, SITE_NAMES, VALID_SITES
)

VALID_SELLER_TYPES = ["LOCAL", "CBT", "CBT_OTHER", "CBT_FBM"]
VALID_LEVELS = ["5_green", "4_light_green", "3_yellow"]
VALID_POWER_TYPES = ["platinum", "gold", "silver"]


def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 店铺查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
店铺类型:
  LOCAL    - 本土店
  CBT      - 跨境店
  CBT_OTHER - CBT remote店
  CBT_FBM  - CBT full店铺

店铺等级:
  5_green       - 绿（优秀）
  4_light_green - 浅绿（良好）
  3_yellow      - 黄（一般）

店铺级别:
  platinum - 铂金
  gold     - 黄金
  silver   - 白银
        """
    )
    parser.add_argument("--token", default=None, help="Authorization Token。⚠️ [不推荐] 会暴露在 shell 历史/进程列表；优先使用环境变量 LJXP_TOKEN")
    parser.add_argument("--page-no", type=int, default=1, help="页码 (默认: 1)")
    parser.add_argument("--page-size", type=int, default=50, help="每页条数 (默认: 50)")
    parser.add_argument("--site", default="MLM", choices=VALID_SITES, help="站点")
    parser.add_argument("--seller-type", default="LOCAL", choices=VALID_SELLER_TYPES,
                        help="店铺类型 (默认: LOCAL)")
    parser.add_argument("--level-id", default="5_green", choices=VALID_LEVELS,
                        help="店铺等级 (默认: 5_green)")
    parser.add_argument("--power-type", default="platinum", choices=VALID_POWER_TYPES,
                        help="店铺级别 (默认: platinum)")
    parser.add_argument("--output", default="table", choices=["table", "json"],
                        help="输出格式: table, json")

    args = parser.parse_args()
    token = get_token(args.token)

    body = {
        "pageNo": args.page_no,
        "pageSize": args.page_size,
        "siteId": args.site,
        "sellerType": args.seller_type,
        "levelId": args.level_id,
        "powerType": args.power_type,
    }

    print(f"正在查询 {SITE_NAMES.get(args.site, args.site)} "
          f"{args.seller_type} {args.power_type} 店铺...", file=sys.stderr)

    response = request_post("/seller/search", token, body)
    check_response(response)

    if args.output == "json":
        output_json(response)
    else:
        data = response.get("data", {})
        sellers = data.get("data", []) if isinstance(data, dict) else []
        print_page_info(data, "店铺搜索结果")
        if not sellers:
            print("未找到符合条件的店铺")
        else:
            for i, seller in enumerate(sellers, 1):
                print_seller_brief(seller, i)

    # 提示关联操作
    sellers_data = response.get("data", {})
    seller_list = sellers_data.get("data", []) if isinstance(sellers_data, dict) else []
    if seller_list and args.output != "json":
        first_id = seller_list[0].get("id")
        if first_id:
            print(f"\n💡 提示: 获取店铺ID后，可搜索该店铺商品:")
            print(f"   python search_items.py --token <TOKEN> --site {args.site} --seller-id {first_id}")


if __name__ == "__main__":
    main()
