#!/usr/bin/env python3
"""
Tavily Industry Search — 行业资讯搜索脚本
用法: python3 tavily_industry_search.py "<关键词>" [--max-results N] [--topic general|news] [--depth basic|advanced]
"""

import argparse
import json
import os
import sys


def search_industry_news(query: str, api_key: str, max_results: int = 5,
                         topic: str = "general", search_depth: str = "basic") -> dict:
    """执行 Tavily 搜索并返回结构化结果。"""
    try:
        from tavily import TavilyClient
    except ImportError:
        return {
            "error": "tavily-python not installed. Run: pip install tavily-python",
            "install_hint": "pip install tavily-python --break-system-packages"
        }

    if not api_key:
        return {"error": "TAVILY_API_KEY environment variable not set"}

    try:
        client = TavilyClient(api_key=api_key)
        result = client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            max_results=max_results,
            include_answer=True,
            include_raw_content=False
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def format_results(results: list) -> str:
    """将搜索结果格式化为易读文本。"""
    lines = []
    for i, r in enumerate(results, 1):
        title = r.get("title", "无标题")
        url = r.get("url", "")
        content = r.get("content", "")[:200]
        score = r.get("score", 0)
        lines.append(f"{i}. {title}")
        lines.append(f"   链接: {url}")
        lines.append(f"   摘要: {content}...")
        lines.append(f"   相关度: {score:.2f}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Tavily 行业资讯搜索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--max-results", type=int, default=5, help="返回结果数量 (1-10)")
    parser.add_argument("--topic", default="general", choices=["general", "news"],
                        help="搜索主题: general=全网, news=最近7天新闻")
    parser.add_argument("--depth", default="basic", choices=["basic", "advanced"],
                        help="搜索深度: basic=快速, advanced=深度")
    parser.add_argument("--api-key", default=os.environ.get("TAVILY_API_KEY", ""),
                        help="Tavily API Key (也可通过 TAVILY_API_KEY 环境变量设置)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: No API key. Set TAVILY_API_KEY env var or pass --api-key", file=sys.stderr)
        sys.exit(1)

    result = search_industry_news(
        query=args.query,
        api_key=args.api_key,
        max_results=args.max_results,
        topic=args.topic,
        search_depth=args.depth
    )

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        if "install_hint" in result:
            print(result["install_hint"], file=sys.stderr)
        sys.exit(1)

    data = result["data"]

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    # 格式化输出
    if data.get("answer"):
        print(f"=== AI 摘要 ===")
        print(data["answer"])
        print()

    results = data.get("results", [])
    print(f"=== 搜索结果 ({len(results)} 条) ===")
    print()
    print(format_results(results))


if __name__ == "__main__":
    main()
