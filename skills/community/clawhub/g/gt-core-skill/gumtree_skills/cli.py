"""gumtree-skills MVP CLI entrypoint."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from scripts.gumtree.errors import BridgeError, BrowserAutomationError, GumtreeError

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def _output(data: dict[str, Any], exit_code: int = 0) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def cmd_search(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_search import run_browser_search
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_search(
        page=page,
        keyword=args.keyword,
        limit=args.limit,
        search_location=args.search_location,
        search_category=args.search_category,
        sort=args.sort,
        distance=args.distance,
        min_price=args.min_price,
        max_price=args.max_price,
        conditions=args.condition,
        seller_types=args.seller_type,
        mobile_storage_capacity=args.mobile_storage_capacity,
        common_for_sale_colour=args.common_for_sale_colour,
        mobile_model_apple=args.mobile_model_apple,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_check_login(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_auth import run_browser_check_login
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_check_login(page=page)
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_login(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_auth import run_browser_login
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_login(page=page, username=args.username, password=args.password)
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_logout(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_auth import run_browser_logout
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_logout(page=page)
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_home_recommend(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_home import run_browser_home_recommendations
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_home_recommendations(
        page=page,
        limit=args.limit,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_favourites(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_favourites import run_browser_favourites
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_favourites(
        page=page,
        limit=args.limit,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_detail(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_detail import run_browser_detail
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_detail(
        page=page,
        detail_url=args.url,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_detail_favourite(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_detail_favourite import run_browser_detail_favourite
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_detail_favourite(
        page=page,
        detail_url=args.url,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_post_ad(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_post_ad import run_browser_post_ad_category
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_post_ad_category(
        page=page,
        keyword=args.keyword,
        category_name=args.category_name,
        category_index=args.category_index,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_messages(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_messages import run_browser_messages
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_messages(
        page=page,
        conversation_id=args.conversation_id,
        message=args.message,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def cmd_detail_message(args: argparse.Namespace) -> None:
    from scripts.gumtree.browser_messages import run_browser_detail_message
    from scripts.gumtree.bridge import BridgePage, ensure_bridge_ready

    ensure_bridge_ready()
    page = BridgePage()
    result = run_browser_detail_message(
        page=page,
        detail_url=args.url,
        message=args.message,
    )
    _output(result, exit_code=0 if result.get("ok") else 2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="gumtree-skills MVP CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sub = subparsers.add_parser("check-login", help="检查 Gumtree 当前登录状态")
    sub.set_defaults(func=cmd_check_login)

    sub = subparsers.add_parser("login", help="通过邮箱和密码登录 Gumtree")
    sub.add_argument("--username", required=True, help="Gumtree 登录邮箱")
    sub.add_argument("--password", required=True, help="Gumtree 登录密码")
    sub.set_defaults(func=cmd_login)

    sub = subparsers.add_parser("logout", help="退出 Gumtree 当前登录状态")
    sub.set_defaults(func=cmd_logout)

    sub = subparsers.add_parser("search", help="通过浏览器扩展搜索 Gumtree 内容")
    sub.add_argument("--keyword", required=True)
    sub.add_argument("--limit", type=int, default=10)
    sub.add_argument("--search-location", default="uk")
    sub.add_argument("--search-category", default="all")
    sub.add_argument(
        "--sort",
        choices=["relevance", "date", "price_lowest_first", "price_highest_first", "distance"],
        help="排序方式：相关性、时间、价格低到高、价格高到低或距离优先",
    )
    sub.add_argument("--distance", type=int, help="搜索半径，单位按 Gumtree 页面参数解释")
    sub.add_argument("--min-price", type=int)
    sub.add_argument("--max-price", type=int)
    sub.add_argument(
        "--condition",
        action="append",
        choices=["as_good_as_new", "good", "new", "fair"],
        help="物品成色筛选；可重复传入，例如 --condition good --condition new",
    )
    sub.add_argument(
        "--seller-type",
        action="append",
        choices=["trade", "private"],
        help="卖家类型筛选；可重复传入，例如 --seller-type trade --seller-type private",
    )
    sub.add_argument("--mobile-storage-capacity")
    sub.add_argument("--common-for-sale-colour")
    sub.add_argument("--mobile-model-apple")
    sub.set_defaults(func=cmd_search)

    sub = subparsers.add_parser("home-recommend", help="提取 Gumtree 首页推荐内容")
    sub.add_argument("--limit", type=int, default=10)
    sub.set_defaults(func=cmd_home_recommend)

    sub = subparsers.add_parser("favourites", help="提取 Gumtree 收藏内容")
    sub.add_argument("--limit", type=int, default=10)
    sub.set_defaults(func=cmd_favourites)

    sub = subparsers.add_parser("detail", help="提取 Gumtree 详情页内容")
    sub.add_argument("--url", required=True)
    sub.set_defaults(func=cmd_detail)

    sub = subparsers.add_parser("detail-favourite", help="收藏 Gumtree 详情页")
    sub.add_argument("--url", required=True)
    sub.set_defaults(func=cmd_detail_favourite)

    sub = subparsers.add_parser("messages", help="查看 Gumtree 站内交流页并可发送消息")
    sub.add_argument("--conversation-id", default=None, help="可选，会话 ID")
    sub.add_argument("--message", default=None, help="可选，要发送的消息内容")
    sub.set_defaults(func=cmd_messages)

    sub = subparsers.add_parser("detail-message", help="从 Gumtree 详情页点击 Message 并进入站内交流页")
    sub.add_argument("--url", required=True)
    sub.add_argument("--message", default=None, help="可选，要发送的消息内容")
    sub.set_defaults(func=cmd_detail_message)

    sub = subparsers.add_parser("post-ad", help="发布二手物品（选择类目）")
    sub.add_argument("--keyword", required=True, help="物品关键词，如 iPhone, Sofa")
    sub.add_argument("--category-name", default=None, help="目标类目名称，模糊匹配建议列表")
    sub.add_argument("--category-index", type=int, default=None, help="目标类目索引（0 起）")
    sub.set_defaults(func=cmd_post_ad)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (GumtreeError, BridgeError, BrowserAutomationError) as exc:
        _output({"ok": False, "error": str(exc)}, exit_code=2)
    except Exception as exc:  # pragma: no cover
        _output({"ok": False, "error": f"未知错误: {exc}"}, exit_code=2)


if __name__ == "__main__":
    main()
