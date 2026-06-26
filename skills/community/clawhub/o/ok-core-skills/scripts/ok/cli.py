#!/usr/bin/env python3
"""OK.com CLI — unified command-line entry point.

All subcommands output JSON to stdout; logs go to stderr.

Usage (from any directory):
    uv run --project <skill-dir> ok-cli <subcommand> [args]
    # or (from project root):
    uv run ok-cli <subcommand> [args]
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict

from ok.client.factory import get_client
from ok.errors import OKError


def _output(data, exit_code: int = 0):
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def _error(message: str, exit_code: int = 2):
    _output({"error": message}, exit_code)


# ─── subcommand handlers ────────────────────────────────────────────────────


def cmd_list_countries(args):
    from ok.locale import list_countries
    _output({"countries": list_countries()})


def cmd_list_cities(args):
    from ok.locale import fetch_all_cities, fetch_cities, search_cities

    mode = getattr(args, "mode", "api")
    if mode == "search" and hasattr(args, "keyword"):
        cities = search_cities(args.country, args.keyword, args.lang)
    elif mode == "all":
        cities = fetch_all_cities(args.country, lang=args.lang)
    else:
        cities = fetch_cities(args.country, args.lang)

    _output({
        "country": args.country,
        "mode": mode,
        "total": len(cities),
        "cities": [{"name": c.name, "code": c.code, "local_id": c.local_id} for c in cities],
    })


def cmd_list_categories(args):
    from ok.locale import fetch_categories

    def cat_to_dict(cat):
        d = {"name": cat.name, "code": cat.code, "category_id": cat.category_id}
        if cat.children:
            d["children"] = [cat_to_dict(c) for c in cat.children]
        return d

    categories = fetch_categories(args.country, args.lang)
    _output({
        "country": args.country,
        "total": len(categories),
        "categories": [cat_to_dict(c) for c in categories],
    })


def cmd_set_locale(args):
    client = get_client()
    mode = getattr(args, "mode", "api")

    if mode == "human":
        from ok.locale_human import switch_city_via_ui
        result = switch_city_via_ui(client, args.city)
        _output({
            "mode": "human",
            "success": result.success,
            "elapsed_seconds": result.elapsed_seconds,
            "locale": asdict(result.final_locale) if result.final_locale else None,
            "url": result.final_url,
            "error": result.error,
        })
    else:
        from ok.locale import navigate_to_locale
        locale = navigate_to_locale(client, args.country, args.city, args.lang)
        _output({"mode": "api", "locale": asdict(locale), "url": locale.base_url()})


def cmd_search_cities(args):
    from ok.locale import search_cities
    cities = search_cities(args.country, args.keyword, args.lang)
    _output({
        "country": args.country,
        "keyword": args.keyword,
        "total": len(cities),
        "cities": [{"name": c.name, "code": c.code, "local_id": c.local_id} for c in cities],
    })


def cmd_get_locale(args):
    client = get_client()
    from ok.locale import get_current_locale
    locale = get_current_locale(client)
    if locale:
        _output({"locale": asdict(locale), "url": locale.base_url()})
    else:
        _output({"locale": None, "message": "当前页面非 ok.com"})


def cmd_search(args):
    client = get_client()
    from ok.search import search_listings
    result = search_listings(
        client,
        keyword=args.keyword,
        country=args.country,
        city=args.city,
        lang=args.lang,
        max_results=args.max_results,
        price_min=args.price_min,
        price_max=args.price_max,
    )
    out = {
        "keyword": result.keyword,
        "total": result.total_count,
        "listings": [asdict(item) for item in result.listings],
    }
    if args.price_min is not None or args.price_max is not None:
        out["price_filter"] = {"min": args.price_min, "max": args.price_max}
    _output(out)


def cmd_list_feeds(args):
    client = get_client()
    from ok.feeds import list_feeds
    listings = list_feeds(
        client,
        country=args.country,
        city=args.city,
        lang=args.lang,
        max_results=args.max_results,
    )
    _output({
        "total": len(listings),
        "listings": [asdict(item) for item in listings],
    })


def cmd_get_listing(args):
    client = get_client()
    from ok.listing_detail import get_listing_detail
    detail = get_listing_detail(client, args.url)
    _output(asdict(detail))


def cmd_browse_category(args):
    client = get_client()
    from ok.categories import browse_category
    listings = browse_category(
        client,
        category_code=args.category,
        country=args.country,
        city=args.city,
        lang=args.lang,
        max_results=args.max_results,
        price_min=args.price_min,
        price_max=args.price_max,
    )
    out = {
        "category": args.category,
        "total": len(listings),
        "listings": [asdict(item) for item in listings],
    }
    if args.price_min is not None or args.price_max is not None:
        out["price_filter"] = {"min": args.price_min, "max": args.price_max}
    _output(out)


def cmd_full_search(args):
    if not args.category and not args.keyword:
        _error("--category 和 --keyword 至少需要提供一个")

    client = get_client()
    from ok.full_search import full_search_flow

    result = full_search_flow(
        client,
        country=args.country,
        city_keyword=args.city,
        category=args.category,
        keyword=args.keyword,
        lang=args.lang,
        max_results=args.max_results,
        price_min=args.price_min,
        price_max=args.price_max,
    )

    out = {
        "flow": result.flow,
        "steps": [
            {
                "step": s.step,
                "success": s.success,
                **({"error": s.error} if s.error else {}),
                **{k: v for k, v in s.detail.items() if k != "raw_listings"},
            }
            for s in result.steps
        ],
        "total": result.total,
        "listings": [asdict(item) for item in result.listings],
        "final_url": result.final_url,
    }
    if args.price_min is not None or args.price_max is not None:
        out["price_filter"] = {"min": args.price_min, "max": args.price_max}
    _output(out)


# def cmd_check_login(args):
#     client = get_client()

#     url = client.get_url()
#     if "ok.com" not in url:
#         from ok.urls import build_base_url
#         client.navigate(build_base_url("sg", "en", "singapore"))
#         client.wait_dom_stable()

#     from ok.login import check_login
#     status = check_login(client)
#     _output(status)

def _ensure_on_ok(client, country="singapore", lang="en"):
    """确保浏览器在 ok.com 页面上"""
    url = client.get_url()
    if "ok.com" not in url:
        from ok.urls import build_base_url
        try:
            from ok.locale import get_country_info
            info = get_country_info(country)
            subdomain = info["subdomain"]
        except Exception:
            subdomain = "sg"
        client.navigate(build_base_url(subdomain, lang, country))
    client.wait_dom_stable()


def _ensure_city_home_for_auth(client, country="singapore", lang="en"):
    """登录/鉴权需要标准城市壳页面；/yun/ 等路径无顶栏登录入口，必须跳转。"""
    from ok.urls import build_base_url, is_city_shell_url

    try:
        from ok.locale import get_country_info

        info = get_country_info(country)
        subdomain = info["subdomain"]
    except Exception:
        subdomain = "sg"
    target = build_base_url(subdomain, lang, country)
    url = client.get_url() or ""
    if not is_city_shell_url(url):
        client.navigate(target)
    client.wait_dom_stable()


def cmd_check_login(args):
    """检查登录状态"""
    client = get_client()
    subdomain = getattr(args, "subdomain", None)

    if subdomain:
        from ok.login import check_login
        status = check_login(client, subdomain=subdomain)
    else:
        _ensure_city_home_for_auth(client, getattr(args, "country", "singapore"))
        from ok.login import check_login
        status = check_login(client)

    _output(status)


def cmd_login(args):
    """通过邮箱密码登录"""
    client = get_client()
    subdomain = getattr(args, "subdomain", None)

    if subdomain:
        from ok.urls import build_base_url
        target = build_base_url(subdomain, "en")
        if f"{subdomain}.ok.com" not in (client.get_url() or ""):
            client.navigate(target)
            client.wait_dom_stable()
    else:
        _ensure_city_home_for_auth(client, getattr(args, "country", "singapore"))

    from ok.login import login_with_email
    result = login_with_email(
        client, args.email, args.password,
        probe_subdomains=[] if subdomain else ["ae", "uk", "au"],
    )
    exit_code = 0 if result.get("logged_in") else 2
    _output(result, exit_code)


def cmd_wait_login(args):
    """等待用户手动完成登录（OAuth 等）"""
    client = get_client()
    subdomain = getattr(args, "subdomain", None)

    if subdomain:
        from ok.urls import build_base_url
        target = build_base_url(subdomain, "en")
        if f"{subdomain}.ok.com" not in (client.get_url() or ""):
            client.navigate(target)
            client.wait_dom_stable()
    else:
        _ensure_city_home_for_auth(client, getattr(args, "country", "singapore"))

    from ok.login import wait_for_login
    result = wait_for_login(client, timeout=args.timeout)
    exit_code = 0 if result.get("logged_in") else 2
    _output(result, exit_code)


def cmd_list_favorites(args):
    """列出收藏列表"""
    client = get_client()
    from ok.favorites import list_favorites
    result = list_favorites(
        client,
        subdomain=args.subdomain,
        lang=args.lang,
        max_results=args.max_results,
    )
    _output({
        "total": result.total,
        "url": result.url,
        "items": [asdict(item) for item in result.items],
    })


def cmd_add_favorite(args):
    """收藏帖子"""
    client = get_client()
    from ok.favorites import add_favorite
    result = add_favorite(client, args.url)
    _output(result)


def cmd_remove_favorite(args):
    """取消收藏帖子"""
    client = get_client()
    if args.index is not None:
        from ok.favorites import remove_favorite_from_list
        result = remove_favorite_from_list(
            client, subdomain=args.subdomain, index=args.index,
        )
    elif args.url:
        from ok.favorites import remove_favorite
        result = remove_favorite(client, args.url)
    else:
        _error("需要 --url 或 --index 参数")
        return
    _output(result)


def cmd_list_my_posts(args):
    """列出我的帖子"""
    client = get_client()
    from ok.my_posts import list_my_posts
    result = list_my_posts(
        client,
        subdomain=args.subdomain,
        lang=args.lang,
        state=args.state,
        max_results=args.max_results,
    )
    _output({
        "total": result.total,
        "state": result.state,
        "url": result.url,
        "items": [asdict(item) for item in result.items],
    })


def cmd_delete_post(args):
    """删除我的帖子"""
    client = get_client()
    from ok.my_posts import delete_post
    result = delete_post(
        client,
        subdomain=args.subdomain,
        lang=args.lang,
        index=args.index,
    )
    _output(result)


def cmd_edit_post(args):
    """获取帖子编辑链接"""
    client = get_client()
    from ok.my_posts import get_edit_url
    result = get_edit_url(
        client,
        subdomain=args.subdomain,
        lang=args.lang,
        index=args.index,
    )
    _output(result)


# ─── argument parser ────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OK.com 自动化 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    sub.add_parser("list-countries", help="列出支持的国家")

    p = sub.add_parser("list-cities", help="动态获取指定国家的城市列表")
    p.add_argument("--country", required=True)
    p.add_argument("--lang", default="en")
    p.add_argument("--mode", choices=["api", "search", "all"], default="api")
    p.add_argument("--keyword", default="")

    p = sub.add_parser("search-cities", help="通过搜索接口匹配城市")
    p.add_argument("--country", required=True)
    p.add_argument("--keyword", required=True)
    p.add_argument("--lang", default="en")

    p = sub.add_parser("list-categories", help="动态获取分类树")
    p.add_argument("--country", required=True)
    p.add_argument("--lang", default="en")

    p = sub.add_parser("set-locale", help="设置 locale")
    p.add_argument("--country", required=True)
    p.add_argument("--city", required=True)
    p.add_argument("--lang", default="en")
    p.add_argument("--mode", choices=["api", "human"], default="api")

    sub.add_parser("get-locale", help="获取当前 locale")

    p = sub.add_parser("search", help="搜索帖子")
    p.add_argument("--keyword", required=True)
    p.add_argument("--country", default="singapore")
    p.add_argument("--city", default="singapore")
    p.add_argument("--lang", default="en")
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--min-price", type=float, default=None, dest="price_min")
    p.add_argument("--max-price", type=float, default=None, dest="price_max")

    p = sub.add_parser("list-feeds", help="获取首页推荐")
    p.add_argument("--country", default="singapore")
    p.add_argument("--city", default="singapore")
    p.add_argument("--lang", default="en")
    p.add_argument("--max-results", type=int, default=20)

    p = sub.add_parser("get-listing", help="获取帖子详情")
    p.add_argument("--url", required=True)

    p = sub.add_parser("browse-category", help="按分类浏览")
    p.add_argument("--category", required=True)
    p.add_argument("--country", default="singapore")
    p.add_argument("--city", default="singapore")
    p.add_argument("--lang", default="en")
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--min-price", type=float, default=None, dest="price_min")
    p.add_argument("--max-price", type=float, default=None, dest="price_max")

    p = sub.add_parser("full-search", help="一站式搜索")
    p.add_argument("--country", required=True)
    p.add_argument("--city", required=True)
    p.add_argument("--category", default=None)
    p.add_argument("--keyword", default=None)
    p.add_argument("--lang", default="en")
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--min-price", type=float, default=None, dest="price_min")
    p.add_argument("--max-price", type=float, default=None, dest="price_max")

    # check-login
    p = sub.add_parser("check-login", help="检查登录状态")
    p.add_argument("--country", default="singapore", help="国家（用于导航，默认 singapore）")
    p.add_argument("--subdomain", default=None, help="目标站点子域名（如 au/sg/us），指定后在该站检测登录态")

    # login
    p = sub.add_parser("login", help="通过邮箱密码登录")
    p.add_argument("--email", required=True, help="邮箱地址")
    p.add_argument("--password", required=True, help="密码")
    p.add_argument("--country", default="singapore", help="国家（用于导航，默认 singapore）")
    p.add_argument("--subdomain", default=None, help="目标站点子域名（如 au/sg/us），指定后在该站登录")

    # wait-login
    p = sub.add_parser("wait-login", help="等待用户手动完成登录（OAuth 等场景）")
    p.add_argument("--timeout", type=float, default=120.0, help="等待超时秒数（默认 120）")
    p.add_argument("--country", default="singapore", help="国家（用于导航，默认 singapore）")
    p.add_argument("--subdomain", default=None, help="目标站点子域名（如 au/sg/us），指定后在该站等待登录")

    # ─── favorites ───────────────────────────────────────────
    p = sub.add_parser("list-favorites", help="列出收藏列表")
    p.add_argument("--subdomain", default="sg", help="国家子域（sg/us/ae …）")
    p.add_argument("--lang", default="en")
    p.add_argument("--max-results", type=int, default=50)

    p = sub.add_parser("add-favorite", help="收藏帖子（通过详情页 URL）")
    p.add_argument("--url", required=True, help="帖子详情页 URL")

    p = sub.add_parser("remove-favorite", help="取消收藏")
    p.add_argument("--url", default=None, help="帖子详情页 URL（详情页取消）")
    p.add_argument("--index", type=int, default=None, help="收藏列表中的索引（0-based，配合 --subdomain）")
    p.add_argument("--subdomain", default="sg", help="国家子域（配合 --index 使用）")

    # ─── my posts ────────────────────────────────────────────
    p = sub.add_parser("list-my-posts", help="列出我的帖子")
    p.add_argument("--subdomain", default="sg", help="国家子域（sg/us/ae …）")
    p.add_argument("--lang", default="en")
    p.add_argument("--state", default="active", choices=["active", "pending", "expired", "draft"])
    p.add_argument("--max-results", type=int, default=50)

    p = sub.add_parser("delete-post", help="删除我的帖子（按序号）")
    p.add_argument("--subdomain", default="sg", help="国家子域（sg/us/ae …）")
    p.add_argument("--lang", default="en")
    p.add_argument("--index", type=int, default=0, help="帖子序号（0-based）")

    p = sub.add_parser("edit-post", help="获取帖子编辑链接")
    p.add_argument("--subdomain", default="sg", help="国家子域（sg/us/ae …）")
    p.add_argument("--lang", default="en")
    p.add_argument("--index", type=int, default=0, help="帖子序号（0-based）")

    return parser


_CMD_MAP = {
    "list-countries": cmd_list_countries,
    "list-cities": cmd_list_cities,
    "search-cities": cmd_search_cities,
    "list-categories": cmd_list_categories,
    "set-locale": cmd_set_locale,
    "get-locale": cmd_get_locale,
    "search": cmd_search,
    "list-feeds": cmd_list_feeds,
    "get-listing": cmd_get_listing,
    "browse-category": cmd_browse_category,
    "full-search": cmd_full_search,
    "check-login": cmd_check_login,
    "login": cmd_login,
    "wait-login": cmd_wait_login,
    "list-favorites": cmd_list_favorites,
    "add-favorite": cmd_add_favorite,
    "remove-favorite": cmd_remove_favorite,
    "list-my-posts": cmd_list_my_posts,
    "delete-post": cmd_delete_post,
    "edit-post": cmd_edit_post,
}


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    handler = _CMD_MAP.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)

    _LOGIN_REQUIRED_CMDS = {
        "list-favorites", "add-favorite", "remove-favorite",
        "list-my-posts", "delete-post", "edit-post",
    }

    try:
        if args.command in _LOGIN_REQUIRED_CMDS:
            from ok.client.factory import get_client
            from ok.login import check_login

            client = get_client()
            subdomain = getattr(args, "subdomain", None)
            status = check_login(client, subdomain=subdomain)
            if not status["logged_in"]:
                site = f" ({subdomain}.ok.com)" if subdomain else ""
                _error(
                    f"未登录{site}。请先在目标站点登录后重试。"
                )
                return

        handler(args)
    except OKError as e:
        _error(str(e))
    except Exception as e:
        _error(f"未预期错误: {e}")


if __name__ == "__main__":
    main()
