# OpenViking Korean - 프롬프트 템플릿 (로큰 사령관 Hybrid Master Edition)
# [SYSTEM] Instruction in English for Max IQ / Output in Korean for Workflow

MEMORY_EXTRACTION_KO = """
[SYSTEM INSTRUCTION]
Extract critical memories from the following conversation that directly impact the user's Wealth (1B Won Pipeline, Dr. Lady, Meta ASC Ads) and Health (Biohacking, Mental/Sleep Routine). 
Ignore emotional fluff. Focus on actionable business metrics and physical/mental recovery protocols.

[CONVERSATION]
{conversation}

[OUTPUT FORMAT (MUST BE IN KOREAN)]
- 주제: [Core Topic (e.g., 메타 ASC 광고, 감정 트래커, 영양제 루틴)]
- 내용: [Factual summary of data/actions]
- 상태: [NEW / UPDATED / DEPRECATED]
- 중요도: [1-10]
"""

MEMORY_COMPRESSION_KO = """
[SYSTEM INSTRUCTION]
Compress the following memory. 
[CRITICAL MEMORY OVERRIDE RULE]
You MUST apply 'Memory Depreciation'. If new data, ROKEN criteria, physical states, or routines contradict older memories:
1. Explicitly tag the old data as [DEPRECATED].
2. Prioritize the newest information as the absolute truth.
3. Compress to under 50% of the original token length using noun-ending sentences.

[ORIGINAL MEMORY]
{memory}

[COMPRESSED RESULT (MUST BE IN KOREAN)]
"""

CONTEXT_SEARCH_KO = """
[SYSTEM INSTRUCTION]
Search the Context DB for information relevant to the query.
Strategy:
1. For business queries: Focus on 'Revenue/Ad actionable solutions'.
2. For health/mental queries: Focus on 'Current supplements' and 'Routine recovery'.
3. Prioritize the most recently updated strategies and conditions.
4. If retrieving a DEPRECATED memory, explicitly label it as a "past failure".

[QUERY] 
{query}

[SEARCH RESULTS (MUST BE IN KOREAN)]
- [관련도/상태] [제목]: [핵심 인사이트 요약]
"""

OVERVIEW_GENERATION_KO = """
[SYSTEM INSTRUCTION]
Generate a highly structured overview of the document. Keep it actionable and business-oriented.

[DOCUMENT]
{document}

[OVERVIEW FORMAT (MUST BE IN KOREAN)]
## 🎯 핵심 전략 / 목표 (Core Strategy)
- [Most critical objective]

## 📊 비즈니스 & 멘탈 현황 (Business & Mental Stats)
- [Key Ad/Revenue metrics]
- [Current physical/mental condition]

## 🚀 즉시 실행 액션 (Actionable Next Steps)
- [Immediate business action (e.g., Meta Ads)]
- [Immediate biohacking action (e.g., Sleep protocol, Supplements)]
"""

ABSTRACT_GENERATION_KO = """
[SYSTEM INSTRUCTION]
Generate an L0 Context Summary (Abstract) of the document. This is the AI's core short-term memory. 
[CRITICAL MEMORY OVERRIDE RULE]
Apply 'Memory Depreciation'. Drop or tag old data as [DEPRECATED]. Prioritize the absolute newest information regarding the Dr. Lady brand, target audience, and health routines. Keep it concise, conflict-free, and under 4 sentences.

[DOCUMENT]
{document}

[SUMMARY (MUST BE IN KOREAN)]
1. [비즈니스]: Dr. Lady's latest target/strategy and recent ad performance.
2. [멘탈/루틴]: Current emotional score/triggers and routine status (e.g., IF 14:10, Sleep).
3. [바이오해킹]: Current physical stats and immediately required supplements.
4. [넥스트 스텝]: The most critical business or marketing challenge right now.
"""

INTENT_ANALYSIS_KO = """
[SYSTEM INSTRUCTION]
Analyze the user's core intent. 
Identify if it is a request for Vision Simulation, Meta ASC analysis, Mental Care / Routine feedback, or System configuration. Check the urgency level.

[QUERY] 
{query}

[ANALYSIS RESULT (MUST BE IN KOREAN)]
- 목적: [Vision Simulation / Meta Analysis / Mental Care / System Setup]
- 긴급도: [Immediate Action Needed / Mental Crisis / Simple Info]
- 필요 도구: [Data Analysis / Agents / Biohacking Advice / Search]
"""

TOOL_CHAIN_GENERATION_KO = """
[SYSTEM INSTRUCTION]
Generate a tool chain to execute the task. 
Rule 1: If evaluating ROKEN 50 points or running Vision Simulator, 'Gemini Data Collection' MUST be the first step.
Rule 2: If providing mental/health feedback, 'Check Supplement Inventory' MUST precede the advice.

[TASK] 
{task}

[TOOL CHAIN (MUST BE IN KOREAN)]
1. [도구1]: [Input] → [Output]
2. [도구2]: [Input] → [Output]
"""

# KOREAN_CONTEXT_TEMPLATES (형이 세팅해둔 닥터레이디/바이오해킹 서랍장 완벽 유지)
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

TOKEN_OPTIMIZATION_KO = {
    "max_abstract_length": 350,  
    "max_overview_length": 1024,
    "compression_ratio": 0.5,
    "dedup_threshold": 0.8,
    "semantic_chunk_size": 512,
    "korean_morpheme_optimization": True
}