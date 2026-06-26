---
name: glm-swarm
description: "경량 모델 병렬 하네스. 명시적으로 swarm/병렬 처리를 요청하거나, AGENTS.md 하네스 규칙에 의해 복합 작업(도구 3회+, 독립 하위작업 2개+)이 감지되었을 때만 사용. 단순 질답, 번역, 요약, 단일 도구 호출에는 절대 사용하지 않는다."
---

# GLM Swarm

경량 모델 복합 작업 병렬 하네스. 상세 패턴은 `references/patterns.md`, Context Packet 규칙은 `references/context-packet.md` 참조.

## 복잡도 게이트 (필수)

swarm 진입 전 반드시 판단:
- 독립 하위 작업 2개 미만 → **직접 처리** (swarm 안 씀)
- 도구 호출 3회 미만 → **직접 처리**
- 위 둘 다 해당 → **swarm 모드**

## 실행 흐름

```
0. bash scripts/planner.sh {task-id} → /tmp/swarm/{task-id}/ 초기화
1. Planner (1회) — 패턴 매칭(A~E) → atomic task 분해
2. Context Packet — worker별 최소 맥락 압축 (출력 300토큰 이내 명시)
3. Worker Pool — sessions_spawn 병렬 (최대 6개, lightContext: true)
4. Shared Scratchpad — /tmp/swarm/{id}/shared.md
5. Aggregator — 구조화 합산 (섹션별 분류 + 핵심 인사이트 3개 + 액션 아이템)
6. bash scripts/cleanup.sh {task-id} → /tmp/swarm/{id}/ 삭제
```

## 패턴 요약

| 패턴 | 트리거 | 구조 |
|------|--------|------|
| A | 조사→판단→실행 | t1∥t2 → t3 → t4 |
| B | 다중 수집→합성 | t1∥t2∥t3∥t4 → t5 |
| C | 반복 N건 병렬 | t1∥...∥tN → concat |
| D | 분석→제안 | t1∥t2 → t3 → t4 |
| E | 검증→수정→배포 | 순차 (파일 충돌 방지) |

매칭 안 되면 동적 분해. 상세: `references/patterns.md`

## Worker 스폰

```
sessions_spawn({
  task: "{context_packet}\n출력은 300토큰 이내로 작성해.",
  mode: "run", runtime: "subagent",
  lightContext: true,
  label: "swarm-{task-id}-{worker-id}"
})
```

Planner 초기화: `bash scripts/planner.sh {task-id}`
정리: `bash scripts/cleanup.sh {task-id}|--all|--list`

## 안전

- Worker: MEMORY/SOUL/AGENTS.md 편집 금지, ~/.secrets/ 접근 금지
- 외부 행동 → Aggregator 후 승인 요청
- 2회 실패 → 해당 task 스킵. 50%+ 실패 → swarm 중단

## Aggregator 규칙

결과 합산 시 반드시 포함:
1. **섹션별 분류** — 결과를 주제별로 정리
2. **핵심 인사이트 3개** — 가장 중요한 발견
3. **액션 아이템** — 즉시 실행 가능한 다음 스텝
4. **출처 표기** — 각 판단에 어떤 worker 결과 기반인지 명시

## 컨텍스트 최적화 (v1.1)

**문제**: worker 결과 전문이 메인 세션에 주입되면 컨텍스트 누적
**해결**: Aggregator는 메인에 **요약만** 반환

```
Aggregator 출력:
1. 메인 세션: 요약 3~5줄 (핵심 발견 + 액션 아이템만)
2. 상세 결과: memory/swarm-results/{task-id}.md 에 저장
3. 메인은 상세가 필요하면 해당 파일을 읽어옴
```

Aggregator 스킵 조건에 추가:
- worker 결과 총합이 500토큰 이하면 → 전문 반환 (요약 불필요)
- 500토큰 초과면 → 요약 반환 + 파일 저장
