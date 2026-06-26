#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보라 Context DB 자동 로드
세션 시작 시 자동으로 관련 Context 검색
"""

import sys
sys.path.insert(0, r"C:\Users\Roken\.openclaw\workspace\_auai-engine\openviking-korean")

from openviking_korean.client import OpenVikingKorean

def auto_recall(query: str):
    """자동 회상 - 쿼리에 따른 Context 검색"""
    client = OpenVikingKorean()
    # 엔터(\n)를 실제 줄바꿈이 아니라 '\n'이라는 글자 자체로 바꿔버려서
    # 파이썬 코드가 여러 줄로 쪼개지는 것을 원천 차단합니다.
    safe_query = str(query).replace('\n', '\\n').replace('\r', '').replace('"', '\\"')
    
    # 에러 핸들링 추가 - Gateway에서 잘못된 형식의 쿼리 전달 시 대비
    try:
        results = client.find(safe_query, level=0)
    except Exception as e:
        print(f"⚠️ 검색 중 오류 발생: {e}")
        print(f"⚠️ 문제 쿼리: {safe_query[:100]}...")
        results = []
    
    if results:
        print(f"\n🔍 '{query}' 관련 Context:")
        for r in results[:3]:
            print(f"  - {r['uri']}")
            print(f"    {r['abstract'][:100]}...")
    else:
        print(f"검색 결과 없음: '{query}'")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="검색 쿼리")
    args = parser.parse_args()
    auto_recall(args.query)