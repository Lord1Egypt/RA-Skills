#!/usr/bin/env python3
"""
Naver Booking/Local Search Script
네이버 예약 및 장소 정보를 조회합니다.
"""

import sys
import os
import argparse
# Add lib directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
from naver_base import perform_search, format_output

def compact_formatter(results):
    output = []
    
    # 1. Booking Results (Specialized)
    bookings = results.get("booking_results", [])
    if bookings:
        output.append(f"🎫 네이버 예약 상품 ({len(bookings)}개)")
        output.append("=" * 30)
        for i, res in enumerate(bookings[:5], 1):
            price = f" | 💰 {res.get('price')}" if res.get('price') else ""
            output.append(f"{i}. {res.get('title')}{price}")
            if res.get('link'):
                output.append(f"   🔗 {res.get('link')}")
            output.append("")

    # 2. Local Results (Places)
    local = results.get("local_results", [])
    if local:
        if output: output.append("-" * 30 + "\n")
        output.append(f"📍 네이버 장소 결과 ({len(local)}개)")
        output.append("=" * 30)
        for i, res in enumerate(local[:10], 1):
            title = res.get('title')
            category = res.get('type')
            address = res.get('address')
            
            output.append(f"{i}. {title} ({category})")
            if address:
                output.append(f"   🏠 {address}")
            if res.get('link'):
                output.append(f"   🔗 {res.get('link')}")
            output.append("")

    if not output:
        return "예약 또는 장소 관련 정보를 찾을 수 없습니다. (일반 검색어에 정보를 포함하여 다시 시도해 보세요.)"
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Naver Booking/Local Search")
    parser.add_argument("query", help="검색어 (예: 강남역 맛집, 서울 호텔 예약)")
    parser.add_argument("-f", "--format", default="compact", choices=["compact", "full", "json"])
    args = parser.parse_args()

    query = args.query
    # '예약' 키워드가 없으면 보강하여 결과 유도 (단, nexearch 특성을 고려)
    if "예약" not in query and "맛집" not in query and "카페" not in query:
        query = f"{args.query} 예약"

    params = {
        "engine": "naver",
        "query": query,
        "where": "nexearch" # 네이버 로컬/예약 정보는 통합검색(nexearch) 결과에 포함됨
    }
    
    results = perform_search(params)
    print(format_output(results, args.format, compact_formatter))

if __name__ == "__main__":
    main()
