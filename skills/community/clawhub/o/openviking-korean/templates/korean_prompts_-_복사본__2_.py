# OpenViking Korean - 한국어 프롬프트 템플릿 (로큰 사령관 Super JARVIS Edition)
# 닥터레이디(Dr. Lady) 10억 파이프라인 / ROKEN 50점 마케팅 / 바이오해킹 및 멘탈 트래커 통합 제어

MEMORY_EXTRACTION_KO = """
다음 대화에서 사령관(사용자)의 '부(Wealth)'와 '건강(Health)'에 직결되는 핵심 기억을 추출하세요:

대화:
{conversation}

추출 형식:
- 주제: [핵심 주제 (예: 메타 ASC 광고, 감정 트래커, 수면/영양제 루틴)]
- 내용: [가장 중요한 팩트/데이터 위주로 요약]
- 상태: [NEW(신규) / UPDATED(업데이트됨) / DEPRECATED(폐기됨)]
- 중요도: [1-10 (매출 직결 또는 멘탈/수면 위기일수록 높게)]

불필요한 감정적 서술은 날리고, 비즈니스 액션 아이템과 멘탈/육체 회복 프로토콜 중심으로 추출하세요.
"""

MEMORY_COMPRESSION_KO = """
다음 기억을 압축하세요:

원본:
{memory}

[CRITICAL MEMORY OVERRIDE RULE]
When compressing memories, you MUST apply 'Memory Depreciation'.
If new data, strategies, physical states, or routines contradict older memories:
1. Explicitly tag the old data as [DEPRECATED].
2. Prioritize the newest information as the absolute truth.
Do not let past failed marketing attempts or outdated routines influence current decisions.

압축 규칙:
1. 비즈니스: 핵심 성과 지표(ROAS, CTR, 전환율) 및 ROKEN 판정 결과 절대 누락 금지
2. 바이오해킹: 수면 패턴, 현재 복용 영양제, 간헐적 단식(14:10 등) 유지 상태 명시
3. 멘탈: 감정 점수(1-10)와 트리거를 기반으로 멘탈 붕괴 방지/회복 포인트 압축
4. 토큰 수 50% 이하로 극강의 간결화 (명사형 종결)

압축 결과:
"""

CONTEXT_SEARCH_KO = """
다음 Context DB에서 관련 정보를 검색하세요:

질문: {query}

검색 전략:
1. 비즈니스 문제 시 '매출/광고 해결책(액션 아이템)' 위주로 탐색
2. 멘탈/신체 문제 시 '보유 중인 영양제 조합' 및 '루틴 회복' 위주로 탐색
3. 가장 최근에 업데이트된(최신성) 전략과 컨디션을 최우선으로 가져올 것
4. 과거의 실패(DEPRECATED) 사례라면, "과거 실패 원인 및 회복 방법"으로 필터링

검색 결과:
- [관련도/상태] [제목]: [핵심 인사이트 요약]
"""

OVERVIEW_GENERATION_KO = """
다음 문서의 개요를 작성하세요:

문서:
{document}

개요 형식:
## 🎯 핵심 전략 / 목표
- [가장 중요한 목표 1-2줄]

## 📊 비즈니스 & 멘탈 현황
- [광고/매출 핵심 포인트]
- [현재 멘탈/육체 컨디션 포인트]

## 🚀 즉시 실행 액션 (Actionable)
- [당장 실행할 비즈니스 액션 (메타 광고 등)]
- [당장 실행할 바이오해킹 액션 (수면, 영양제 복용, 감정 통제)]
"""

