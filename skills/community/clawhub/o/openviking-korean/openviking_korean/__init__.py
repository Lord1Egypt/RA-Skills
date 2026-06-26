#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TokenSaver (토큰세이버) - Korean Context DB for AI Agents
한국어 Context DB for AI Agents

95-96% AI Cost Reduction for Korean | 한국어 95-96% 비용 절약
85-90% AI Cost Reduction for English | 영어 85-90% 비용 절약

Quick Start / 빠른 시작:
    from openviking_korean import TokenSaver
    client = TokenSaver()
    client.save("memo/1", "Important content", level=2)
    results = client.find("important")

Features / 주요 기능:
- Bilingual: Korean + English optimized / 한영겸용 최적화
- JVM-Free: Pure Python tokenizer (no Java required) / Java 없는 순수 Python
- 4-Level Compression: L0(99%) L1(96%) L2(91%) L3(original) / 4단계 압축
- Async batch processing / 비동기 배치 처리
- Export/Import with backup / 백업 익스포트/임포트
- Auto-compression scheduler / 자동 압축 스케줄러

Install / 설치:
    pip install tokensaver
    pip install tokensaver[speed]  # with orjson + aiofiles
"""

from openviking_korean.client import OpenVikingKorean, Context, ContextStore
from openviking_korean.tokenizer import KoreanTokenizer, create_default_tokenizer
from openviking_korean.vector_store import VectorStore, create_vector_store
from openviking_korean.auto_sync import AutoSync, create_auto_sync

# v3.1 새로운 클래스들 (TokenSaver)
try:
    from openviking_korean.v3 import (
        TokenSaver,                    # Main client / 메인 클라이언트
        TokenSaverV3,                  # Alias / 별칭
        PurePythonKoreanTokenizer,     # JVM-free tokenizer / Java 없는 토크나이저
        MultiLevelCompressor,          # 4-level compression / 4단계 압축
        CompressionResult,             # Compression stats / 압축 통계
        SearchResult,                  # Search result / 검색 결과
        BatchResult                    # Batch result / 배치 결과
    )
    V3_AVAILABLE = True
except ImportError as e:
    V3_AVAILABLE = False
    print(f"[TokenSaver] v3.1 not available: {e}")

__version__ = "3.1.0"
__version_info__ = (3, 1, 0)
__author__ = "ClawHub"

__all__ = [
    # 메인 (v3.1 - 토큰세이버)
    "TokenSaver",
    "TokenSaverV3",
    
    # 타입 지원 클래스들
    "CompressionResult",
    "SearchResult",
    "BatchResult",
    
    # 하위호환 (v2.x)
    "OpenVikingKorean",
    "Context",
    "ContextStore",
    
    # 토크나이저
    "KoreanTokenizer",
    "create_default_tokenizer",
    "PurePythonKoreanTokenizer",
    
    # 압축
    "MultiLevelCompressor",
    
    # 벡터 검색
    "VectorStore",
    "create_vector_store",
    
    # 자동 동기화
    "AutoSync",
    "create_auto_sync",
    
    # 버전 정보
    "__version__",
    "__version_info__",
]