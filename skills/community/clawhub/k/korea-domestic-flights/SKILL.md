---
name: korea-domestic-flights
description: Search, compare, and monitor 대한민국 domestic flights using a Playwright-backed airfare workflow. Use when the user wants 한국 국내선 항공권 최저가 조회, 김포-제주/부산-제주 같은 노선 비교, 편도/왕복 검색, 날짜 범위 최저가 탐색, 여러 국내 목적지 비교, 시간대 선호(늦은 출발/늦은 복귀) 반영, 국내선 운임 브리핑, 목적지+날짜 범위 최적 조합 탐색, or 목표가 이하 가격 감시/가격 알림 저장·점검. Accept common Korean airport names like 김포, 제주, 부산, 청주 and natural-language dates like 오늘/내일/모레/이번주말/내일부터 3일. Prefer this skill for Korean domestic airfare tasks; do not use it for international flights.
---

# Korea Domestic Flights

Use this skill for **대한민국 국내선 전용 항공권 검색**.

Current scope:
- 국내선 편도 검색
- 국내선 왕복 검색
- 날짜 범위 최저가 탐색
- 날짜별 가격 캘린더/히트맵 요약
- 다중 목적지 비교
- 다중 목적지 + 날짜 범위 최적 조합 탐색
- 다중 목적지 + 날짜 범위 비교에서도 목적지별 가격 캘린더 요약 제공
- JSON 출력
- 더 자연스러운 한국어 브리핑 출력
- 한글 공항명 입력 지원
- `오늘/내일/모레/이번주말/내일부터 3일` 같은 간단한 자연어 날짜 지원
- `2026-03-25~2026-03-30`, `20260325~20260330`, `2026-03-25부터 2026-03-30` 같은 명시 날짜 범위 지원
- 채팅 친화 래퍼 제공
- 시간대 필터(오전/오후/저녁, 출발 N시 이후, 복귀 N시 이후, 너무 이른 비행 제외)
- 최저가 외 시간 선호 기반 추천(예: 늦은 시간대 기준 추천)
- 왕복/날짜범위 검색에서 귀환편 시간 조건 반영
- 왕복 범위/조합 검색에서 가격만이 아닌 왕복 시간 균형 추천 제공
- 추천 결과에 가격 차이·시간 조건·왕복 균형 기반 추천 사유 설명 제공
- 목표가 기반 가격 감시 규칙 저장/목록/삭제/점검
- 가격 감시 규칙에 시간대 조건 저장/점검 지원
- 가격 알림 중복 방지(dedupe)
- 단일/다중 목적지 가격 감시
- 알림 메시지 포맷 커스터마이즈
- cron/브리핑 연동을 염두에 둔 JSON 저장 포맷
- Windows 작업 스케줄러 등록 초안 스크립트

Do not use it for 국제선.

## Source dependency

This skill wraps the local project clone at:

- `tmp/Scraping-flight-information`

Main reused entry points:
- `scraping.searcher.FlightSearcher`
- `scraping.parallel.ParallelSearcher`

If the clone or its dependencies are missing, searches will fail.

## Scripts

### 1) Single-route domestic search

```bash
python skills/korea-domestic-flights/scripts/search_domestic.py --origin 김포 --destination 제주 --departure 내일 --human
```

시간 조건 포함:

```bash
python skills/korea-domestic-flights/scripts/search_domestic.py --origin 김포 --destination 제주 --departure 내일 --time-pref "출발 10시 이후" --prefer late --human
```

Round trip:

```bash
python skills/korea-domestic-flights/scripts/search_domestic.py --origin GMP --destination CJU --departure 2026-03-25 --return-date 2026-03-28 --human
```

### 2) Date-range cheapest-day search

```bash
python skills/korea-domestic-flights/scripts/search_date_range.py --origin 김포 --destination 제주 --date-range "내일부터 3일" --human
```

Explicit range:

```bash
python skills/korea-domestic-flights/scripts/search_date_range.py --origin 김포 --destination 제주 --start-date 내일 --end-date 2026-03-30 --human
```