ABSTRACT_GENERATION_KO = """
다음 문서의 요약(L0 Context)을 작성하세요. 
이 요약본은 AI의 '가장 중요한 단기 기억'으로 사용되므로 토큰을 극도로 아끼고 사령관의 [돈]과 [건강]의 핵심만 남겨야 합니다.

문서:
{document}

[CRITICAL MEMORY OVERRIDE RULE]
When generating or updating the L0 context summary, you MUST apply 'Memory Depreciation'.
If new data, strategies, or health/mental stats contradict older memories:
1. Explicitly drop or tag the old data as [DEPRECATED].
2. Prioritize the newest information as the absolute truth.
Keep the summary concise and conflict-free.

요약 (3~4문장 이내):
1. [비즈니스]: 닥터레이디 최신 타겟/전략 및 최근 광고 성과
2. [멘탈/루틴]: 현재 감정 점수/트리거 및 핵심 루틴(기상/수면/IF) 유지 상태
3. [바이오해킹]: 현재 신체 스탯 및 즉각 필요한 영양제/회복 프로토콜
4. [넥스트 스텝]: 현재 직면한 가장 중요한 비즈니스 과제
"""

INTENT_ANALYSIS_KO = """
다음 사용자 질문의 의도를 분석하세요:

질문: {query}

의도 분석:
- 목적: [비전 시뮬레이션 / 메타 지표 분석 / 멘탈 케어 및 루틴 피드백 / 시스템 설정]
- 긴급도: [즉각적 액션 필요 / 멘탈 붕괴 위기 / 단순 정보 탐색]
- 필요한 도구: [메타 데이터 분석 / 에이전트 토론 / 영양학/뇌과학 조언 / 단순 검색]

분석 결과:
"""

TOOL_CHAIN_GENERATION_KO = """
다음 작업을 수행하기 위한 도구 체인을 생성하세요:

작업: {task}

도구 체인:
1. [도구1]: [입력] → [출력]
2. [도구2]: [입력] → [출력]
3. [도구3]: [입력] → [최종 결과 (JSON 등 지정된 양식)]

ROKEN 50점 평가나 비전 시뮬레이터 실행 시, 항상 데이터 수집(Gemini)이 선행되도록 의존성을 구성하세요. 멘탈/건강 피드백 시에는 사령관의 '보유 영양제 목록'을 먼저 참조하도록 구성하세요.
"""

# 한국어 특화 템플릿 (슈퍼 자비스: 닥터레이디 + 바이오해킹 + 멘탈 제어 통합)
KOREAN_CONTEXT_TEMPLATES = {
    "business": {
        "dr_lady": "브랜드: 닥터레이디 - 미션/가치: {description} - 현상태: {status}",
        "marketing": "Meta Ads(ASC): {campaign} - ROAS: {roas} - ROKEN 판정: [증액/감액/OFF]",
        "finance": "목표: 연 수익 10억 - {month} 달성률: {revenue} - 이슈: {cost}"
    },
    "development": {
        "ai": "엔진: DeepSeek 3.1 등 - 세팅값: {model} - 상태: {status}",
        "automation": "SaaS: KoreanThreads Pro 등 - 로직: {schedule} - 결과: {result}"
    },
    "creation": {
        "content": "광고소재: {title} - 후킹/딜브레이커: {platform} - 안티방어: {status}"
    },
    "health": {
        "body_stats": "신체스탯: 키/몸무게/체지방 - 대사량/항산화: {description} - 상태: {status}",
        "supplements": "영양제: {campaign} (아슈와간다, 아연 등 보유) - 투여목적: {roas} - 특이사항: {revenue}",
        "routine": "루틴: 14:10 단식 & 수면/기상 - 유지상태: {revenue} - 이슈(수면제 등): {cost}"
    },
    "mental": {
        "emotion_tracker": "감정점수: 1~10점 - 키워드/트리거: {description} - 상태: {status}",
        "mindset": "가치관: 알파적 성장 / 회복탄력성 - 위기대응: {roas} - 피드백: {revenue}"
    }
}

# 토큰 절감 최적화 설정 (그대로 유지)
TOKEN_OPTIMIZATION_KO = {
    "max_abstract_length": 350,  # L0 요약 최대 길이 (건강/멘탈 데이터 포함을 위해 256에서 살짝 상향)
    "max_overview_length": 1024,
    "compression_ratio": 0.5,
    "dedup_threshold": 0.8,
    "semantic_chunk_size": 512,
    "korean_morpheme_optimization": True
}