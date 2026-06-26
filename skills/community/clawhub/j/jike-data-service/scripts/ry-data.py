#!/usr/bin/env python3
"""
极客数据 CLI — OpenClaw skill script for 抖音内容营销数据平台.

Usage:
  python3 ry-data.py check
  python3 ry-data.py accounts search [options]
  python3 ry-data.py accounts get --sec-uid <sec_uid>
  python3 ry-data.py videos search [options]
  python3 ry-data.py videos trend --aweme-id <id> [--days 7]
  python3 ry-data.py keywords search [options]
  python3 ry-data.py keywords add --word <keyword>
  python3 ry-data.py keywords delete --word <keyword>
  python3 ry-data.py keyword-videos search [options]
  python3 ry-data.py hot-videos search [options]
  python3 ry-data.py hot-videos categories
  python3 ry-data.py hashtags search [options]
  python3 ry-data.py hashtags trending [--days 7] [--size 50]

Configuration:
  Edit scripts/config.json to set base_url.
  Environment variable RY_DATA_BASE_URL overrides config.json.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
DEFAULT_BASE_URL = "https://ry-api.dso100.com"

_config_cache = None


def load_config() -> dict:
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    if not os.path.exists(CONFIG_PATH):
        _config_cache = {}
        return _config_cache
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to read config.json: {e}", file=sys.stderr)
        _config_cache = {}
    return _config_cache


def get_base_url() -> str:
    url = os.environ.get("RY_DATA_BASE_URL", "").strip()
    if not url:
        cfg = load_config()
        url = (cfg.get("base_url") or "").strip()
    return url or DEFAULT_BASE_URL


def get_secret_key() -> str:
    """Get API key. Environment variable overrides config.json."""
    key = os.environ.get("RY_DATA_SECRET_KEY", "").strip()
    if not key:
        cfg = load_config()
        key = (cfg.get("secret_key") or "").strip()
    return key


def get_page_size() -> int:
    cfg = load_config()
    return cfg.get("page_size", 20)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def api_request(method: str, path: str, body=None, query: dict | None = None) -> dict:
    """Send HTTP request to API. Returns parsed JSON response."""
    base = get_base_url()
    url = f"{base}{path}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    secret_key = get_secret_key()
    if secret_key:
        headers["X-API-Key"] = secret_key

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("message", err_body)
        except Exception:
            msg = err_body
        print(f"Error: HTTP {e.code} — {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Connection failed — {e.reason}", file=sys.stderr)
        sys.exit(1)

    if isinstance(result, dict) and result.get("code", 0) not in (0, 200):
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    return result.get("data") if isinstance(result, dict) else result


def fmt_json(data, use_json: bool = False):
    if use_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    return False


def fmt_number(n) -> str:
    """Format large numbers: 12345 -> 1.2万"""
    if n is None:
        return "0"
    n = int(n)
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)


# ---------------------------------------------------------------------------
# Commands: check
# ---------------------------------------------------------------------------


def cmd_check(_args):
    base = get_base_url()
    key = get_secret_key()
    print(f"Config:   {CONFIG_PATH}")
    print(f"Base URL: {base}")
    if key:
        print(f"Key:      {key[:8]}...{key[-4:]}" if len(key) > 12 else f"Key: {key}")
    else:
        print(f"Key:      未配置 (set secret_key in config.json or RY_DATA_SECRET_KEY env)")
    try:
        data = api_request("GET", "/api/v1/douyin/hot-videos/categories")
        count = len(data) if isinstance(data, list) else 0
        print(f"Status:   OK ({count} categories available)")
    except SystemExit:
        print("Status:   FAILED — check your API key and network")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commands: accounts
# ---------------------------------------------------------------------------


def cmd_accounts(args):
    if args.action == "search":
        body = {}
        if args.keyword: body["keyword"] = args.keyword
        if args.follower_min is not None: body["follower_min"] = args.follower_min
        if args.follower_max is not None: body["follower_max"] = args.follower_max
        if args.brand_tags: body["brand_tags"] = [t.strip() for t in args.brand_tags.split(",")]
        if args.content_tags: body["content_tags"] = [t.strip() for t in args.content_tags.split(",")]
        if args.user_type: body["user_type"] = [int(t.strip()) for t in args.user_type.split(",")]
        if args.exclude_star: body["exclude_star"] = True
        if args.exclude_shop: body["exclude_shop"] = True
        body["sort_by"] = args.sort_by or "follower_count"
        body["sort_order"] = args.sort_order or "desc"
        body["page"] = args.page or 1
        body["page_size"] = args.page_size or get_page_size()

        data = api_request("POST", "/api/v1/douyin/users/search", body)
        if fmt_json(data, args.json):
            return

        total = data.get("total", 0)
        users = data.get("list", [])
        print(f"共 {total} 个账号，当前显示 {len(users)} 个:\n")
        for i, u in enumerate(users, 1):
            nickname = u.get("nickname", "未知")
            followers = fmt_number(u.get("follower_count", 0))
            favorited = fmt_number(u.get("total_favorited", 0))
            aweme = u.get("aweme_count", 0)
            utype = {1: "个人", 2: "黄V", 3: "蓝V"}.get(u.get("user_type"), "?")
            brands = ",".join(u.get("brand_tags", []))
            tags = ",".join(u.get("content_tags", []))
            print(f"  {i}. {nickname} [{utype}]  粉丝:{followers}  获赞:{favorited}  作品:{aweme}")
            if brands:
                print(f"     品牌: {brands}")
            if tags:
                print(f"     标签: {tags}")
            print(f"     sec_uid: {u.get('sec_uid', '')}")
            print()

    elif args.action == "get":
        if not args.sec_uid:
            print("Error: --sec-uid required", file=sys.stderr); sys.exit(1)
        data = api_request("GET", f"/api/v1/douyin/users/{args.sec_uid}")
        if fmt_json(data, args.json):
            return
        print(json.dumps(data, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Commands: videos
# ---------------------------------------------------------------------------


def cmd_videos(args):
    if args.action == "search":
        body = {}
        if args.keyword: body["keyword"] = args.keyword
        if args.sec_uids: body["sec_uids"] = [s.strip() for s in args.sec_uids.split(",")]
        if args.interaction_min is not None: body["interaction_count_min"] = args.interaction_min
        if args.interaction_max is not None: body["interaction_count_max"] = args.interaction_max
        if args.publish_start: body["publish_time_start"] = args.publish_start
        if args.publish_end: body["publish_time_end"] = args.publish_end
        body["sort_by"] = args.sort_by or "interaction_count"
        body["sort_order"] = args.sort_order or "desc"
        body["page"] = args.page or 1
        body["page_size"] = args.page_size or get_page_size()

        data = api_request("POST", "/api/v1/douyin/videos/search", body)
        if fmt_json(data, args.json):
            return

        total = data.get("total", 0)
        videos = data.get("list", [])
        print(f"共 {total} 个视频，当前显示 {len(videos)} 个:\n")
        for i, v in enumerate(videos, 1):
            title = (v.get("desc") or v.get("item_title") or "无标题")[:60]
            author = v.get("nickname") or v.get("nick_name") or "未知"
            interaction = fmt_number(v.get("interaction_count", 0))
            play = fmt_number(v.get("play_count") or v.get("play_cnt", 0))
            like = fmt_number(v.get("digg_count") or v.get("like_cnt", 0))
            print(f"  {i}. {title}")
            print(f"     作者: {author}  播放:{play}  点赞:{like}  互动:{interaction}")
            aweme_id = v.get("aweme_id") or v.get("item_id", "")
            if aweme_id:
                print(f"     aweme_id: {aweme_id}")
            print()

    elif args.action == "trend":
        if not args.aweme_id:
            print("Error: --aweme-id required", file=sys.stderr); sys.exit(1)
        days = args.days or 7
        data = api_request("GET", f"/api/v1/douyin/videos/{args.aweme_id}/trend",
                           query={"days": str(days)})
        if fmt_json(data, args.json):
            return
        items = data.get("list", []) if isinstance(data, dict) else data
        total = data.get("total", len(items)) if isinstance(data, dict) else len(items)
        print(f"视频趋势 (近{days}天, {total}条记录):\n")
        if isinstance(items, list):
            for item in items:
                print(f"  {json.dumps(item, ensure_ascii=False)}")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Commands: keywords
# ---------------------------------------------------------------------------


def cmd_keywords(args):
    if args.action == "search":
        body = {}
        if args.keyword: body["keyword"] = args.keyword
        if args.brand: body["brand"] = args.brand
        if args.category: body["category"] = args.category
        body["sort_by"] = args.sort_by or "mounth_search_index"
        body["sort_order"] = args.sort_order or "desc"
        body["page"] = args.page or 1
        body["page_size"] = args.page_size or get_page_size()

        data = api_request("POST", "/api/v1/douyin/keywords/search", body)
        if fmt_json(data, args.json):
            return

        total = data.get("total", 0)
        kws = data.get("list", [])
        print(f"共 {total} 个关键词，当前显示 {len(kws)} 个:\n")
        for i, kw in enumerate(kws, 1):
            word = kw.get("keyword", "")
            search_idx = kw.get("mounth_search_index", 0)
            competition = kw.get("competition", "")
            video_count = kw.get("video_count", 0)
            print(f"  {i}. {word}")
            print(f"     月搜索指数:{search_idx}  竞争:{competition}  视频数:{video_count}")
            print()

    elif args.action == "add":
        if not args.word:
            print("Error: --word required", file=sys.stderr); sys.exit(1)
        data = api_request("POST", "/api/v1/douyin/keywords", {"keyword": args.word})
        if fmt_json(data, args.json):
            return
        print(f"关键词添加成功: {args.word}")

    elif args.action == "delete":
        if not args.word:
            print("Error: --word required", file=sys.stderr); sys.exit(1)
        api_request("DELETE", f"/api/v1/douyin/keywords/{urllib.parse.quote(args.word)}")
        print(f"关键词删除成功: {args.word}")


# ---------------------------------------------------------------------------
# Commands: keyword-videos
# ---------------------------------------------------------------------------


def cmd_keyword_videos(args):
    if args.action == "search":
        body = {}
        if args.keyword: body["keyword"] = args.keyword
        if args.search_date: body["search_date"] = args.search_date
        body["sort_by"] = args.sort_by or "rank"
        body["sort_order"] = args.sort_order or "asc"
        body["page"] = args.page or 1
        body["page_size"] = args.page_size or get_page_size()

        data = api_request("POST", "/api/v1/douyin/keyword-videos/search", body)
        if fmt_json(data, args.json):
            return

        total = data.get("total", 0)
        videos = data.get("list", [])
        print(f"关键词「{args.keyword or ''}」搜索排名，共 {total} 条:\n")
        for i, v in enumerate(videos, 1):
            title = (v.get("desc") or v.get("item_title") or "无标题")[:60]
            rank = v.get("rank", i)
            author = v.get("nickname") or v.get("nick_name") or "未知"
            print(f"  #{rank} {title}")
            print(f"      作者: {author}")
            print()


# ---------------------------------------------------------------------------
# Commands: hot-videos
# ---------------------------------------------------------------------------


def cmd_hot_videos(args):
    if args.action == "search":
        body = {}
        if args.category: body["category"] = args.category
        if args.snapshot_date: body["snapshot_date"] = args.snapshot_date
        if args.keyword: body["keyword"] = args.keyword
        body["sort_by"] = args.sort_by or "score"
        body["sort_order"] = args.sort_order or "desc"
        body["page"] = args.page or 1
        body["page_size"] = args.page_size or get_page_size()

        data = api_request("POST", "/api/v1/douyin/hot-videos/search", body)
        if fmt_json(data, args.json):
            return

        total = data.get("total", 0)
        videos = data.get("list", [])
        print(f"热榜视频，共 {total} 条:\n")
        for i, v in enumerate(videos, 1):
            title = (v.get("item_title") or "无标题")[:60]
            author = v.get("nick_name") or "未知"
            score = v.get("score", 0)
            play = fmt_number(v.get("play_cnt", 0))
            like = fmt_number(v.get("like_cnt", 0))
            follow_rate = v.get("follow_rate", 0)
            cat = v.get("category", "")
            rank = v.get("rank", i)
            print(f"  #{rank} [{cat}] {title}")
            print(f"      作者:{author}  热度:{score}  播放:{play}  点赞:{like}  涨粉率:{follow_rate}")
            print()

    elif args.action == "categories":
        data = api_request("GET", "/api/v1/douyin/hot-videos/categories")
        if fmt_json(data, args.json):
            return
        if isinstance(data, list):
            print(f"共 {len(data)} 个分类:\n")
            for c in data:
                print(f"  [{c.get('category_id', '?')}] {c.get('category', '?')}")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Commands: hashtags
# ---------------------------------------------------------------------------


def cmd_hashtags(args):
    if args.action == "search":
        body = {}
        if args.keyword: body["keyword"] = args.keyword
        if args.is_trending: body["is_trending"] = True
        body["sort_by"] = args.sort_by or "video_count"
        body["sort_order"] = args.sort_order or "desc"
        body["page"] = args.page or 1
        body["page_size"] = args.page_size or get_page_size()

        data = api_request("POST", "/api/v1/douyin/hashtags/search", body)
        if fmt_json(data, args.json):
            return

        total = data.get("total", 0)
        tags = data.get("list", [])
        print(f"话题标签，共 {total} 条:\n")
        for i, t in enumerate(tags, 1):
            name = t.get("hashtag", "")
            vcount = t.get("video_count", 0)
            interaction = fmt_number(t.get("total_interaction", 0))
            print(f"  {i}. #{name}  视频数:{vcount}  总互动:{interaction}")

    elif args.action == "trending":
        body = {
            "days": args.days or 7,
            "size": args.size or 50,
        }
        data = api_request("POST", "/api/v1/douyin/trending-hashtags", body)
        if fmt_json(data, args.json):
            return

        items = data.get("list", []) if isinstance(data, dict) else data
        total = data.get("total", len(items)) if isinstance(data, dict) else len(items)
        print(f"热门话题 (近{body['days']}天, {total}条):\n")
        for i, t in enumerate(items, 1):
            name = t.get("hashtag", "")
            vcount = t.get("video_count", 0)
            interaction = fmt_number(t.get("total_interaction", 0))
            print(f"  {i}. #{name}  视频数:{vcount}  总互动:{interaction}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ry-data.py",
        description="极客数据 CLI — 抖音内容营销数据平台",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    sub.add_parser("check", help="检查 API 连接状态")

    # --- accounts ---
    p = sub.add_parser("accounts", help="账号搜索与查询")
    p.add_argument("action", choices=["search", "get"])
    p.add_argument("--keyword", help="搜索昵称/简介")
    p.add_argument("--follower-min", type=int, help="最低粉丝数")
    p.add_argument("--follower-max", type=int, help="最高粉丝数")
    p.add_argument("--brand-tags", help="品牌标签，逗号分隔 (荣耀,华为,小米,OPPO,vivo,苹果,三星)")
    p.add_argument("--content-tags", help="内容标签，逗号分隔 (拍摄,电池,屏幕,AI,外观,性能,游戏,评测,开箱,折叠屏,性价比)")
    p.add_argument("--user-type", help="账号类型，逗号分隔 (1=个人,2=黄V,3=蓝V)")
    p.add_argument("--exclude-star", action="store_true", help="排除明星账号")
    p.add_argument("--exclude-shop", action="store_true", help="排除带货账号")
    p.add_argument("--sec-uid", help="用户 sec_uid (get 用)")
    p.add_argument("--sort-by", default="follower_count", help="排序字段")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int)
    p.add_argument("--json", action="store_true", help="输出原始 JSON")

    # --- videos ---
    p = sub.add_parser("videos", help="视频搜索与趋势")
    p.add_argument("action", choices=["search", "trend"])
    p.add_argument("--keyword", help="搜索视频标题/描述")
    p.add_argument("--sec-uids", help="作者 sec_uid 列表，逗号分隔")
    p.add_argument("--interaction-min", type=int, help="最低互动量")
    p.add_argument("--interaction-max", type=int, help="最高互动量")
    p.add_argument("--publish-start", type=int, help="发布时间起始 (Unix timestamp)")
    p.add_argument("--publish-end", type=int, help="发布时间结束 (Unix timestamp)")
    p.add_argument("--aweme-id", help="视频 ID (trend 用)")
    p.add_argument("--days", type=int, default=7, help="趋势天数 (默认7)")
    p.add_argument("--sort-by", default="interaction_count", help="排序字段")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int)
    p.add_argument("--json", action="store_true")

    # --- keywords ---
    p = sub.add_parser("keywords", help="关键词搜索与管理")
    p.add_argument("action", choices=["search", "add", "delete"])
    p.add_argument("--keyword", help="搜索关键词")
    p.add_argument("--word", help="要添加/删除的关键词")
    p.add_argument("--brand", help="品牌筛选")
    p.add_argument("--category", help="分类筛选")
    p.add_argument("--sort-by", default="mounth_search_index", help="排序字段")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int)
    p.add_argument("--json", action="store_true")

    # --- keyword-videos ---
    p = sub.add_parser("keyword-videos", help="关键词搜索排名视频")
    p.add_argument("action", choices=["search"])
    p.add_argument("--keyword", help="关键词 (精确匹配)")
    p.add_argument("--search-date", help="搜索日期 YYYY-MM-DD")
    p.add_argument("--sort-by", default="rank")
    p.add_argument("--sort-order", default="asc", choices=["asc", "desc"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int)
    p.add_argument("--json", action="store_true")

    # --- hot-videos ---
    p = sub.add_parser("hot-videos", help="热榜视频")
    p.add_argument("action", choices=["search", "categories"])
    p.add_argument("--category", help="分类名称 (如 科技, 游戏)")
    p.add_argument("--snapshot-date", help="日期 YYYY-MM-DD")
    p.add_argument("--keyword", help="搜索视频标题")
    p.add_argument("--sort-by", default="score")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int)
    p.add_argument("--json", action="store_true")

    # --- hashtags ---
    p = sub.add_parser("hashtags", help="话题标签搜索与热门趋势")
    p.add_argument("action", choices=["search", "trending"])
    p.add_argument("--keyword", help="搜索话题")
    p.add_argument("--is-trending", action="store_true", help="仅热门话题")
    p.add_argument("--days", type=int, default=7, help="热门话题天数范围")
    p.add_argument("--size", type=int, default=50, help="热门话题数量")
    p.add_argument("--sort-by", default="video_count")
    p.add_argument("--sort-order", default="desc", choices=["asc", "desc"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int)
    p.add_argument("--json", action="store_true")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

COMMAND_MAP = {
    "check": cmd_check,
    "accounts": cmd_accounts,
    "videos": cmd_videos,
    "keywords": cmd_keywords,
    "keyword-videos": cmd_keyword_videos,
    "hot-videos": cmd_hot_videos,
    "hashtags": cmd_hashtags,
}


def main():
    parser = build_parser()
    args = parser.parse_args()
    handler = COMMAND_MAP.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