Round-trip-style date scan with fixed return offset:

```bash
python skills/korea-domestic-flights/scripts/search_date_range.py --origin 김포 --destination 제주 --date-range "다음주말" --return-offset 2 --time-pref "복귀 18시 이후" --human
```

### 3) Multi-destination comparison

```bash
python skills/korea-domestic-flights/scripts/search_multi_destination.py --origin 김포 --destinations 제주,부산,여수 --departure 내일 --human
```

Round trip comparison:

```bash
python skills/korea-domestic-flights/scripts/search_multi_destination.py --origin GMP --destinations CJU,PUS,RSU --departure 2026-03-25 --return-date 2026-03-28 --human
```

### 4) Multi-destination + date-range best-combo search

```bash
python skills/korea-domestic-flights/scripts/search_destination_date_matrix.py --origin 김포 --destinations 제주,부산 --date-range "내일부터 2일" --human
```

Round-trip offset scan across destinations:

```bash
python skills/korea-domestic-flights/scripts/search_destination_date_matrix.py --origin 김포 --destinations 제주,부산 --date-range "다음주말" --return-offset 2 --human
```

### 5) Chat-friendly wrapper

Use this first when the user is chatting naturally and you want the easiest invocation.

Single route:

```bash
python skills/korea-domestic-flights/scripts/chat_search.py --origin 김포 --destination 제주 --when 내일
```

Date range:

```bash
python skills/korea-domestic-flights/scripts/chat_search.py --origin 김포 --destination 제주 --when "내일부터 3일"
```

Multi-destination + range:

```bash
python skills/korea-domestic-flights/scripts/chat_search.py --origin 김포 --destinations 제주,부산 --when "내일부터 2일" --return-offset 1 --time-pref "출발 10시 이후, 늦은 시간 선호"
```

Add `--json` when structured output is needed; otherwise it defaults to a human-readable Korean briefing.

### 0) Hybrid diagnostics smoke/live checks

Fixture-based regression/smoke check:

```bash
python skills/korea-domestic-flights/scripts/hybrid_smoke_check.py
```

Shallow environment-only check:

```bash
python skills/korea-domestic-flights/scripts/hybrid_live_dry_run.py
```

Optional shallow live probe (non-brittle, no fare assertion):

```bash
python skills/korea-domestic-flights/scripts/hybrid_live_dry_run.py --probe
```

### 6) Price alert / watch rules

Store a single-date alert:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destination 제주 --departure 내일 --target-price 70000 --label "김포-제주 내일 특가"
```

Store a date-range alert:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destination 제주 --date-range "내일부터 3일" --target-price 80000 --label "김포-제주 3일 범위 감시"
```

Store a time-filtered alert:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destination 제주 --date-range "다음주말" --return-offset 2 --target-price 150000 --time-pref "복귀 18시 이후, 늦은 시간 선호" --label "주말 늦복 왕복 감시"
```

Store a multi-destination watch:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destinations 제주,부산,여수 --departure 내일 --target-price 90000 --label "김포 출발 내일 다중 목적지 감시"
```

Store a round-trip range alert with fixed return offset:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destination 제주 --date-range "다음주말" --return-offset 2 --target-price 150000 --label "주말 왕복 특가"
```

Store a custom message format:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destinations 제주,부산 --date-range "내일부터 3일" --target-price 85000 --message-template "[특가감시] {best_destination_label} {departure_date} {observed_price} / 기준 {target_price}"
```

Check all active rules:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py check
```

List saved rules:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py list
```

