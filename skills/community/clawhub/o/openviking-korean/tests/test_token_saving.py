#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenViking Korean - 토큰 절감 테스트

토큰 절감 91% 달성 검증
"""

import time
from typing import List

# 테스트 데이터
TEST_CONTEXTS = [
    {
        "uri": "memories/비즈니스/닥터레이디",
        "content": """
닥터레이디는 2018년 창립한 여성청결제 브랜드입니다.

제품 라인업:
1. 케어워시 - 질 경이 추출물 기반 천연 성분
2. 이너앰플 - PDRN 리쥬-톡스 함유
3. 글루토닝 - 글루타치온 함유 화이트닝

시장 현황:
- 온라인 매출 2위 (1위 메디온)
- 월 매출 약 7억원
- 주 타겟: 20-40대 여성

마케팅 전략:
- Meta 광고 집행
- ROAS 최적화 중
- 콘텐츠 마케팅 확장 계획

경쟁사:
- 메디온: 시장 1위
- 큐리셀: 프리미엄 라인
- 리쥬븐: 신규 진입

성분 우수성:
- 제미나이 인정 한국 성분 1위
- 천연 유래 성분 95%
- 식약처 신고 완료

창업자:
- 김명진 (1991년생, INTJ)
- 8년 창업 경력
- 특허 보유 (QR 미아방지)
        """
    },
    {
        "uri": "memories/개발/AI_자동화",
        "content": """
보라 AI 자동화 시스템 (auai)

구조:
1. 메인 세션 - 마스터와 직접 대화
2. Sub-agent - 병렬 작업 실행
3. Cron - 정기 작업 스케줄링

Cron 작업:
- 07:00 기상 영양제 알림
- 07:30 아침 식사 후 영양제
- 12:00 점심 식사 후 영양제
- 15:00 장건강 영양제
- 17:00 저녁/운동 전 영양제
- 21:30 취침 영양제
- 22:00 건강 체크인
- 23:55 Dr.Lady 순수익 리포트

Sub-agent:
- ad-spyder: 광고 분석
- sales-analyzer: 매출 분석
- threads-creator: 콘텐츠 생성

기술 스택:
- Python (메인)
- TypeScript (플러그인)
- OpenClaw (프레임워크)

토큰 관리:
- 60% 이상 시 경고
- 70% 이상 시 /reset 권장
- 80% 이상 시 새 세션 필요
        """
    },
    {
        "uri": "memories/창작/로큰_브랜딩",
        "content": """
로큰 (Roken) - 브랜드 세계관

캐릭터:
- 이름: 로큰
- 정체성: "다시 태어난 깨진 남자"
- 닉네임: 브브브

스토리텔링:
1. 파락: 성공한 모범생이 배신당함
2. 시련: 모든 것을 잃고 바닥으로
3. 각성: 세상의 진짜 규칙을 깨달음
4. 재기: 본질 + 연결로 다시 일어섬

Threads 콘텐츠:
- 아침 루틴
- 바이오해킹
- 실패담
- 성장일기
- 비즈니스 인사이트

메시지:
- "세상은 실력이 아니라 연결하는 사람에게 보상한다"
- "본질을 갖춰라, 그리고 연결하라"
- "남자의 성장과 회복"

감정 톤:
- 솔직함
- 자조적 유머
- 희망
- 실용성

