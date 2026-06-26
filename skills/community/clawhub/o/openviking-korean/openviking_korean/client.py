#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenViking Korean - 한국어 Context DB 클라이언트

토큰 절감 91% 달성을 위한 한국어 최적화 클라이언트
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# 한국어 형태소 분석 (선택적)
try:
    from konlpy.tag import Okt
    KONLPY_AVAILABLE = True
except ImportError:
    KONLPY_AVAILABLE = False


@dataclass
class Context:
    """Context 객체"""
    uri: str
    abstract: str = ""
    content: str = ""
    level: int = 2  # L0=abstract, L1=overview, L2=detail
    category: str = "general"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    meta: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "abstract": self.abstract,
            "content": self.content,
            "level": self.level,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "meta": self.meta
        }


class KoreanTokenizer:
    """한국어 토크나이저 - 토큰 절감 최적화"""
    
    def __init__(self):
        self.okt = Okt() if KONLPY_AVAILABLE else None
    
    def tokenize(self, text: str) -> List[str]:
        """한국어 형태소 분석 기반 토큰화"""
        if self.okt:
            # 형태소 분석으로 불필요한 토큰 제거
            tokens = self.okt.morphs(text, stem=True)
            # 조사, 어미 등 불필요한 토큰 필터링
            filtered = [t for t in tokens if len(t) > 1]
            return filtered
        else:
            # 기본 공백 분할
            return text.split()
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """핵심 키워드 추출"""
        tokens = self.tokenize(text)
        # 빈도 기반 키워드 추출
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_tokens[:top_n]]


class ContextStore:
    """Context 저장소 - 파일시스템 기반"""
    
    def __init__(self, base_path: str = "~/.openviking/korean"):
        self.base_path = Path(base_path).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 카테고리 디렉토리 생성
        for category in ["memories", "resources", "skills"]:
            (self.base_path / category).mkdir(exist_ok=True)
    
    def save(self, context: Context) -> bool:
        """Context 저장"""
        # URI에서 파일 경로 생성
        path = self._uri_to_path(context.uri)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # JSON으로 저장
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(context.to_dict(), f, ensure_ascii=False, indent=2)
        
        return True
    
    def load(self, uri: str, level: int = 2) -> Optional[Context]:
        """Context 로드 (계층적)"""
        path = self._uri_to_path(uri)
        
        if not path.exists():
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 레벨에 따른 내용 로드
        context = Context(**data)
        if level == 0:
            context.content = context.abstract
        elif level == 1:
            # 개요만 로드 (구현 필요)
            context.content = self._get_overview(context)
        # level == 2: 전체 내용
        
        return context
    
    def search(self, query: str, category: Optional[str] = None) -> List[Context]:
        """한국어 검색"""
        results = []
        search_path = self.base_path / category if category else self.base_path
        
        # 한국어 토크나이저로 키워드 추출
        tokenizer = KoreanTokenizer()
        keywords = tokenizer.extract_keywords(query)
        
        # 파일 검색
        for file in search_path.rglob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 키워드 매칭
            text = f"{data['abstract']} {data.get('content', '')}"
            if any(kw in text for kw in keywords):
                results.append(Context(**data))
        
        return results
    
    def _uri_to_path(self, uri: str) -> Path:
        """URI를 파일 경로로 변환"""
        # viking://memories/프로젝트/마케팅.md -> memories/프로젝트/마케팅.json
        if uri.startswith("viking://"):
            uri = uri[9:]  # viking:// 제거
        return self.base_path / f"{uri}.json"
    
    def _get_overview(self, context: Context) -> str:
        """개요 생성 (L1)"""
        # 간단한 개요 생성 로직
        lines = context.content.split('\n')
        overview_lines = lines[:10]  # 첫 10줄
        return '\n'.join(overview_lines)