Remove a rule:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py remove --rule-id kdf-1234abcd
```

When a rule matches, `check` prints a human-readable Korean alert message to stdout so an upper-layer cron/briefing flow can forward it directly.

## Parameters

`search_domestic.py`
- `--origin`: 출발 공항 코드 또는 한글 공항명
- `--destination`: 도착 공항 코드 또는 한글 공항명
- `--departure`: 출발일 (`YYYY-MM-DD`, `YYYYMMDD`, `내일`, `모레`, `이번주말`, `다음주 금요일` 등)
- `--return-date`: 귀국일 (선택)
- `--adults`: 성인 수, 기본값 `1`
- `--cabin`: `ECONOMY|BUSINESS|FIRST`
- `--max-results`: 최대 결과 수
- `--time-pref`: 자연어 시간 조건 (`오전`, `오후`, `저녁`, `출발 10시 이후`, `복귀 18시 이후`, `너무 이른 비행 제외 8시`, `늦은 시간 선호` 등)
- `--depart-after`, `--return-after`, `--exclude-early-before`: 옵션 기반 시간 필터
- `--prefer`: `late|morning|afternoon|evening` 시간 선호 추천
- `--human`: 자연스러운 한국어 브리핑 출력 (`최저가` / `시간대 추천` / `왕복 균형 추천` 중심 구획형 요약)

`search_date_range.py`
- `--origin`: 출발 공항 코드 또는 한글 공항명
- `--destination`: 도착 공항 코드 또는 한글 공항명
- `--start-date`: 범위 시작일
- `--end-date`: 범위 종료일
- `--date-range`: 자연어 범위 (`내일부터 3일`, `이번주말`, `2026-03-25~2026-03-30`)
- `--return-offset`: 왕복 탐색용 귀국 오프셋 일수
- `--adults`: 성인 수
- `--cabin`: `ECONOMY|BUSINESS|FIRST`
- `--time-pref`, `--depart-after`, `--return-after`, `--exclude-early-before`, `--prefer`: 시간 필터/시간 선호 추천
- 시간 조건이 있으면 전체 날짜를 병렬로 빠르게 훑은 뒤 저가 후보·인접 날짜·범위 커버리지 앵커를 함께 상세 재검증하는 하이브리드 모드로 전환됨
- 상세 재검증 후 시간 조건 일치 결과가 너무 적거나, 시간조건 탈락/빈결과 유사 패턴이 강하면 fallback 후보 확장을 한 번 더 수행할 수 있음
- `summary.search_metadata` / 최상위 `search_metadata` / `logs` 에 하이브리드 여부, 전체 스캔 수, 초기/추가 재검증 수, fallback 여부, 시간 조건 요약과 `refine_diagnostics`(시간조건 탈락 / usable match 없음 / 빠른스캔-상세 불일치 빈결과 / 출발·복귀 시간정보 부족 / 가격정보 부족 분류, 샘플, user/developer 힌트, `ranked_reasons`, `dominant_reason_code`, `primary_interpretation`)가 기록됨
- fallback 판단 요약은 `fallback_decision` / `fallback_reason_codes` 에 구조화되어 남음
- 결과 요약에는 날짜별 가격 캘린더/히트맵(`summary.price_calendar`)이 포함됨
- `--human`: 자연스러운 한국어 브리핑 출력

`search_multi_destination.py`
- `--origin`: 출발 공항 코드 또는 한글 공항명
- `--destinations`: 쉼표로 구분한 여러 목적지 (코드 또는 한글)
- `--departure`: 출발일
- `--return-date`: 귀국일 (선택)
- `--adults`: 성인 수
- `--cabin`: `ECONOMY|BUSINESS|FIRST`
- `--time-pref`, `--depart-after`, `--return-after`, `--exclude-early-before`, `--prefer`: 시간 필터/시간 선호 추천
- `--human`: 목적지 간 가격 차이와 추천이 포함된 한국어 브리핑 출력

`search_destination_date_matrix.py`
- `--origin`: 출발 공항 코드 또는 한글 공항명
- `--destinations`: 쉼표로 구분한 여러 목적지
- `--start-date`, `--end-date`: 날짜 범위 지정
- `--date-range`: 자연어 날짜 범위 지정
- `--return-offset`: 출발일 기준 귀국 오프셋 일수
- `--adults`: 성인 수
- `--cabin`: `ECONOMY|BUSINESS|FIRST`
- `--time-pref`, `--depart-after`, `--return-after`, `--exclude-early-before`, `--prefer`: 시간 필터/시간 선호 추천
- 시간 조건이 있으면 전체 조합을 목적지별 병렬 스캔으로 먼저 좁힌 뒤 저가 조합·목적지별 후보·인접 날짜 조합·커버리지 앵커를 함께 상세 재검증하는 하이브리드 모드로 전환됨
- 상세 재검증 후 시간 조건 일치 조합이 너무 적거나, 시간조건 탈락/빈결과 유사 패턴이 강하면 fallback 후보 확장을 한 번 더 수행할 수 있음
- `summary.search_metadata` / 최상위 `search_metadata` / `logs` 에 하이브리드 여부, 전체 스캔 수, 초기/추가 재검증 수, fallback 여부, 시간 조건 요약과 `refine_diagnostics`(시간조건 탈락 / usable match 없음 / scraper-empty 유사 분류 / 시간·가격 정보 완전누락·부분누락, 샘플, `human_hint`/`developer_hint`, `extraction_summary`, `ranked_reasons`, `dominant_reason_code`, `primary_interpretation`)가 기록됨
- fallback 판단 요약은 `fallback_decision` / `fallback_reason_codes` 에 구조화되어 남음
- `--human`: 전체 최적 조합 + 목적지별 베스트 브리핑 출력

`chat_search.py`
- `--origin`: 출발 공항명/코드
- `--destination`: 단일 목적지
- `--destinations`: 다중 목적지
- `--when`: 자연어 날짜/날짜범위
- `--departure`: 명시적 출발일
- `--return-date`: 명시적 귀국일
- `--return-offset`: 날짜범위 왕복 오프셋. `chat_search.py`에서는 다중 목적지 + 명시적 `--departure` 와 함께 써도 단일일 매트릭스 왕복 탐색으로 라우팅됨
- `--time-pref`: 자연어 시간 선호/필터 입력
- `--depart-after`, `--return-after`, `--exclude-early-before`, `--prefer`: 옵션 기반 시간 필터
- `--json`: JSON 출력, 생략 시 사람이 읽기 쉬운 브리핑 출력

`price_alerts.py`
- `add`: 감시 규칙 저장
  - `--origin`: 출발 공항
  - `--destination` 또는 `--destinations`: 단일/다중 목적지
  - `--departure`: 단일 날짜 감시
  - `--return-date`: 왕복 귀국일
  - `--date-range`: 날짜 범위 감시
  - `--return-offset`: 날짜 범위 왕복 감시 시 귀국 오프셋
  - `--adults`: 성인 수
  - `--cabin`: `ECONOMY|BUSINESS|FIRST`
  - `--target-price`: 목표가(원)
  - `--label`: 사람이 읽을 이름
  - `--time-pref`, `--depart-after`, `--return-after`, `--exclude-early-before`, `--prefer`: 시간대 조건/선호 저장
  - `--message-template`: 커스텀 알림 포맷
  - `--store`: 저장 파일 경로 오버라이드
  - 동일 조건+목표가 규칙은 fingerprint 기준으로 중복 저장되지 않음
- `list`: 저장된 규칙 목록 출력
- `check`: 활성 규칙 점검, 목표가 충족 시 한국어 알림 출력
  - 동일한 결과는 `notify.dedupe_key` 기준으로 재알림 억제
  - `--no-dedupe` 로 강제 재출력 가능
- `render`: 마지막 `last_result` 를 현재 템플릿으로 미리보기
- `remove`: 규칙 삭제

## References

Read these only when needed:
- `references/domestic-airports.md`: 국내 공항 코드/이름 매핑
- `references/price-alerts-schema.md`: 가격 감시 JSON 저장 포맷, dedupe, 다중 목적지 감시, 메시지 템플릿, cron/스케줄러 연결 힌트

## Operational notes

- This skill depends on a working Playwright browser environment.
- If browser init fails, install or repair Chromium/Chrome/Edge in the source repo environment.
- The provider site DOM may change; if results suddenly disappear, the upstream scraper may need maintenance.
- For stable chat use, prefer `chat_search.py` or `--human` summaries unless structured JSON is explicitly needed.
- Prefer domestic routes only; if the user asks for ICN-NRT or any overseas route, do not use this skill.
