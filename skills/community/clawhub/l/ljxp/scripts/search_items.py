#!/usr/bin/env python3
"""
蓝鲸选品 - 商品查询脚本
调用 /items/search 接口进行多维度商品搜索。

用法:
  python search_items.py --token <YOUR_TOKEN> [选项]
  python search_items.py [选项]                         # 使用环境变量 LJXP_TOKEN

示例:
  python search_items.py --token abc123
  python search_items.py --token abc123 --site MLB --seller-type LOCAL --price-begin 100 --price-end 500
  python search_items.py --token abc123 --title "phone case" --sort-key sale30 --sort-order desc
  LJXP_TOKEN=abc123 python search_items.py --site MLM
"""

import argparse
import sys
import os

# 将父目录加入 sys.path 以支持直接运行
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    get_token, request_post, check_response, output_json, output_html,
    print_page_info, print_item_brief, SITE_NAMES, VALID_SITES
)

# 枚举值
VALID_SORT_KEYS = ["sale7", "sale30", "saleTotal", "amount30"]
VALID_SORT_ORDERS = ["asc", "desc"]
VALID_STORAGE_TYPES = ["FULL", "CBT,LOCAL"]
VALID_SELLER_TYPES = ["LOCAL", "CBT"]
VALID_ITEM_STATUSES = ["active", "paused"]
VALID_START_TIME = [15, 30, 60, 90, 180, 365]


def build_request_body(args):
    """根据命令行参数构建请求体"""
    body = {
        "pageNo": args.page_no,
        "pageSize": args.page_size,
        "siteId": args.site,
        "sellerId": args.seller_id,
        "title": args.title,
        "categoryId": args.category_id,
        "storageType": args.storage_type,
        "sellerType": args.seller_type,
        "follow": args.follow,
        "startTimeAdded": args.start_time_added,
        "startTimeBegin": args.start_time_begin,
        "startTimeEnd": args.start_time_end,
        "isUsaFull": args.is_usa_full,
        "priceBegin": args.price_begin,
        "priceEnd": args.price_end,
        "commentBegin": args.comment_begin,
        "commentEnd": args.comment_end,
        "soldTotalBegin": args.sold_total_begin,
        "soldTotalEnd": args.sold_total_end,
        "sale30Start": args.sale30_start,
        "sale30End": args.sale30_end,
        "weightStart": args.weight_start,
        "weightEnd": args.weight_end,
        "scoreStart": args.score_start,
        "scoreEnd": args.score_end,
        "sale30RangeStart": args.sale30_range_start,
        "sale30RangeEnd": args.sale30_range_end,
        "itemStatus": args.item_status,
        "sortKey": args.sort_key,
        "sortOrder": args.sort_order,
    }
    return body


