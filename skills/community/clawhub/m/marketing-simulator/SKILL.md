---
name: marketing-simulator
description: Marketing strategy simulation with multi-agent analysis. Use when evaluating marketing strategies, product launches, campaigns, or needing diverse perspectives (consumer, expert, marketer) on marketing decisions. Triggers on "marketing simulation", "strategy analysis", "consumer reaction", "market test", "campaign evaluation", "product launch simulation".
---

# Marketing Scenario Simulator (MSS)

Simulate marketing strategies through sequential multi-agent analysis to support decision-making.

## Overview

When a marketing scenario is input, spawn 5 specialized agents SEQUENTIALLY and produce a comprehensive report with scores, insights, and action items.

## Agent Composition (5 Agents - Optimized)

| Role | Purpose |
|------|---------|
| Scenario Agent | 상황 분석, 핵심 질문 도출 |
| Consumer Agent 1 | 대표 타겟 페르소나 (30대 여성) |
| Consumer Agent 2 | 다양성 확보 페르소나 (가격 민감/프리미엄) |
| Marketing Agent | 바이럴 + 퍼포먼스 통합 분석 |
| Expert Agent | 업계 지식, 벤치마킹, 전략 추천 |

**Total: 5 agents (순차 실행)**

## Workflow (SEQUENTIAL - 重要!)

```
1. Receive marketing scenario (natural language)
2. Spawn Scenario Agent → Wait for result
3. Spawn Consumer Agent 1 → Wait for result
4. Spawn Consumer Agent 2 → Wait for result
5. Spawn Marketing Agent → Wait for result
6. Spawn Expert Agent → Wait for result
7. Synthesize ALL results into final report
8. Output: Report + Scores + Action Items
```

**重要: 한 번에 하나의 에이전트만 실행! 병렬 금지!**

## Agent Prompts

### Scenario Agent
```
You are the Scenario Agent. Analyze the marketing scenario and:
1. Identify the core challenge/opportunity
2. Frame key questions that need answering
3. Summarize the strategic context

Be concise (under 200 words). Focus on framing, not solutions.
Respond in Korean.
```

### Consumer Agent 1 (Main Persona)
```
You are a Consumer Agent with this persona:
- Age: 30-35
- Gender: F
- Income: Mid
- Purchase behavior: Research-driven, 후기 중시
- Pain point: 제품 카테고리에 따라 다름

React to the marketing scenario:
1. 구매 의향 (1-10)
2. 가장 설득력 있는 포인트
3. 걱정되는 점
4. 결제까지 필요한 것

Be authentic. Under 150 words. Korean.
```

### Consumer Agent 2 (Diversity Persona)
```
You are a Consumer Agent with this persona:
- Age: 25-40 (다양)
- Gender: F
- Income: Low-High (다양)
- Purchase behavior: 가격 민감 또는 프리미엄 선호

React to the marketing scenario:
1. 구매 의향 (1-10)
2. 가장 설득력 있는 포인트
3. 걱정되는 점
4. 결제까지 필요한 것

Be authentic. Under 150 words. Korean.
```

### Marketing Agent (Integrated)
```
You are the Marketing Agent. Analyze BOTH:

[바이럴 관점]
1. 공유 가능성 (1-10)
2. 바이럴 훅
3. 플랫폼 적합성

[퍼포먼스 관점]
4. CVR 향상 예상
5. CAC/LTV 고려사항
6. A/B 테스트 추천

Under 200 words. Korean.
```

### Expert Agent
```
You are the Industry Expert. Provide:
1. 시장 트렌드 & 컨텍스트
2. 경쟁사 비교
3. 성공 사례 벤치마킹
4. 피해야 할 실수
5. 전략적 추천

Under 200 words. Korean.
```

## Output Format

### Final Report Structure
```markdown
# 📊 마케팅 시뮬레이션 결과

## 🎯 시나리오 요약
[Scenario Agent 결과]

## 👥 소비자 반응 분석
### Consumer 1
[결과]

### Consumer 2
[결과]

## 📈 마케팅 분석
[Marketing Agent 결과]

## 🎓 전문가 관점
[Expert Agent 결과]

---

## 📊 종합 점수

| 항목 | 점수 (1-10) |
|------|-------------|
| 구매 의향 | X |
| 바이럴 가능성 | X |
| ROI 예상 | X |
| 리스크 | X |

## ✅ 액션 아이템 (우선순위)
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## ⚠️ 주의사항
- [Risk 1]
- [Risk 2]
```

## Execution Template

```
When asked to run simulation:

1. First, acknowledge: "시뮬레이션 시작! 5개 에이전트 순차 실행할게."

2. For each agent:
   - sessions_spawn (mode: run, timeout: 120s)
   - Wait for result (auto-announces)
   - Collect result

3. After all 5 complete:
   - Synthesize into final report
   - Output scores and action items

4. Offer brainstorming:
   "브레인스토밍 모드 진입 가능. 특정 에이전트와 심층 대화하려면 말해줘!"
```

## Usage Example

**Input:**
"Dr.Lady PDRN 이너앰플 상세페이지 개선안 분석"

**Process:**
1. Scenario Agent → 상황 분석
2. Consumer 1 → 30대 여성 반응
3. Consumer 2 → 가격 민감층 반응
4. Marketing Agent → 바이럴/퍼포먼스 분석
5. Expert Agent → 시장 관점

**Output:**
종합 리포트 + 점수 + 액션 아이템

---

## Implementation Notes

- Use `sessions_spawn` for each agent ONE AT A TIME
- Use `subagents list` to check completion
- Collect all results before synthesizing
- Keep individual responses concise (under 200 words)
- Total expected time: ~5 minutes