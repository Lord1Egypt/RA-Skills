---
name: managed-agent-growth-loop
description: 고객사 상주 에이전트의 실행 품질을 성장시키는 운영 루프. 사용 내역/현장 회고에서 "잘 쓰는 부분, 한계, 개선점, 무펭이즘 서비스 가치"를 뽑아 상태 인수인계, 선제 행동, 팀원 온보딩, 결과 피드백, 멀티에이전트 검수 플로우로 전환할 때 사용. "에이전트 운영 개선", "인사이트 뽑아서 스킬", "현장 회고", "컨텍스트 휘발", "피드백 루프", "팀원 온보딩", "선제적 행동" 요청에 트리거.
version: 0.1.1
platforms:
- macos
- linux
metadata:
  hermes:
    priority: P1
source: 2026-04-30 포네이처스 힐림이 사용 회고 — 실행은 강하지만 추적·피드백 루프가 약하다는 인사이트
---

# Managed Agent Growth Loop

고객사 에이전트를 "시키면 잘하는 도구"에서 "상태를 이어받고, 먼저 챙기고, 결과에서 배우는 운영 파트너"로 올리는 스킬.

## 핵심 인사이트

- 강점: 문서 생성 속도, 외부/내부 데이터 연결, 비동기 멀티태스킹은 이미 고객 가치가 크다.
- 병목: 세션이 끊기면 맥락이 휘발되고, 마감/진행 추적이 약하며, 팀원 연결과 결과 회고가 빠진다.
- 서비스 가치: 무펭이즘은 개별 작업 대행이 아니라 **운영 루프 OS**를 제공해야 한다.

## 실행 트리거

다음 상황이면 이 스킬을 적용한다.

- 고객사 에이전트 사용 내역을 회고할 때
- "잘 쓰는 부분 / 한계 / 개선점 / 우리가 줄 수 있는 것"을 정리할 때
- 작업은 많이 했는데 다음 단계, 결과, 담당자, 마감이 불명확할 때
- 새 고객사·팀원 온보딩 또는 에이전트 운영 체계를 만들 때

## 5단계 운영 루프

### 1. Usage → Value Map

최근 작업을 아래 4칸으로 분류한다.

```markdown
## 사용 가치 맵
- 빠른 실행: (문서/자료/분석 등 시간 단축 사례)
- 데이터 연결: (공고·NAS·보고서·기존 자료·CRM/ERP 연결 사례)
- 비동기 지원: (대표/팀원이 다른 일 할 때 병렬 처리한 사례)
- 미활용 영역: (아직 연결 안 된 사람/채널/업무)
```

### 2. State Handoff

진행 중 작업마다 상태 파일을 남긴다. 완벽한 문서보다 **다음 에이전트가 바로 이어받을 수 있는 최소 상태**가 중요하다.

```markdown
# 작업 상태 — {프로젝트명}
- 최종 업데이트: YYYY-MM-DD HH:mm
- 담당/요청자:
- 목표:
- 마감:
- 현재 단계:
- 완료한 것:
- 남은 것:
- 차단 요소:
- 관련 파일/링크:
- 다음 액션 1개:
```

권장 저장 위치: 고객사별 `memory/clients/{client}/active-tasks/` 또는 기존 운영 파일.

### 3. Proactive Watchlist

에이전트가 먼저 챙길 항목을 3개 이하로 유지한다. 많으면 안 한다.

```markdown
## 선제 체크리스트
- D-7/D-3/D-1 마감 알림:
- 제출 후 결과 확인일:
- 담당자 응답 대기:
```

규칙:
- 마감 있는 일은 D-7/D-3/D-1 중 최소 1번 확인.
- 48시간 이상 응답 없는 외부 의존 작업은 한 번만 리마인드 초안 제안.
- 심야/외부 발송/민감 커뮤니케이션은 사용자 승인 후 진행.

### 4. Team Onboarding Gap

에이전트가 커버하지 못하는 사람/채널을 명시한다.

```markdown
## 온보딩 갭
| 사람 | 역할 | 현재 연결 | 필요한 연결 | 다음 액션 |
|---|---|---|---|---|
```

다음 액션 예시:
- ERP 등록 필요
- Discord/Telegram 초대 필요
- 자료 접근 권한 필요
- 담당 업무/호칭/응대 톤 확인 필요

### 5. Outcome Feedback Loop

문서·제안서·신청서는 제출 후 결과가 들어와야 실력이 오른다.

```markdown
## 결과 회고
- 산출물:
- 제출처/상대:
- 결과: 통과 / 탈락 / 보류 / 미확인
- 받은 피드백:
- 다음에 유지할 것:
- 다음에 바꿀 것:
- 스킬/메모리에 반영할 규칙:
```

