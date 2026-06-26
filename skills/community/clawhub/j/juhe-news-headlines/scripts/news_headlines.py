#!/usr/bin/env python3
"""
新闻头条查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
获取最新新闻头条，支持按分类查询和新闻详情

用法:
    python news_headlines.py [--type top] [--page 1] [--page-size 30]
    python news_headlines.py --detail <uniquekey>

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_NEWS_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_NEWS_KEY=your_api_key
    3. 直接传参: python news_headlines.py --key your_api_key --type top

免费申请 API Key: https://www.juhe.cn/docs/api/id/235
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

LIST_API_URL = "http://v.juhe.cn/toutiao/index"
DETAIL_API_URL = "http://v.juhe.cn/toutiao/content"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/235"

# 支持的新闻分类
TYPE_OPTIONS = [
    "top", "guonei", "guoji", "yule", "tiyu",
    "junshi", "keji", "caijing", "youxi", "qiche", "jiankang"
]


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_NEWS_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_NEWS_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def query_list(
    api_key: str,
    type_: str = "top",
    page: int = 1,
    page_size: int = 30,
    is_filter: int = 0,
) -> dict:
    """查询新闻列表"""
    params = {
        "key": api_key,
        "type": type_ if type_ in TYPE_OPTIONS else "top",
        "page": min(max(1, page), 50),
        "page_size": min(max(1, page_size), 30),
        "is_filter": 1 if is_filter else 0,
    }
    url = f"{LIST_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    if data.get("error_code") == 0:
        result = data.get("result", {})
        return {
            "success": True,
            "stat": result.get("stat"),
            "page": result.get("page"),
            "pageSize": result.get("pageSize"),
            "data": result.get("data") or [],
        }

    return {
        "success": False,
        "error_code": data.get("error_code", -1),
        "reason": data.get("reason", "查询失败"),
    }


def query_detail(api_key: str, uniquekey: str) -> dict:
    """查询新闻详情"""
    uniquekey = uniquekey.strip()
    if not uniquekey:
        return {"success": False, "error": "uniquekey 不能为空"}

    params = {"key": api_key, "uniquekey": uniquekey}
    url = f"{DETAIL_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    if data.get("error_code") == 0:
        result = data.get("result", {})
        detail = result.get("detail", {})
        return {
            "success": True,
            "uniquekey": result.get("uniquekey"),
            "content": result.get("content", ""),
            "detail": {
                "title": detail.get("title"),
                "date": detail.get("date"),
                "category": detail.get("category"),
                "author_name": detail.get("author_name"),
                "url": detail.get("url"),
                "thumbnail_pic_s": detail.get("thumbnail_pic_s"),
            },
        }

    error_code = data.get("error_code", -1)
    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 223501:
        hint = "（uniquekey 格式错误）"
    elif error_code == 223502:
        hint = "（暂无法查询该新闻详情）"

    return {
        "success": False,
        "error_code": error_code,
        "reason": f"{reason}{hint}",
    }


def format_list_output(result: dict, type_: str) -> None:
    """格式化新闻列表输出"""
    if not result["success"]:
        print(f"❌ {result.get('reason', result.get('error', '查询失败'))}")
        return

    items = result.get("data", [])
    if not items:
        print("暂无新闻数据")
        return

    type_names = {
        "top": "推荐", "guonei": "国内", "guoji": "国际",
        "yule": "娱乐", "tiyu": "体育", "junshi": "军事",
        "keji": "科技", "caijing": "财经", "youxi": "游戏",
        "qiche": "汽车", "jiankang": "健康",
    }
    cat_name = type_names.get(type_, type_)

    print(f"📰 {cat_name}新闻 (共 {len(items)} 条)\n")
    for i, item in enumerate(items, 1):
        title = item.get("title", "未知标题")[:50]
        if len(item.get("title", "")) > 50:
            title += "..."
        date_str = item.get("date", "")[:16]
        author = item.get("author_name", "-")
        print(f"{i}. {title}")
        print(f"   来源: {author} | 时间: {date_str} | ID: {item.get('uniquekey', '-')}")
        print()


def format_detail_output(result: dict) -> None:
    """格式化新闻详情输出"""
    if not result["success"]:
        print(f"❌ {result.get('reason', result.get('error', '查询失败'))}")
        return

    detail = result.get("detail", {})
    content = result.get("content", "")

    print(f"📰 {detail.get('title', '未知标题')}")
    print(f"分类: {detail.get('category', '-')} | 来源: {detail.get('author_name', '-')} | 时间: {detail.get('date', '-')}")
    print(f"原文: {detail.get('url', '-')}")
    print()
    print("--- 正文 ---")
    print(content.strip() or "（无正文内容）")


def main():
    args = sys.argv[1:]
    cli_key = None
    type_ = "top"
    page = 1
    page_size = 30
    is_filter = 0
    detail_uniquekey = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        if args[i] == "--type" and i + 1 < len(args):
            type_ = args[i + 1].lower()
            args = args[:i] + args[i + 2:]
            continue
        if args[i] == "--page" and i + 1 < len(args):
            try:
                page = int(args[i + 1])
            except ValueError:
                pass
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--page-size", "--page_size") and i + 1 < len(args):
            try:
                page_size = int(args[i + 1])
            except ValueError:
                pass
            args = args[:i] + args[i + 2:]
            continue
        if args[i] == "--filter" and i + 1 < len(args):
            is_filter = 1 if args[i + 1] in ("1", "true", "yes") else 0
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--detail", "-d") and i + 1 < len(args):
            detail_uniquekey = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        i += 1

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_NEWS_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_NEWS_KEY=your_api_key")
        print("   3. 命令行参数: python news_headlines.py --key your_api_key --type top")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    if detail_uniquekey:
        result = query_detail(api_key, detail_uniquekey)
        format_detail_output(result)
        print()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = query_list(api_key, type_, page, page_size, is_filter)
        format_list_output(result, type_)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