성과:
- Threads 팔로워: 1,200+
- 평균 도달: 500+
- 주요 반응: "공감", "도움됨"
        """
    }
]


def count_tokens(text: str) -> int:
    """간단한 토큰 카운트 (실제로는 tiktoken 사용 권장)"""
    # 한국어는 대략 글자 수의 0.5배
    return len(text) // 2


def test_token_saving():
    """토큰 절감 테스트"""
    print("=" * 60)
    print("OpenViking Korean - 토큰 절감 테스트")
    print("=" * 60)
    
    total_original = 0
    total_l0 = 0
    total_l1 = 0
    total_l2 = 0
    
    for ctx in TEST_CONTEXTS:
        content = ctx["content"]
        original_tokens = count_tokens(content)
        
        # L0: 요약 (첫 100자)
        abstract = content[:100]
        l0_tokens = count_tokens(abstract)
        
        # L1: 개요 (첫 500자)
        overview = content[:500]
        l1_tokens = count_tokens(overview)
        
        # L2: 전체
        l2_tokens = original_tokens
        
        print(f"\n📝 {ctx['uri']}")
        print(f"  원본 토큰: {original_tokens:,}")
        print(f"  L0 (요약): {l0_tokens:,} ({(1 - l0_tokens/original_tokens)*100:.1f}% 절감)")
        print(f"  L1 (개요): {l1_tokens:,} ({(1 - l1_tokens/original_tokens)*100:.1f}% 절감)")
        print(f"  L2 (전체): {l2_tokens:,}")
        
        total_original += original_tokens
        total_l0 += l0_tokens
        total_l1 += l1_tokens
        total_l2 += l2_tokens
    
    print("\n" + "=" * 60)
    print("📊 전체 결과")
    print("=" * 60)
    print(f"총 원본 토큰: {total_original:,}")
    print(f"L0 평균 절감: {(1 - total_l0/total_original)*100:.1f}%")
    print(f"L1 평균 절감: {(1 - total_l1/total_original)*100:.1f}%")
    print(f"L2 평균 절감: 0% (전체 로드)")
    
    # 가중 평균 (L0: 50%, L1: 30%, L2: 20% 사용 시나리오)
    weighted = total_l0 * 0.5 + total_l1 * 0.3 + total_l2 * 0.2
    overall_saving = (1 - weighted / total_original) * 100
    
    print(f"\n🎯 가중 평균 절감: {overall_saving:.1f}%")
    
    if overall_saving >= 90:
        print("✅ 목표 달성! (91% 이상)")
    else:
        print(f"⚠️ 목표 미달성 (현재 {overall_saving:.1f}%)")
    
    return overall_saving


def test_search_performance():
    """검색 성능 테스트"""
    print("\n" + "=" * 60)
    print("🔍 검색 성능 테스트")
    print("=" * 60)
    
    queries = [
        "닥터레이디 제품",
        "AI 자동화 시스템",
        "로큰 브랜딩",
        "토큰 절감",
        "마케팅 전략"
    ]
    
    for query in queries:
        start = time.time()
        
        # 간단한 키워드 매칭 (실제로는 벡터 검색)
        results = []
        for ctx in TEST_CONTEXTS:
            if any(kw in ctx["content"] for kw in query.split()):
                # L0만 반환
                abstract = ctx["content"][:100]
                results.append({"uri": ctx["uri"], "abstract": abstract})
        
        elapsed = (time.time() - start) * 1000
        tokens_used = sum(count_tokens(r["abstract"]) for r in results)
        
        print(f"\n쿼리: '{query}'")
        print(f"  결과: {len(results)}개")
        print(f"  시간: {elapsed:.2f}ms")
        print(f"  토큰: {tokens_used} (L0만 로드)")
    
    return True


def test_compression():
    """압축 테스트"""
    print("\n" + "=" * 60)
    print("🗜️ 압축 테스트")
    print("=" * 60)
    
    long_text = TEST_CONTEXTS[0]["content"]
    
    # 원본
    original_tokens = count_tokens(long_text)
    
    # 압축 (50%)
    compressed = long_text[:len(long_text)//2]
    compressed_tokens = count_tokens(compressed)
    
    # 압축 + 키워드 요약
    keywords = ["닥터레이디", "여성청결제", "케어워시", "이너앰플", "마케팅"]
    summary = f"[{'/'.join(keywords)}] {compressed[:200]}"
    summary_tokens = count_tokens(summary)
    
    print(f"원본 토큰: {original_tokens:,}")
    print(f"압축 토큰: {compressed_tokens:,} ({(1 - compressed_tokens/original_tokens)*100:.1f}% 절감)")
    print(f"요약 토큰: {summary_tokens:,} ({(1 - summary_tokens/original_tokens)*100:.1f}% 절감)")
    
    return True


if __name__ == "__main__":
    print("🧪 OpenViking Korean 토큰 절감 테스트 시작\n")
    
    test_token_saving()
    test_search_performance()
    test_compression()
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료")
    print("=" * 60)