# naver-real-estate-search 설계 메모

## 목표
- 대한민국 / 네이버 부동산 맥락에 맞는 OpenClaw 스킬 제공
- 자연어 요청을 최소 실행 가능한 검색 파라미터로 빠르게 축약
- `twbeatles/naverland-scrapper` 내부 로직을 가능한 범위에서 재사용
- 429 환경에서도 **direct URL/ID 우선 → 후보 좁히기 → 비교 → 감시** 흐름 유지

## 이번 고도화 핵심

### 1) 식별/안정성
- candidate cache를 단순 리스트에서 `version/entries/updated_at` 구조로 확장하고, seed/import/list 관리용 CLI를 추가
- alias 변형 생성 강화: 원문 / 공백 정리 / suffix 제거 / `아파트` 재부착 / 일부 지역 alias 확장
- 자연어 파서 강화: raw subject, location hint, direct complex ID 추출 보존
- cold-start 후보 탐색 시 `지역 + 단지명`, raw subject, cleaned query를 조합한 다중 검색어 전략 사용
- 점수화 기준 강화: 이름 정규화, alias, 질의 토큰, 주소 내 지역 힌트, 세대수 신뢰도 반영
- `신월시영아파트` 같은 케이스에서 alias cache warm-up 이후 재질문 성공률이 높아지도록 설계
- `references/candidate-seeds.json`을 통해 자주 쓰는 단지 후보를 운영 전 warm-cache 할 수 있게 설계
- 429 발생 시 메타에 상태를 남기고 direct URL/ID 우선 재시도 흐름을 유지

### 2) 비교/출력
- 거래유형별 `min/avg/median/max` 요약 추가
- `area_summary`를 도입해 동일 평형 버킷(예: `33평`) 기준 비교 가능하게 확장
- compare 결과에 `compare_insights.trade`, `compare_insights.same_area` 계층 추가
- 한국어 브리핑에서:
  - 전체 평균 비교 문장
  - 동일 평형 기준 비교 문장
  - 가격 분산 해석 문장
  - 대표 매물 bullet 정리
  를 더 자연스럽게 생성

### 3) 감시/연동
- watch schema를 `schema_version`, `rules`, `events`, `last_seen`, `last_checked_at` 구조로 확장
- rule 단위 옵션 추가:
  - `target_max_price`
  - `notify_on_new`
  - `notify_on_price_drop`
- check 결과 stdout JSON을 상위 레이어 친화적으로 정리:
  - `kind`
  - `schema_version`
  - `checked_at`
  - `alert_count`
  - `alerts[]`
  - `message_preview`
  - `summary`
- `last_seen` + `dedupe_key` 기반 중복 알림 억제
- snapshot에 `complex_info`, `market_summary`, `meta`를 넣어 텔레그램/브리핑 레이어가 재가공하기 쉽게 만듦

## 후보 탐색 전략 상세

1. direct complex ID / URL / 텍스트 내 complex ID를 먼저 본다.
2. cache에서 alias exact/contains 매칭을 먼저 시도한다.
3. 실패 시 web search를 쓰되 단일 키워드 하나만 쓰지 않는다.
   - raw subject
   - cleaned query
   - candidate keyword
   - location hint
   - `지역 + 단지명` 조합
4. 수집한 complex ID에 대해 상세 API를 조회해 이름/주소/세대수 보강
5. 점수 상위 후보만 반환

## 429 운영 원칙
- 먼저 짧은 backoff로 재시도한다.
- 여전히 실패하면 더 넓은 탐색으로 밀어붙이지 않는다.
- 사용자나 상위 레이어에 다음을 유도한다.
  - direct complex ID
  - direct URL
  - 후보 1~3개만 좁혀 재시도

## watch JSON 예시

```json
{
  "kind": "naver-real-estate-watch-check",
  "schema_version": 2,
  "checked_at": 1760000000,
  "alert_count": 2,
  "alerts": [
    {
      "rule": {"id": "rule-abcd1234", "name": "리센츠 전세 30평대"},
      "matched_count": 1,
      "matched": [
        {
          "event_type": "target_hit",
          "article_key": "1147:123456789",
          "price": 950000000,
          "price_text": "9억 5,000",
          "article_url": "https://new.land.naver.com/..."
        }
      ],
      "snapshot": {
        "complex_info": {"name": "리센츠"},
        "market_summary": {"전세": {"count": 8}},
        "meta": {"rate_limited": false}
      }
    }
  ]
}
```

## 테스트 권장 시나리오
- `--self-test`
- `--parse-only` 로 자연어 파서 확인
- `--list-candidates` 로 tricky alias 확인
- direct complex ID 조회
- 비교 브리핑 확인
- watch add/check 및 두 번째 check에서 dedupe 동작 확인

## 추가 개선 후보
- Playwright 세션 재사용 기반 429 회피력 향상
- 실거래가/전세가율 같은 파생 지표 추가
- 특정 지역 사전(alias seed) 확장
- 텔레그램 markdown-safe formatter 별도 스크립트 추가
