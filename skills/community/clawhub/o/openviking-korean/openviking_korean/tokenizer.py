#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenViking Korean - 한국어 형태소 분석 모듈

konlpy 기반 최적화된 토크나이저
"""

import re
from typing import List, Dict, Set, Optional, Tuple
from collections import Counter
import json
from pathlib import Path

try:
    from konlpy.tag import Okt, Mecab
    KONLPY_AVAILABLE = True
except ImportError:
    KONLPY_AVAILABLE = False


# 한국어 불용어 목록
KOREAN_STOPWORDS = {
    # 조사
    '은', '는', '이', '가', '을', '를', '에', '의', '와', '과', '도', '만', '까지', '부터',
    '으로', '로', '에서', '에게', '한테', '보다', '처럼', '만큼', '뿐', '뿐만', '외', '외에',
    
    # 어미
    '다', '니다', '해요', '하세요', '했습니다', '합니다', '이다', '하다', '되다', '있다', '없다',
    '했다', '했다가', '하니', '해서', '하여', '하면', '하며', '하면서', '하고', '하니까',
    
    # 의존 명사
    '것', '수', '뿐', '뿐만', '데', '적', '바', '줄', '만', '뿐', '채', '듯', '듯이', '성', '분',
    
    # 일반적인 무의미 단어
    '그', '이', '저', '것', '등', '들', '및', '또', '또한', '그리고', '그러나', '그래서',
    '그러면', '그러므로', '그런데', '하지만', '따라서', '왜냐하면', '즉', '예를', '들면',
    
    # 숫자/영어 (선택적)
    # '1', '2', '3', 'one', 'two', 'three'
}

# 한국어 동의어 사전 (간단 버전)
KOREAN_SYNONYMS = {
    '마케팅': ['광고', '홍보', '판촉', '프로모션'],
    '광고': ['마케팅', '홍보', '광고물'],
    '매출': ['수익', '수입', '판매액', '실적'],
    '수익': ['매출', '이익', '소득', '수입'],
    '고객': ['소비자', '유저', '사용자', '구매자'],
    '제품': ['상품', '아이템', '물건', '아이템'],
    '프로젝트': ['과제', '작업', '태스크', '일'],
    '개발': ['구현', '제작', '만들기', '생성'],
    '비즈니스': ['사업', '영업', '장사', '비지니스'],
    '전략': ['계획', '방안', '대책', '전술'],
}


class KoreanTokenizer:
    """한국어 토크나이저 - 토큰 절감 최적화"""
    
    def __init__(self, 
                 use_mecab: bool = False,
                 min_token_length: int = 2,
                 use_synonyms: bool = True):
        """
        Args:
            use_mecab: Mecab 사용 여부 (더 정확하지만 설치 필요)
            min_token_length: 최소 토큰 길이
            use_synonyms: 동의어 확장 사용 여부
        """
        self.min_token_length = min_token_length
        self.use_synonyms = use_synonyms
        
        if KONLPY_AVAILABLE:
            if use_mecab:
                try:
                    self.tagger = Mecab()
                except:
                    try:
                        self.tagger = Okt()
                    except:
                        self.tagger = None
            else:
                try:
                    self.tagger = Okt()
                except:
                    self.tagger = None
        else:
            self.tagger = None
        
        # 불용어 로드
        self.stopwords = KOREAN_STOPWORDS.copy()
        
        # 동의어 로드
        self.synonyms = KOREAN_SYNONYMS.copy()
        
        # 사용자 정의 사전
        self.user_words: Set[str] = set()
    
    def add_stopwords(self, words: List[str]):
        """불용어 추가"""
        self.stopwords.update(words)
    
    def add_synonyms(self, word: str, synonyms: List[str]):
        """동의어 추가"""
        if word in self.synonyms:
            self.synonyms[word].extend(synonyms)
        else:
            self.synonyms[word] = synonyms
    
    def add_user_words(self, words: List[str]):
        """사용자 정의 단어 추가"""
        self.user_words.update(words)
    
    def tokenize(self, text: str, pos_filter: List[str] = None) -> List[str]:
        """
        한국어 형태소 분석 기반 토큰화
        
        Args:
            text: 입력 텍스트
            pos_filter: 유지할 품사 목록 (예: ['Noun', 'Verb', 'Adjective'])
        
        Returns:
            토큰 리스트
        """
        if self.tagger is None:
            # 기본 공백 분할
            return self._simple_tokenize(text)
        
        # 품사 필터 기본값
        if pos_filter is None:
            pos_filter = ['Noun', 'Verb', 'Adjective', 'Alpha']  # 명사, 동사, 형용사, 영어
        
        # 형태소 분석
        if isinstance(self.tagger, Okt):
            # Okt: morphs() 사용
            pos_tags = self.tagger.pos(text, stem=True)
            tokens = [word for word, pos in pos_tags 
                     if pos in pos_filter and len(word) >= self.min_token_length]
        else:
            # Mecab: nouns(), verbs() 등 사용
            nouns = self.tagger.nouns(text)
            tokens = [n for n in nouns if len(n) >= self.min_token_length]
        
        # 불용어 제거
        tokens = [t for t in tokens if t not in self.stopwords]
        
        # 사용자 정의 단어 추가
        for word in self.user_words:
            if word in text and word not in tokens:
                tokens.append(word)
        
        return tokens
    
    def _simple_tokenize(self, text: str) -> List[str]:
        """간단한 토큰화 (konlpy 없을 때)"""
        # 공백 분할
        tokens = text.split()
        
        # 특수문자 제거
        tokens = [re.sub(r'[^가-힣a-zA-Z0-9]', '', t) for t in tokens]
        
        # 길이 필터
        tokens = [t for t in tokens if len(t) >= self.min_token_length]
        
        # 불용어 제거
        tokens = [t for t in tokens if t not in self.stopwords]
        
        return tokens
    
    def extract_keywords(self, 
                        text: str, 
                        top_n: int = 10,
                        use_tfidf: bool = False) -> List[Tuple[str, float]]:
        """
        핵심 키워드 추출
        
        Args:
            text: 입력 텍스트
            top_n: 상위 n개 키워드
            use_tfidf: TF-IDF 사용 여부
        
        Returns:
            (키워드, 점수) 튜플 리스트
        """
        tokens = self.tokenize(text)
        
        # 빈도 계산
        freq = Counter(tokens)
        
        # 동의어 확장 점수
        if self.use_synonyms:
            for token, count in list(freq.items()):
                if token in self.synonyms:
                    for syn in self.synonyms[token]:
                        if syn in freq:
                            freq[token] += freq[syn] * 0.5
        
        # 정렬
        sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_tokens[:top_n]
    
    def expand_query(self, query: str) -> List[str]:
        """
        쿼리 확장 (동의어 포함)
        
        Args:
            query: 원본 쿼리
        
        Returns:
            확장된 쿼리 토큰 리스트
        """
        tokens = self.tokenize(query)
        expanded = set(tokens)
        
        # 동의어 추가
        for token in tokens:
            if token in self.synonyms:
                expanded.update(self.synonyms[token])
        
        return list(expanded)
    
    def get_word_score(self, word: str) -> float:
        """
        단어 중요도 점수
        
        Args:
            word: 단어
        
        Returns:
            점수 (0.0 ~ 1.0)
        """
        # 기본 점수
        score = 1.0
        
        # 길이 보정 (긴 단어일수록 중요)
        score *= min(len(word) / 5.0, 1.5)
        
        # 동의어 존재 시 보정 (여러 의미로 쓰이면 중요)
        if word in self.synonyms:
            score *= 1.2
        
        # 불용어면 0점
        if word in self.stopwords:
            score = 0.0
        
        return min(score, 1.0)
    
    def create_search_pattern(self, query: str) -> Dict[str, Any]:
        """
        검색 패턴 생성
        
        Args:
            query: 검색 쿼리
        
        Returns:
            검색 패턴 딕셔너리
        """
        tokens = self.tokenize(query)
        keywords = self.extract_keywords(query, top_n=5)
        expanded = self.expand_query(query)
        
        return {
            "original_query": query,
            "tokens": tokens,
            "keywords": [k[0] for k in keywords],
            "expanded_tokens": expanded,
            "search_regex": '|'.join(expanded),  # 정규식용
            "must_have": [k[0] for k in keywords[:2]]  # 반드시 포함
        }
    
    def save_user_dict(self, path: str):
        """사용자 사전 저장"""
        data = {
            "stopwords": list(self.stopwords),
            "synonyms": self.synonyms,
            "user_words": list(self.user_words)
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_user_dict(self, path: str):
        """사용자 사전 로드"""
        p = Path(path)
        if not p.exists():
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.stopwords.update(data.get('stopwords', []))
        self.synonyms.update(data.get('synonyms', {}))
        self.user_words.update(data.get('user_words', []))


def create_default_tokenizer() -> KoreanTokenizer:
    """기본 토크나이저 생성"""
    tokenizer = KoreanTokenizer(
        use_mecab=False,
        min_token_length=2,
        use_synonyms=True
    )
    
    # OpenClaw 특화 단어 추가
    tokenizer.add_user_words([
        '보라', '마스터', 'AUAI', 'ROKEN', 'OpenViking', 'ClawHub',
        'Dr.Lady', '바른연구소', '닥터레이디', '메모리', '컨텍스트'
    ])
    
    return tokenizer


if __name__ == "__main__":
    # 테스트
    tokenizer = create_default_tokenizer()
    
    test_text = """
    마케팅 전략을 세워야 해요. 고객을 위한 제품을 개발하고 있습니다.
    이 프로젝트는 비즈니스 수익을 높이는 것이 목표입니다.
    """
    
    print("=== 토큰화 ===")
    tokens = tokenizer.tokenize(test_text)
    print(tokens)
    
    print("\n=== 키워드 추출 ===")
    keywords = tokenizer.extract_keywords(test_text, top_n=5)
    for word, score in keywords:
        print(f"  {word}: {score}")
    
    print("\n=== 쿼리 확장 ===")
    expanded = tokenizer.expand_query("마케팅 전략")
    print(expanded)
    
    print("\n=== 검색 패턴 ===")
    pattern = tokenizer.create_search_pattern("마케팅 전략")
    print(json.dumps(pattern, ensure_ascii=False, indent=2))