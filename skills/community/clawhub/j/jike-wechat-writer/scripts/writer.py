#!/usr/bin/env python3
"""
公众号文章创作 CLI — 选题搜索、热点与图片生成能力脚本。

Usage:
  python3 writer.py check
  python3 writer.py search --query "关键词" [--action news|wechat_article|image]
  python3 writer.py trend
  python3 writer.py trend-summary --keyword "关键词"
  python3 writer.py generate-image --prompt "图片描述" [--ratio 3:4] [--ref-url URL ...]

Configuration:
  Edit scripts/config.json to set api_key and base_url.
  Environment variables 100CITY_API_KEY / 100CITY_BASE_URL override config.json.
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

DEFAULT_BASE_URL = "https://gin-test.100.city/api"

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


def get_config():
    """Resolve api_key and base_url. Env vars override config.json."""
    cfg = load_config()

    key = os.environ.get("100CITY_API_KEY", "").strip()
    if not key:
        key = (cfg.get("api_key") or "").strip()

    base = os.environ.get("100CITY_BASE_URL", "").strip()
    if not base:
        base = (cfg.get("base_url") or "").strip()
    if not base:
        base = DEFAULT_BASE_URL

    return key, base.rstrip("/")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def api_request(method: str, path: str, body=None, query: dict | None = None) -> dict:
    """Send HTTP request to API. Returns parsed JSON response."""
    key, base = get_config()
    if not key:
        print("Error: API Key 未配置。请设置环境变量 100CITY_API_KEY 或在 config.json 中填写 api_key。", file=sys.stderr)
        sys.exit(1)
    url = f"{base}{path}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if key:
        headers["Authorization"] = f"Bearer {key}"

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("msg") or err_json.get("message", err_body)
        except Exception:
            msg = err_body
        print(f"Error: HTTP {e.code} — {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Connection failed — {e.reason}", file=sys.stderr)
        sys.exit(1)

    # GVA standard response: {code: 0, data: ..., msg: "..."}
    if isinstance(result, dict):
        code = result.get("code", 0)
        if code != 0:
            print(f"Error: {result.get('msg', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        return result.get("data", result)
    return result


def fmt_json(data, use_json: bool = False):
    if use_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    return False


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_check(_args):
    """Check API connectivity."""
    key, base = get_config()
    print(f"Config:   {CONFIG_PATH}")
    print(f"Base URL: {base}")
    print(f"Key:      {key[:8]}...{key[-4:]}" if len(key) > 12 else f"Key: {key}")
    try:
        data = api_request("GET", "/agent_adk/capabilities/trend_news")
        success = data.get("success", False) if isinstance(data, dict) else False
        if success:
            print(f"Status:   OK")
            print(f"Data:     {data.get('data_date', 'N/A')} ({data.get('total', 0)} items)")
        else:
            print(f"Status:   Connected but got unexpected response")
    except SystemExit:
        print("Status:   FAILED — check your API key and base URL")
        sys.exit(1)


def cmd_search(args):
    """Unified search: news / wechat_article / image."""
    if not args.query:
        print("Error: --query required", file=sys.stderr)
        sys.exit(1)

    body = {
        "action": args.action or "news",
        "query": args.query,
    }
    data = api_request("POST", "/agent_adk/capabilities/search", body)

    if fmt_json(data, args.json):
        return

    success = data.get("success", False)
    if not success:
        print(f"搜索失败: {data.get('message', 'unknown error')}")
        return

    results = data.get("results", [])
    total = data.get("total", len(results))
    action = data.get("action", body["action"])
    print(f"搜索类型: {action}")
    print(f"关键词:   {data.get('query', args.query)}")
    print(f"结果数:   {total}\n")

    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        url = r.get("url", "")
        snippet = r.get("snippet", "")
        source = r.get("source", "")
        date = r.get("publish_date", "")

        header = f"[{i}] {title}"
        if source or date:
            header += f"  ({source} {date})".rstrip()
        print(header)

        if action == "image":
            # image results: snippet contains the image URL
            print(f"    图片: {snippet}")
        else:
            if snippet:
                preview = snippet[:200].replace("\n", " ")
                print(f"    {preview}")
            if url:
                print(f"    {url}")
        print()


def cmd_trend(args):
    """Get latest trend news."""
    data = api_request("GET", "/agent_adk/capabilities/trend_news")

    if fmt_json(data, args.json):
        return

    if not data.get("success"):
        print(f"获取失败: {data.get('message', 'unknown error')}")
        return

    date = data.get("data_date", "")
    items = data.get("items", [])
    print(f"日期: {date}")
    print(f"热点数: {len(items)}\n")

    for item in items:
        rank = item.get("rank", "")
        title = item.get("title", "")
        platform = item.get("platform_name", "")
        url = item.get("url", "")
        print(f"  [{rank:>3}] 【{platform}】{title}")
        if url:
            print(f"        {url}")


def cmd_style_by_name(args):
    """Analyze wechat mp writing style by account name."""
    if not args.name:
        print("Error: --name required", file=sys.stderr)
        sys.exit(1)

    body = {"account_name": args.name}
    data = api_request("POST", "/agent_adk/capabilities/wechat_mp_style/analyze_by_name", body)

    if fmt_json(data, args.json):
        return

    if not data.get("success"):
        print(f"拆解失败: {data.get('message', 'unknown error')}")
        if data.get("error"):
            print(f"  原因: {data['error']}")
        return

    print(f"公众号:   {data.get('account_name', '')}")
    print(f"任务ID:   {data.get('task_id', '')}")
    print(f"状态:     {data.get('status', '')}")
    analysis_url = data.get("article_analysis_url", "")
    if analysis_url:
        print(f"风格报告: {analysis_url}")
    list_url = data.get("article_list_url", "")
    if list_url:
        print(f"文章列表: {list_url}")


def cmd_style_by_url(args):
    """Analyze wechat mp writing style by article URL."""
    if not args.url:
        print("Error: --url required", file=sys.stderr)
        sys.exit(1)

    body = {"article_url": args.url}
    data = api_request("POST", "/agent_adk/capabilities/wechat_mp_style/analyze_by_url", body)

    if fmt_json(data, args.json):
        return

    if not data.get("success"):
        print(f"拆解失败: {data.get('message', 'unknown error')}")
        if data.get("error"):
            print(f"  原因: {data['error']}")
        return

    print(f"公众号:   {data.get('account_name', '')}")
    print(f"任务ID:   {data.get('task_id', '')}")
    print(f"状态:     {data.get('status', '')}")
    analysis_url = data.get("article_analysis_url", "")
    if analysis_url:
        print(f"风格报告: {analysis_url}")
    list_url = data.get("article_list_url", "")
    if list_url:
        print(f"文章列表: {list_url}")


def cmd_trend_summary(args):
    """Summarize trend news by keyword."""
    if not args.keyword:
        print("Error: --keyword required", file=sys.stderr)
        sys.exit(1)

    body = {"keyword": args.keyword}
    data = api_request("POST", "/agent_adk/capabilities/trend_news/summary", body)

    if fmt_json(data, args.json):
        return

    if not data.get("success"):
        print(f"总结失败: {data.get('message', 'unknown error')}")
        return

    date = data.get("data_date", "")
    keyword = data.get("keyword", args.keyword)
    summary = data.get("summary", "")
    points = data.get("points", [])

    print(f"关键词: {keyword}")
    print(f"日期:   {date}")
    print(f"总览:   {summary}\n")

    if not points:
        print("未发现相关内容点")
        return

    print(f"内容点 ({len(points)}):\n")
    for p in points:
        pid = p.get("id", "?")
        title = p.get("title", "")
        desc = p.get("description", "")
        relevance = p.get("relevance", "")
        refs = p.get("news_refs", [])

        print(f"  [{pid}] {title}")
        if desc:
            print(f"      {desc}")
        if relevance:
            print(f"      关联: {relevance}")
        if refs:
            for ref in refs:
                r_title = ref.get("title", "")
                r_source = ref.get("source", "")
                r_url = ref.get("url", "")
                label = f"{r_title}（{r_source}）" if r_source else r_title
                print(f"      来源: {label}  {r_url}")
        print()


def cmd_generate_image(args):
    """Generate image from prompt."""
    if not args.prompt:
        print("Error: --prompt required", file=sys.stderr)
        sys.exit(1)

    body = {"prompt": args.prompt}
    if args.ratio:
        body["ratio"] = args.ratio
    if args.ref_url:
        body["image_urls"] = args.ref_url

    data = api_request("POST", "/agent_adk/capabilities/generate_image", body)

    if fmt_json(data, args.json):
        return

    if not data.get("success"):
        print(f"生成失败: {data.get('message', 'unknown error')}")
        if data.get("error"):
            print(f"  原因: {data['error']}")
        return

    image_url = data.get("image_url", "")
    print(f"状态:   成功")
    print(f"图片URL: {image_url}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser():
    parser = argparse.ArgumentParser(
        prog="writer.py",
        description="公众号文章创作 CLI — 选题搜索与热点能力",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    sub.add_parser("check", help="检查连接和认证")

    # search
    p = sub.add_parser("search", help="统一搜索（news/wechat_article/image）")
    p.add_argument("--query", "-q", required=True, help="搜索关键词")
    p.add_argument("--action", "-a", default="news",
                   choices=["news", "wechat_article", "image"],
                   help="搜索类型（默认 news）")
    p.add_argument("--json", action="store_true")

    # trend
    p = sub.add_parser("trend", help="获取最新热点新闻")
    p.add_argument("--json", action="store_true")

    # trend-summary
    p = sub.add_parser("trend-summary", help="关键词热点总结")
    p.add_argument("--keyword", "-k", required=True, help="关键词")
    p.add_argument("--json", action="store_true")

    # style-by-name
    p = sub.add_parser("style-by-name", help="按公众号名称拆解创作风格")
    p.add_argument("--name", "-n", required=True, help="公众号名称")
    p.add_argument("--json", action="store_true")

    # style-by-url
    p = sub.add_parser("style-by-url", help="按文章链接拆解创作风格")
    p.add_argument("--url", "-u", required=True, help="公众号文章链接")
    p.add_argument("--json", action="store_true")

    # generate-image
    p = sub.add_parser("generate-image", help="AI 生成图片")
    p.add_argument("--prompt", "-p", required=True, help="图片内容描述")
    p.add_argument("--ratio", "-r", default=None,
                   help="宽高比（如 1:1/3:4/16:9，默认 3:4）")
    p.add_argument("--ref-url", action="append", default=None,
                   help="参考图片 URL（可多次指定，启用图生图模式）")
    p.add_argument("--json", action="store_true")

    return parser


COMMAND_MAP = {
    "check": cmd_check,
    "search": cmd_search,
    "trend": cmd_trend,
    "trend-summary": cmd_trend_summary,
    "style-by-name": cmd_style_by_name,
    "style-by-url": cmd_style_by_url,
    "generate-image": cmd_generate_image,
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
