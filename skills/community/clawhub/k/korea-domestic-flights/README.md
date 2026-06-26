# korea-domestic-flights

대한민국 **국내선 항공권 검색·비교·날짜 범위 탐색·가격 감시**를 위한 OpenClaw 스킬입니다.

이 스킬은 Playwright 기반 항공권 검색 흐름을 감싸서 다음 같은 작업을 처리합니다.

- 김포-제주, 부산-제주 같은 **국내선 단일 노선 검색**
- **왕복 검색** 및 시간대 조건 반영
- **날짜 범위 최저가 탐색**
- **다중 목적지 비교**
- **다중 목적지 + 날짜 범위 최적 조합 탐색**
- **가격 캘린더/히트맵 요약**
- **목표가 기반 가격 감시 규칙 저장/점검**

> 국제선에는 사용하지 않습니다.

---

## 핵심 기능

### 1. 단일 노선 검색
- 편도/왕복 검색
- 한글 공항명 입력 지원 (`김포`, `제주`, `부산` 등)
- 시간대 조건 반영 (`출발 10시 이후`, `복귀 18시 이후` 등)
- 추천 사유 설명 출력

### 2. 날짜 범위 최저가 탐색
- `내일부터 3일`, `이번주말`, `다음주말`, `2026-03-25~2026-03-30` 같은 자연어/명시 범위 입력 지원
- 날짜별 가격 캘린더 제공
- 왕복 검색 시 균형 추천 제공
- 시간 조건이 있을 때는 빠른 전체 스캔 후 저가 후보 + 인접 날짜 + 범위 커버리지 앵커를 함께 상세 재검증하는 하이브리드 최적화 적용
- 시간 조건 하이브리드에서 상세 재검증 결과가 너무 적거나 시간조건 탈락/빈결과 유사 패턴이 강하면 fallback 후보 확장을 한 번 더 수행해 false no-result / false-best 위험을 줄임

### 3. 다중 목적지 비교
- 예: 김포 출발로 제주/부산/여수 중 어디가 가장 유리한지 비교
- 목적지별 최저가/추천/가격 차이 설명 제공

### 4. 목적지 + 날짜 범위 매트릭스 탐색
- 여러 목적지와 여러 날짜 조합을 한 번에 비교
- 최적 조합 + 목적지별 가격 캘린더 제공

### 5. 가격 감시 / 알림
- 목표가 이하로 내려오면 알림 메시지 생성
- 단일 목적지 / 다중 목적지 / 날짜 범위 감시 지원
- 시간대 조건 포함 규칙 저장 가능
- dedupe(중복 억제) 지원

---

## 빠른 예시

### 단일 검색
```bash
python skills/korea-domestic-flights/scripts/search_domestic.py --origin 김포 --destination 제주 --departure 내일 --human
```

### 날짜 범위 검색
```bash
python skills/korea-domestic-flights/scripts/search_date_range.py --origin 김포 --destination 제주 --date-range "내일부터 3일" --human
```

### 다중 목적지 + 날짜 범위 검색
```bash
python skills/korea-domestic-flights/scripts/search_destination_date_matrix.py --origin 김포 --destinations 제주,부산 --date-range "다음주말" --return-offset 2 --human
```

### 시간 조건 포함 가격 감시 규칙 저장
```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add --origin 김포 --destination 제주 --date-range "다음주말" --return-offset 2 --target-price 150000 --time-pref "복귀 18시 이후, 늦은 시간 선호" --label "주말 늦복 왕복 감시"
```

---

## 출력 특징

이 스킬은 단순 최저가만 보여주지 않고, 가능하면 아래 정보도 같이 제공합니다.

- 추천 사유
- 시간대 추천
- 왕복 균형 추천
- 날짜별 가격 캘린더
- 목적지별 가격 캘린더
- 사람용 출력에서는 `최저가`, `시간대 추천`, `왕복 균형 추천` 같은 구획을 나눠 더 읽기 쉽게 표시
- 사람용 출력에서는 너무 길어지지 않도록 캘린더를 일부만 미리 보여주고 나머지 일수는 축약 표시

예를 들어:
- **추천:** 이번 조건에서는 부산(PUS) 조합이 가장 유리합니다.
- **추천 사유:** 2위보다 더 저렴하고, 시간 조건에도 맞습니다.
- **왕복 균형 추천:** 아주 약간 더 비싸더라도 시간대가 더 무난한 조합을 별도로 제안할 수 있습니다.

---

## 의존성

이 스킬은 다음 로컬 소스 저장소를 감쌉니다.

- `tmp/Scraping-flight-information`

필요 조건:
- Playwright/브라우저 실행 가능 환경
- upstream 검색 로직이 정상 동작할 것

환경이 깨졌거나 사이트 DOM이 바뀌면 결과가 없거나 오류가 날 수 있습니다.

---

## 현재 확인된 동작 상태

최근 점검 기준:
- 모든 주요 스크립트 `py_compile` 통과
- `price_alerts.py add/list/remove` 동작 확인
- `chat_search.py`를 통한 다중 목적지+날짜 범위 JSON 검색 동작 확인
- `chat_search.py`에서 다중 목적지 + 명시적 출발일 + `--return-offset` 조합이 날짜 매트릭스로 올바르게 라우팅되도록 보정
- 다중 목적지+날짜 범위 검색에서 목적지별 `price_calendar` 출력 확인
- `references/hybrid-smoke-fixtures.json` 기반 회귀/스모크 진단 케이스 확인
- `hybrid_live_dry_run.py`로 환경 전용 또는 얕은 live probe 점검 가능

---

## 한계 / 주의점

- 실제 검색은 외부 사이트 상태와 브라우저 환경에 영향을 받습니다.
- 날짜 범위/다중 목적지/왕복 검색은 실행 시간이 길 수 있지만, 시간 조건이 있는 범위/매트릭스 검색은 하이브리드 최적화로 전체 조합을 먼저 빠르게 훑은 뒤 저가 후보·인접 날짜·커버리지 앵커를 함께 상세 검색합니다.
- 상세 재검증 후 시간 조건 일치 결과가 너무 적으면 fallback 후보 확장을 추가로 수행할 수 있습니다.
- JSON `summary.search_metadata` / 최상위 `search_metadata` 와 `logs` 에 하이브리드 사용 여부, 초기/추가 재검증 수, fallback 여부, 시간 조건 요약과 `refine_diagnostics`(시간조건 탈락 / usable match 없음 / 빠른스캔-상세 불일치 빈결과 / 시간·가격 정보 완전누락/부분누락 분류, 샘플, `human_hint`/`developer_hint`, `extraction_summary`, `ranked_reasons`, `dominant_reason_code`, `primary_interpretation`)가 기록됩니다.
- fallback 판단은 `fallback_decision` / `fallback_reason_codes` 로 구조화되어 남아 extraction incompleteness 우세인지 genuine time-filter rejection 우세인지 구분하기 쉽게 했습니다.
- 사람용 출력에서는 필요할 때만 한 줄짜리 `참고:` 진단 힌트를 덧붙이고, 더 자세한 디버그성 힌트와 커버리지 수치는 JSON 메타데이터에만 남겨서 사람용 출력이 시끄러워지지 않게 유지합니다.
- 국제선은 범위 밖입니다.

자세한 사용법은 `SKILL.md`를 참고하세요.
