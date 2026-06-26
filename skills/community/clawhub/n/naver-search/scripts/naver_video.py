#!/usr/bin/env python3
import sys
import os
import argparse

# Add lib directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
from naver_base import perform_search, format_output

def compact_formatter(results):
    output = []
    videos = results.get("video_results")
    if videos:
        output.append(f"🎥 네이버 비디오 검색 결과 ({len(videos)}개)")
        output.append("=" * 30)
        for i, res in enumerate(videos[:10], 1):
            video_info = res.get('video_info', {})
            source = res.get('source', '알 수 없음')
            duration = res.get('duration', '')
            
            duration_info = f" | {duration}" if duration else ""
            output.append(f"{i}. {res.get('title')}")
            output.append(f"   📺 {source}{duration_info}")
            output.append(f"   🔗 {res.get('link')}")
            output.append("")
    
    return "\n".join(output) if output else "비디오 검색 결과가 없습니다."

def main():
    parser = argparse.ArgumentParser(description="Naver Video Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-p", "--page", type=int, default=1, help="Page number")
    parser.add_argument("-f", "--format", default="compact", choices=["compact", "full", "json"])
    args = parser.parse_args()

    params = {
        "engine": "naver",
        "query": args.query,
        "where": "video",
        "page": args.page
    }
    
    results = perform_search(params)
    print(format_output(results, args.format, compact_formatter))

if __name__ == "__main__":
    main()
