# Context Packet 프로토콜

## 목적

서브에이전트(worker)에게 전달하는 맥락을 최소화+명시화하여:
1. 토큰 비용 절감
2. worker의 작업 정확도 향상
3. 불필요한 맥락으로 인한 혼란 방지

## Context Packet 구조

```
=== CONTEXT PACKET ===
[GOAL] 전체 작업의 목적 (1줄)
[YOUR_ROLE] 이 worker가 할 일 (1줄)
[CONTEXT] 이 task 수행에 필요한 정보
  - 팩트 1
  - 팩트 2
  - (필요한 만큼, 최소한으로)
[OUTPUT_FORMAT] 정확한 출력 형태
[CONSTRAINTS] 하지 말아야 할 것
[SCRATCHPAD] /tmp/swarm/{task-id}/shared.md (읽기/쓰기 경로)
[WRITE_TO] /tmp/swarm/{task-id}/{worker-id}.md (결과 저장 경로)
=== END PACKET ===
```

## 작성 원칙

### 1. 최소 전달 (Minimum Context)

❌ 나쁜 예:
```
[CONTEXT] MEMORY.md 전체, TOOLS.md 전체, 최근 대화 30턴
```

✅ 좋은 예:
```
[CONTEXT]
- 고객사 A Discord 채널 ID: 1234567890
- 확인할 것: 최근 24시간 대화 유무
- 활성도 기준: 24h 내 대화 있으면 ✅, 없으면 ⚠️, 7일 없으면 🔴
```

### 2. Self-contained (자기 완결)

worker가 Context Packet만 보고 바로 실행 가능해야 함.
추가 파일 읽기나 질문 없이.

필요한 ID, 경로, 기준값은 모두 packet에 포함.

### 3. 출력 포맷 고정

worker가 "적당히 정리"하면 Aggregator가 합치기 어려움.

❌: "결과를 정리해줘"
✅: "JSON 형태로 출력: {channel: string, status: '✅'|'⚠️'|'🔴', last_message: string, hours_ago: number}"

### 4. 제약 명시

worker가 하면 안 되는 것:
- 시스템 파일(MEMORY.md, SOUL.md) 수정
- `~/.secrets/` 접근
- 외부 행동 (이메일, SNS, 메시지 전송)
- 다른 worker의 출력 파일 덮어쓰기

## Context Packet 크기 가이드

| worker 작업 복잡도 | packet 권장 크기 |
|-------------------|----------------|
| 단순 조회 | 100~200 토큰 |
| 분석/비교 | 200~500 토큰 |
| 실행/생성 | 300~600 토큰 |

600 토큰 넘으면 task를 더 쪼개야 하는 신호.

## Shared Scratchpad 프로토콜

경로: `/tmp/swarm/{task-id}/shared.md`

### 쓰기 규칙
```markdown
## t1 결과
(t1 worker가 여기에 씀)

## t2 결과
(t2 worker가 여기에 씀)
```

- 각 worker는 자기 섹션(`## {worker-id} 결과`)에만 쓰기
- 다른 worker 섹션은 읽기만

### 읽기 규칙
- 의존성 있는 worker만 선행 worker 섹션을 읽음
- 의존성 없는 worker는 Scratchpad 안 읽어도 됨
