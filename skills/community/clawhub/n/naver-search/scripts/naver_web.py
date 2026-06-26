#!/usr/bin/env python3
import sys
import os
import argparse

# Add lib directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
from naver_base import perform_search, format_output

def compact_formatter(results):
    output = []
    
    # AI Overview
    if "ai_overview" in results:
        output.append("🤖 AI 요약")
        output.append("=" * 30)
        output.append(results['ai_overview'].get('text', '내용 없음'))
        output.append("-" * 30 + "\n")

    # Ads
    ads = results.get("ads_results", results.get("ads"))
    if ads:
        output.append(f"📢 광고 ({len(ads)}개)")
        for ad in ads[:3]:
            output.append(f"· {ad.get('title')}")
            output.append(f"  🔗 {ad.get('link')}")
        output.append("")

    # Web/Organic results
    organic = results.get("web_results", results.get("organic_results"))
    if organic:
        output.append(f"📊 웹 검색 결과 ({len(organic)}개)")
        for i, res in enumerate(organic[:10], 1):
            output.append(f"{i}. {res.get('title')}")
            output.append(f"   🔗 {res.get('link')}")
            if res.get('snippet'):
                output.append(f"   📝 {res.get('snippet')}")
        output.append("")

    # Related queries
    related_list = results.get("related_queries", results.get("related_results", []))
    if related_list:
        related = ", ".join([r.get('query', '') for r in related_list[:8]])
        if related:
            output.append(f"🔍 관련 검색어: {related}")

    return "\n".join(output) if output else "검색 결과가 없습니다."

def main():
    parser = argparse.ArgumentParser(description="Naver Web/Integrated Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-p", "--page", type=int, default=1, help="Page number")
    parser.add_argument("-f", "--format", default="compact", choices=["compact", "full", "json"])
    args = parser.parse_args()

    params = {
        "engine": "naver",
        "query": args.query,
        "where": "nexearch",
        "page": args.page
    }
    
    results = perform_search(params)
    print(format_output(results, args.format, compact_formatter))

if __name__ == "__main__":
    main()
