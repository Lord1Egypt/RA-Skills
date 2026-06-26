# OpenViking Korean - 한국어 프롬프트 템플릿
# 토큰 절감을 위한 한국어 최적화 프롬프트

MEMORY_EXTRACTION_KO = """
다음 대화에서 중요한 기억을 추출하세요:

대화:
{conversation}

추출 형식:
- 주제: [핵심 주제]
- 내용: [요약된 기억]
- 카테고리: [비즈니스/개발/창작/개인]
- 중요도: [1-10]

중복 제거하고 핵심만 추출하세요.
"""

MEMORY_COMPRESSION_KO = """
다음 기억을 압축하세요:

원본:
{memory}

압축 규칙:
1. 핵심 정보만 유지
2. 불필요한 서술 제거
3. 한국어 간결화
4. 토큰 수 50% 이하로 줄이기

압축 결과:
"""

CONTEXT_SEARCH_KO = """
다음 Context DB에서 관련 정보를 검색하세요:

질문: {query}

검색 전략:
1. 키워드 확장 (동의어, 연관어)
2. 카테고리 필터링
3. 시간 순 정렬
4. 관련도 점수 계산

검색 결과:
- [관련도] [제목]: [요약]
"""

OVERVIEW_GENERATION_KO = """
다음 문서의 개요를 작성하세요:

문서:
{document}

개요 형식:
## 핵심 주제
- [주요 주제 1]
- [주요 주제 2]

## 주요 내용
- [핵심 포인트 1]
- [핵심 포인트 2]
- [핵심 포인트 3]

## 추천 액션
- [다음 단계 1]
- [다음 단계 2]
"""

ABSTRACT_GENERATION_KO = """
다음 문서의 요약을 3문장으로 작성하세요:

문서:
{document}

요약:
1. [핵심 메시지]
2. [주요 내용]
3. [결론/제안]
"""

INTENT_ANALYSIS_KO = """
다음 사용자 질문의 의도를 분석하세요:

질문: {query}

의도 분석:
- 검색 의도: [정보 검색/작업 요청/대화]
- 카테고리: [비즈니스/개발/창작/개인]
- 키워드: [주요 키워드 추출]
- 예상 응답: [정보 제공/실행/대화]

분석 결과:
"""

TOOL_CHAIN_GENERATION_KO = """
다음 작업을 수행하기 위한 도구 체인을 생성하세요:

작업: {task}

도구 체인:
1. [도구1]: [입력] → [출력]
2. [도구2]: [입력] → [출력]
3. [도구3]: [입력] → [최종 결과]

실행 순서와 의존성을 고려하세요.
"""

# 한국어 특화 템플릿
KOREAN_CONTEXT_TEMPLATES = {
    "business": {
        "startup": "창업: {project_name} - {description} - 상태: {status}",
        "marketing": "마케팅: {campaign} - ROAS: {roas} - 매출: {revenue}",
        "finance": "재무: {month} - 매출: {revenue} - 비용: {cost} - 순이익: {profit}"
    },
    "development": {
        "ai": "AI: {project} - 모델: {model} - 상태: {status}",
        "automation": "자동화: {task} - 스케줄: {schedule} - 결과: {result}",
        "skill": "스킬: {skill_name} - 버전: {version} - 용도: {purpose}"
    },
    "creation": {
        "content": "콘텐츠: {title} - 플랫폼: {platform} - 상태: {status}",
        "branding": "브랜딩: {brand} - 메시지: {message} - 타겟: {target}",
        "storytelling": "스토리: {theme} - 감정: {emotion} - 전달: {message}"
    }
}

# 토큰 절감 최적화 설정
TOKEN_OPTIMIZATION_KO = {
    "max_abstract_length": 256,  # L0 요약 최대 길이
    "max_overview_length": 1024,  # L1 개요 최대 길이
    "compression_ratio": 0.5,  # 압축 비율
    "dedup_threshold": 0.8,  # 중복 제거 임계값
    "semantic_chunk_size": 512,  # 시맨틱 청크 크기
    "korean_morpheme_optimization": True  # 한국어 형태소 최적화
}