결과가 미확인이면 "블랙박스"로 표시하고, 확인 요청 후보에 올린다.

## Cron/Heartbeat 운영 레시피

이 스킬은 문서 포맷만으로 끝내지 말고, 반복 확인이 필요한 항목을 cron 또는 heartbeat 작업으로 승격한다.

### 승격 기준

- 마감/결과 확인일이 명확하다 → cron
- 매일 짧게 상태를 훑으면 가치가 있다 → cron
- 현장 맥락을 보고 유연하게 판단해야 한다 → heartbeat
- 외부 발송, 민감 커뮤니케이션, 고객에게 보이는 액션 → 초안까지만 만들고 사용자 승인

### 표준 cron 후보

```markdown
## Cron 후보
| 이름 | 주기 | 목적 | 세션 | 전달 | 성공 기준 | 실패/중단 기준 |
|---|---|---|---|---|---|---|
| D-day Watch | 매일 09:10 | 마감 D-7/D-3/D-1 확인 | isolated | no-deliver 또는 내부 채널 | 놓친 마감 0건 | 2주간 유효 항목 0건이면 중단 |
| Outcome Check | 매주 월 10:00 | 제출물 결과 미확인 추적 | isolated | announce | 블랙박스 항목 감소 | 리마인드 2회 무응답이면 보류 |
| Onboarding Gap Check | 매주 금 16:00 | 팀원/데이터 연결 누락 확인 | isolated | no-deliver | 갭 리스트 최신화 | 신규 갭 없으면 월 1회로 축소 |
```

### OpenClaw cron 예시

```bash
openclaw cron add \
  --name "{고객사} managed-agent D-day watch" \
  --cron "10 9 * * *" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "Use the managed-agent-growth-loop skill. Check active tasks for {고객사}; update the proactive watchlist; only notify if a deadline/blocked dependency/customer-risk needs attention." \
  --light-context \
  --no-deliver
```

```bash
openclaw cron add \
  --name "{고객사} outcome feedback loop" \
  --cron "0 10 * * 1" \
  --tz "Asia/Seoul" \
  --session isolated \
  --message "Use the managed-agent-growth-loop skill. Review submitted proposals/docs for {고객사}; mark results as pass/fail/hold/unknown; draft one approval-needed follow-up if outcome is still unknown." \
  --light-context \
  --announce \
  --channel discord \
  --to "channel:{운영채널ID}"
```

### Cron 실행 원칙

- cron은 직접 고객에게 보내는 발송기가 아니라 **감시/정리/초안 생성기**로 둔다.
- 같은 알림을 반복하지 않는다. 상태가 바뀌었거나 리스크가 커졌을 때만 알린다.
- 2주 동안 가치 신호가 없으면 주기를 낮추거나 끈다.
- cron이 만든 결과는 State Handoff / Proactive Watchlist / Outcome Feedback Loop 중 하나에 반드시 반영한다.

## 멀티에이전트 품질 게이트

중요 문서/고객 대면 산출물은 단독 완료하지 말고 역할을 나눈다.

```markdown
1. 현장 에이전트: 초안 작성 + 고객 맥락 반영
2. 검수 에이전트: 숫자/근거/assertion-grounding 검토
3. 메인 에이전트: 전략·톤·리스크 최종 점검
4. 사용자/고객: 외부 제출 승인
```

검수 기준:
- 숫자 출처가 있는가?
- 공고/요청사항과 1:1로 대응하는가?
- 과장·허위·근거 없는 표현이 있는가?
- 다음 액션과 책임자가 명확한가?

## 리포트 포맷

사용 회고나 고객사 점검 후 아래 형식으로 요약한다.

```markdown
# {고객사/에이전트} 운영 인사이트 — YYYY-MM-DD

## 한 줄 결론

## 잘 쓰는 부분
- 

## 한계/병목
- 

## 무펭이즘이 제공할 서비스 가치
- 

## 바로 적용할 운영 루프
- 상태 인수인계:
- 선제 체크:
- 온보딩 갭:
- 결과 회고:
- 검수 플로우:

## 다음 액션 3개
1.
2.
3.
```

## 원칙

- "많이 했다"보다 "이어받을 수 있다"가 중요하다.
- 고객사는 결과물을 원하지만, 무펭이즘은 결과물이 반복 개선되는 구조를 팔아야 한다.
- 선제 행동은 스팸이 아니라 놓치면 손해 보는 리스크를 조용히 줄이는 것이다.
- 회고 없는 문서 생산은 성장하지 않는다.