class OpenVikingKorean:
    """OpenViking Korean 메인 클래스"""
    
    def __init__(self, config_path: str = "~/.openviking/ovk.conf"):
        self.config_path = Path(config_path).expanduser()
        self.config = self._load_config()
        self.store = ContextStore()
        self.tokenizer = KoreanTokenizer()
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 로드"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "language": "ko",
            "token_optimization": {
                "enabled": True,
                "target_reduction": 0.91
            }
        }
    
    def save_memory(self, uri: str, content: str, category: str = "memories") -> bool:
        """기억 저장"""
        # 한국어 요약 생성
        abstract = self._generate_abstract(content)
        
        context = Context(
            uri=f"{category}/{uri}",
            abstract=abstract,
            content=content,
            category=category
        )
        
        return self.store.save(context)
    
    def find(self, query: str, category: Optional[str] = None, level: int = 2) -> List[Dict[str, Any]]:
        """Context 검색"""
        results = self.store.search(query, category)
        
        # 토큰 절감을 위해 레벨에 따른 내용 반환
        return [
            {
                "uri": r.uri,
                "abstract": r.abstract,
                "content": r.content if level == 2 else r.abstract,
                "category": r.category,
                "relevance": self._calculate_relevance(query, r)
            }
            for r in results
        ]
    
    def abstract(self, uri: str) -> str:
        """L0 요약 반환"""
        context = self.store.load(uri, level=0)
        return context.abstract if context else ""
    
    def overview(self, uri: str) -> str:
        """L1 개요 반환"""
        context = self.store.load(uri, level=1)
        return context.content if context else ""
    
    def read(self, uri: str) -> str:
        """L2 전체 내용 반환"""
        context = self.store.load(uri, level=2)
        return context.content if context else ""
    
    def compress_memory(self, content: str) -> str:
        """기억 압축 - 토큰 절감"""
        # 한국어 간결화 로직
        # 1. 불필요한 서술 제거
        # 2. 핵심 정보만 유지
        # 3. 50% 이하로 압축
        
        # 간단한 구현: 첫 500자
        compressed = content[:500]
        
        # 토큰 절감률 계산
        original_tokens = len(content.split())
        compressed_tokens = len(compressed.split())
        reduction = 1 - (compressed_tokens / original_tokens)
        
        print(f"토큰 절감: {reduction:.1%}")
        
        return compressed
    
    def _generate_abstract(self, content: str) -> str:
        """한국어 요약 생성"""
        # 키워드 기반 간단한 요약
        keywords = self.tokenizer.extract_keywords(content, top_n=5)
        abstract = f"[{'/'.join(keywords)}] {content[:100]}..."
        return abstract
    
    def _calculate_relevance(self, query: str, context: Context) -> float:
        """관련도 계산"""
        query_keywords = set(self.tokenizer.extract_keywords(query))
        content_keywords = set(self.tokenizer.extract_keywords(context.content))
        
        if not query_keywords or not content_keywords:
            return 0.0
        
        intersection = query_keywords & content_keywords
        union = query_keywords | content_keywords
        
        return len(intersection) / len(union)


# CLI 진입점
def main():
    """CLI 메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenViking Korean CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # find 명령어
    find_parser = subparsers.add_parser("find", help="Context 검색")
    find_parser.add_argument("query", help="검색 쿼리")
    find_parser.add_argument("--category", "-c", help="카테고리 필터")
    find_parser.add_argument("--level", "-l", type=int, default=2, help="Context 레벨 (0=abstract, 1=overview, 2=detail)")
    
    # save 명령어
    save_parser = subparsers.add_parser("save", help="Context 저장")
    save_parser.add_argument("uri", help="저장 URI")
    save_parser.add_argument("--content", "-c", required=True, help="내용")
    save_parser.add_argument("--category", "-C", default="memories", help="카테고리")
    
    # read 명령어
    read_parser = subparsers.add_parser("read", help="Context 읽기")
    read_parser.add_argument("uri", help="읽을 URI")
    
    # abstract 명령어
    abstract_parser = subparsers.add_parser("abstract", help="L0 요약")
    abstract_parser.add_argument("uri", help="URI")
    
    # overview 명령어
    overview_parser = subparsers.add_parser("overview", help="L1 개요")
    overview_parser.add_argument("uri", help="URI")
    
    args = parser.parse_args()
    
    client = OpenVikingKorean()
    
    if args.command == "find":
        results = client.find(args.query, args.category, args.level)
        for r in results:
            print(f"[{r['relevance']:.2f}] {r['uri']}")
            print(f"  {r['abstract']}")
    
    elif args.command == "save":
        client.save_memory(args.uri, args.content, args.category)
        print(f"저장 완료: {args.uri}")
    
    elif args.command == "read":
        content = client.read(args.uri)
        print(content)
    
    elif args.command == "abstract":
        abstract = client.abstract(args.uri)
        print(abstract)
    
    elif args.command == "overview":
        overview = client.overview(args.uri)
        print(overview)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()