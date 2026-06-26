#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보라의 Context DB 초기화
MEMORY.md, USER.md, SOUL.md를 OpenViking Korean에 저장
"""

import sys
import os
sys.path.insert(0, r"C:\Users\Roken\.openclaw\workspace\_auai-engine\openviking-korean")

from openviking_korean.client import OpenVikingKorean, Context

def main():
    print("🧠 보라의 Context DB 초기화 시작\n")
    
    # 클라이언트 초기화
    client = OpenVikingKorean()
    
    # 저장할 파일들
    files = [
        {
            "uri": "memories/보라/MEMORY",
            "content": open(r"C:\Users\Roken\.openclaw\workspace\MEMORY.md", encoding="utf-8").read(),
            "category": "memories"
        },
        {
            "uri": "memories/보라/USER",
            "content": open(r"C:\Users\Roken\.openclaw\workspace\USER.md", encoding="utf-8").read(),
            "category": "memories"
        },
        {
            "uri": "memories/보라/SOUL",
            "content": open(r"C:\Users\Roken\.openclaw\workspace\SOUL.md", encoding="utf-8").read(),
            "category": "memories"
        },
        {
            "uri": "memories/보라/AGENTS",
            "content": open(r"C:\Users\Roken\.openclaw\workspace\AGENTS.md", encoding="utf-8").read(),
            "category": "memories"
        },
        {
            "uri": "memories/보라/IDENTITY",
            "content": open(r"C:\Users\Roken\.openclaw\workspace\IDENTITY.md", encoding="utf-8").read(),
            "category": "memories"
        }
    ]
    
    total_original = 0
    total_abstract = 0
    
    for f in files:
        try:
            # 토큰 카운트
            original_tokens = len(f["content"]) // 2
            
            # 저장
            client.save_memory(f["uri"], f["content"], f["category"])
            
            # 요약 토큰
            abstract = client.abstract(f"memories/{f['uri'].split('/')[-1]}")
            abstract_tokens = len(abstract) // 2
            
            print(f"✅ 저장 완료: {f['uri']}")
            print(f"   원본 토큰: {original_tokens:,}")
            print(f"   요약 토큰: {abstract_tokens:,}")
            print(f"   절감률: {(1 - abstract_tokens/original_tokens)*100:.1f}%\n")
            
            total_original += original_tokens
            total_abstract += abstract_tokens
            
        except Exception as e:
            print(f"❌ 오류: {f['uri']} - {e}\n")
    
    print("=" * 60)
    print("📊 전체 결과")
    print("=" * 60)
    print(f"총 원본 토큰: {total_original:,}")
    print(f"총 요약 토큰: {total_abstract:,}")
    print(f"평균 절감률: {(1 - total_abstract/total_original)*100:.1f}%")
    
    # 검색 테스트
    print("\n" + "=" * 60)
    print("🔍 검색 테스트")
    print("=" * 60)
    
    queries = ["마스터", "닥터레이디", "영양제", " Threads"]
    for query in queries:
        results = client.find(query, level=0)  # L0만
        if results:
            print(f"\n쿼리: '{query}'")
            print(f"  결과: {len(results)}개")
            for r in results[:2]:
                print(f"  - {r['uri']}: {r['abstract'][:50]}...")
    
    print("\n✅ Context DB 초기화 완료!")

if __name__ == "__main__":
    main()