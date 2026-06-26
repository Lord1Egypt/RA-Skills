# 채점 기준표 — 상세 예시

각 차원별 채점에 대한 구체적인 예시입니다.

---

## A. 구조 (Structure) 예시

### name 유효성 검사
| name | 점수 | 사유 |
|------|------|------|
| `summarize` | ✅10 | 소문자, 하이픈 |
| `unit-converter` | ✅10 | 소문자, 하이픈 |
| `Skill_Creator` | ❌0 | 대문자 포함, 언더스코어 |
| `my-skill-is-really-long-and-descriptive-of-what-it-does` | ❌0 | 64자 초과 |
| `123skill` | ❌0 | 숫자로 시작 |

### description 품질
| description | 점수 | 사유 |
|------------|------|------|
| "요약, 상세요약, 5배요약, 요약해, 정리, summary, summarize, digest..." (200단어, what+when+keywords) | ✅15+10 | 명확함 + 키워드 포함 |
| "도움이 되는 스킬입니다." | ❌0 | 너무 모호함 |
| "내용을 요약합니다." | ❌5 | what은 있으나 when/keywords 없음 |

### 보조 파일 (auxiliary files)
| 파일 구성 | 점수 |
|-----------|------|
| SKILL.md + references/ | ✅10 |
| SKILL.md + README.md | ❌0 |
| SKILL.md + CHANGELOG.md + INSTALL.md | ❌0 |

---

## B. 트리거링 (Triggering) 예시

### "When" 배치 위치
| 위치 | 점수 | 사유 |
|------|------|------|
| description에 "Use when..." 포함 | ✅25 | 본문보다 먼저 로드됨 |
| SKILL.md 본문에 "When to Use" 섹션이 있음 | ❌0 | 본문은 트리거링 이후에 로드됨 |
| 둘 다 있음 | ⚠️15 | 본문의 존재는 트리거링에 의미 없음 |

### 키워드
| description | ko | en | 점수 |
|------------|----|----|------|
| "요약, 짧게 요약, 200자, summarize, digest" | ✅ | ✅ | ✅30 |
| "Summarize content into structured markdown" | ❌ | ✅ | ⚠️15 |

---

## C. 스타일 가이드 (Style Guide) 예시

### 좋은 예시 (요약 스킬)
```markdown
### Preservation Criteria (never discard)
- Core arguments and evidence — convey the author's intent
- Specific examples — concretize abstract claims
- Figures and data — with sources

### Compression Criteria
- Repeated arguments — if the same content appears in multiple places, keep only one
```
→ ✅ preservation(30) + compression(25) + essence(20) = 75+

### 나쁜 예시 (형식만 지정)
```markdown
## Output Format
- Each chapter 3-5 sentences
- Include key takeaways
```
→ ❌ preservation 기준 없음, compression 기준 없음 = 0

### N/A 적용 예외
스킬이 sub-agent를 전혀 사용하지 않고 단일 작업인 경우:
- 전체 Style Guide 점수의 50% 적용 (최대 50 → N/A 조정으로 70% 점수)
- 사유: 단일 작업 에이전트는 이미 자체 판단 기준을 내장하고 있음

---

## D. 워크플로우 (Workflow) 예시

### 좋은 예시 (명시적 Phase 0)
```markdown
### Phase 0: Structure Analysis (★ most important)
1. Scan entire text to understand outline/section structure
2. Map topic flow
3. Include this information in sub-agent prompts

### Phase 1: ...
```
→ ✅ Phase 0(30) + 번호 매기기(15) + 컨텍스트 계획(25) = 70+

### 나쁜 예시 (Phase 0 없음)
```markdown
## How to Use
1. Extract text from PDF
2. Split into chunks
3. Send to sub-agent
```
→ ❌ Phase 0 없음 = 컨텍스트 계획 0점, 전반적으로 낮은 점수

---

## E. Sub-Agent 설계 예시

### 좋은 템플릿 (`[ ]` 사용)
```markdown
## Context
[Full structure — filled by Phase 0]
[This chunk's position — filled by Phase 0]

## Preserve (this chunk only)
[Preservation list — filled by Phase 0]
```
→ ✅ template(20) + placeholders(20) + context(20) = 60+

### 나쁜 템플릿 (컨텍스트 주입 없음)
```markdown
Summarize the following text in 3-5 sentences.

---
[chunk text]
---
```
→ ❌ placeholders 없음, 컨텍스트 없음 = 낮은 점수

---

## F. 간결성 (Conciseness) 예시

| SKILL.md 줄 수 | 점수 | 참고 |
|---------------|------|------|
| 120줄 | ✅50 | 300줄 미만, 보너스 +10 = 50 |
| 280줄 | ✅40 | 500줄 미만 |
| 520줄 | ⚠️20 | 약간 초과, 분할 권장 |
| 800줄 | ❌0 | 훨씬 초과, 분할 필수 |

### "에이전트는 똑똑하다" 위반
```markdown
## How to Read a File
Use the `read` tool to read the contents of a file. The `read` tool takes a
`path` parameter which specifies the file to read...
```
→ ❌ 에이전트가 이미 아는 도구 사용법을 중복 설명함 → -15

---

## 점수 해석 가이드

### A (90+): 프로덕션 준비 완료
모든 차원에서 높은 품질을 갖춘 잘 설계된 스킬입니다. 사소한 개선만으로 배포 준비가 완료되었습니다.

### B (75–89): 양호
대부분의 기준을 충족하지만 1~2개 차원에서 개선 여지가 있습니다.

### C (60–74): 보통
기본적으로 기능하지만, sub-agent를 사용할 경우 품질이 저하될 수 있습니다.
Style Guide 또는 Phase 0이 누락되었을 가능성이 높습니다.

### D (45–59): 개선 필요
여러 차원에서 부족합니다. sub-agent 결과가 일관되지 않을 가능성이 높습니다.
구조적 개선이 필요합니다.

### F (<45): 미흡
기본 사양 준수에 문제가 있을 수 있습니다. frontmatter 또는 description을 다시 작성해야 합니다.
