#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from openviking_korean.client import OpenVikingKorean

client = OpenVikingKorean()
results = client.find("""오늘 작업""", level=0)

print("=== Context DB 검색 결과 ===")
for r in results[:3]:
    print(f"{r['uri']}: {r['abstract'][:50]}...")