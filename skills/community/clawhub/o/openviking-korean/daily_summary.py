#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context DB Daily Summary Generator
매일 아침 실행해서 L0 요약을 파일로 저장
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openviking_korean.client import OpenVikingKorean

def generate_daily_summary():
    client = OpenVikingKorean()
    
    # 핵심 키워드 검색
    keywords = ['마스터', '닥터레이디', '영양제', '목표', '오늘 작업']
    
    summary_lines = ["# Context DB Daily Summary (L0)", f"생성: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    
    for kw in keywords:
        results = client.find(kw, level=0)
        if results:
            summary_lines.append(f"## {kw}")
            for r in results[:2]:
                summary_lines.append(f"- {r['abstract'][:80]}...")
            summary_lines.append("")
    
    # 파일 저장
    output_path = os.path.expanduser("~/.openclaw/workspace/context-summary.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"저장 완료: {output_path}")
    print(f"토큰: {len('\\n'.join(summary_lines)) // 2}")

if __name__ == "__main__":
    generate_daily_summary()