def main():
    parser = argparse.ArgumentParser(
        description="蓝鲸选品 - 商品查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --token YOUR_TOKEN --site MLM
  %(prog)s --token YOUR_TOKEN --title "phone case" --sort-key sale30 --sort-order desc
  %(prog)s --token YOUR_TOKEN --site MLB --price-begin 100 --price-end 500
  %(prog)s --token YOUR_TOKEN --site MLM --seller-type LOCAL --storage-type FULL

Token 也可通过环境变量 LJXP_TOKEN 传入，无需每次敲 --token。
        """
    )

    # 必填参数
    parser.add_argument("--token", default=None, help="Authorization Token (也可通过环境变量 LJXP_TOKEN 传入)。⚠️ [不推荐] 会暴露在 shell 历史/进程列表；优先使用环境变量 LJXP_TOKEN")

    # 分页参数
    parser.add_argument("--page-no", type=int, default=1, help="当前页码 (默认: 1)")
    parser.add_argument("--page-size", type=int, default=50, help="每页条数 (默认: 50)")

    # 站点
    parser.add_argument("--site", default="MLM", choices=VALID_SITES,
                        help="站点: MLM(墨西哥), MLB(巴西), MLC(智利), MLA(阿根廷), MCO(哥伦比亚)")

    # 搜索条件
    parser.add_argument("--seller-id", default=None, help="店铺ID")
    parser.add_argument("--title", default=None, help="商品标题关键词")
    parser.add_argument("--category-id", default=None, help="类目ID，如 MLM458037")
    parser.add_argument("--storage-type", default=None, choices=VALID_STORAGE_TYPES,
                        help="仓储类型: FULL(自发货), CBT,LOCAL")
    parser.add_argument("--seller-type", default=None, choices=VALID_SELLER_TYPES,
                        help="店铺类型: LOCAL(本土店), CBT(跨境店)")
    parser.add_argument("--follow", type=int, default=None, choices=[0, 1],
                        help="是否跟卖: 0(否), 1(是)")
    parser.add_argument("--is-usa-full", type=lambda x: x.lower() == 'true', default=False,
                        help="是否美国转运仓 (默认: false)")

    # 上架时间
    parser.add_argument("--start-time-added", type=int, default=None, choices=VALID_START_TIME,
                        help="上架时间范围: 15/30/60/90/180/365 天")
    parser.add_argument("--start-time-begin", default=None, help="上架时间开始，如 2026-03-01")
    parser.add_argument("--start-time-end", default=None, help="上架时间结束，如 2026-03-24")

    # 价格范围
    parser.add_argument("--price-begin", type=int, default=None, help="最低价格")
    parser.add_argument("--price-end", type=int, default=None, help="最高价格")

    # 评论范围
    parser.add_argument("--comment-begin", type=int, default=None, help="最低评论数")
    parser.add_argument("--comment-end", type=int, default=None, help="最高评论数")

    # 销量范围
    parser.add_argument("--sold-total-begin", type=int, default=None, help="最低总销量")
    parser.add_argument("--sold-total-end", type=int, default=None, help="最高总销量")
    parser.add_argument("--sale30-start", type=int, default=None, help="最低30天销量")
    parser.add_argument("--sale30-end", type=int, default=None, help="最高30天销量")
    parser.add_argument("--sale30-range-start", type=int, default=None, help="最低30天销量环比")
    parser.add_argument("--sale30-range-end", type=int, default=None, help="最高30天销量环比")

    # 重量范围
    parser.add_argument("--weight-start", type=int, default=None, help="最低商品重量(g)")
    parser.add_argument("--weight-end", type=int, default=None, help="最高商品重量(g)")

    # 评分范围
    parser.add_argument("--score-start", type=float, default=None, help="最低评分")
    parser.add_argument("--score-end", type=float, default=None, help="最高评分")

    # 商品状态
    parser.add_argument("--item-status", default=None, choices=VALID_ITEM_STATUSES,
                        help="商品状态: active(活跃), paused(暂停)")

    # 排序
    parser.add_argument("--sort-key", default=None, choices=VALID_SORT_KEYS,
                        help="排序字段: sale7, sale30, saleTotal, amount30")
    parser.add_argument("--sort-order", default=None, choices=VALID_SORT_ORDERS,
                        help="排序方向: asc(升序), desc(降序)")

    # 输出格式
    parser.add_argument("--output", default="table", choices=["table", "json", "html"],
                        help="输出格式: table(表格), json(原始JSON), html(浏览器界面)")

    args = parser.parse_args()

    # 获取 Token
    token = get_token(args.token)

    # 构建请求体
    body = build_request_body(args)

    # 发送请求
    print(f"正在查询 {SITE_NAMES.get(args.site, args.site)} 站点商品...", file=sys.stderr)
    response = request_post("/items/search", token, body)
    check_response(response)

    # 输出结果
    if args.output == "json":
        output_json(response)
    elif args.output == "html":
        output_html(response, body)
    else:
        data = response.get("data", {})
        items = data.get("data", []) if isinstance(data, dict) else []
        print_page_info(data, "商品搜索结果")
        if not items:
            print("未找到符合条件的商品")
        else:
            for i, item in enumerate(items, 1):
                print_item_brief(item, i)


if __name__ == "__main__":
    main()
