#!/usr/bin/env python3
"""
Generate Intel Report — 生成结构化情报简报
用法: python3 generate_intel_report.py --query "<关键词>" [--max-results N] [--language zh|en] [--output <文件>]
"""

import argparse
import json
import os
import sys
from datetime import datetime


def search(query: str, api_key: str, max_results: int, topic: str = "general",
           search_depth: str = "basic") -> dict:
    try:
        from tavily import TavilyClient
    except ImportError:
        return {"error": "tavily-python not installed. Run: pip install tavily-python"}

    if not api_key:
        return {"error": "TAVILY_API_KEY not set"}

    try:
        client = TavilyClient(api_key=api_key)
        result = client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            max_results=max_results,
            include_answer=True
        )
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def detect_industry(query: str) -> str:
    """从查询关键词推断行业名称。"""
    query_lower = query.lower()
    industries = {
        "AI": ["AI", "人工智能", "LLM", "GPT", "大模型", "AIGC", "生成式"],
        "电商": ["电商", "跨境", "Shopify", "亚马逊", "天猫", "京东"],
        "科技": ["科技", "互联网", "IT", "软件"],
        "金融": ["金融", "银行", "保险", "投资", "区块链"],
        "医疗": ["医疗", "健康", "医药", "生物"],
        "教育": ["教育", "培训", "在线教育"],
    }
    for industry, keywords in industries.items():
        if any(kw.lower() in query_lower for kw in keywords):
            return industry
    return "行业"


def build_report(query: str, results: list, ai_answer: str, language: str = "zh") -> str:
    """构建 Markdown 格式情报简报。"""
    today = datetime.now().strftime("%Y-%m-%d")
    industry = detect_industry(query)

    lines = [
        f"# {industry} 情报简报",
        f"**日期**: {today}",
        f"**关键词**: {query}",
        "",
    ]

    if ai_answer:
        lines.append("## 今日要点")
        lines.append("")
        lines.append(ai_answer)
        lines.append("")

    if results:
        lines.append("## 热门资讯")
        lines.append("")
        for i, r in enumerate(results, 1):
            title = r.get("title", "无标题")
            url = r.get("url", "")
            content = r.get("content", "")
            # 截取摘要
            snippet = content[:300] + ("..." if len(content) > 300 else "")
            lines.append(f"**{i}. {title}**")
            lines.append(f"链接: {url}")
            lines.append(f"{snippet}")
            lines.append("")

    lines.append("## 来源列表")
    lines.append("")
    seen = set()
    for r in results:
        url = r.get("url", "")
        title = r.get("title", "")
        if url and url not in seen:
            seen.add(url)
            lines.append(f"- [{title}]({url})")

    lines.append("")
    lines.append("---")
    lines.append(f"*由 industry-intel-assistant 自动生成 | {today}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成行业情报简报")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--max-results", type=int, default=8, help="结果数量 (1-10)")
    parser.add_argument("--language", default="zh", choices=["zh", "en"],
                        help="简报语言")
    parser.add_argument("--topic", default="general", choices=["general", "news"],
                        help="搜索主题")
    parser.add_argument("--depth", default="advanced", choices=["basic", "advanced"],
                        help="搜索深度")
    parser.add_argument("--output", default="", help="输出文件路径 (默认打印到 stdout)")
    parser.add_argument("--api-key", default=os.environ.get("TAVILY_API_KEY", ""),
                        help="Tavily API Key")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: TAVILY_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print(f"正在搜索: {args.query} ...")
    result = search(
        query=args.query,
        api_key=args.api_key,
        max_results=args.max_results,
        topic=args.topic,
        search_depth=args.depth
    )

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    data = result["data"]
    report = build_report(
        query=args.query,
        results=data.get("results", []),
        ai_answer=data.get("answer", ""),
        language=args.language
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"简报已保存: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
