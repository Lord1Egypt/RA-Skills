# candidate seed 자동 생성 메모

## 목적
- 서울 주요 단지 seed 리스트를 입력받아 `candidate-seeds.generated.json` 초안을 만든다.
- 기존 `candidate-seeds.json`, `candidate-cache.json`, `search_real_estate.py`와 연결 가능한 구조를 유지한다.
- 운영용 승격 기준은 `verification_status in {verified, weak-verified}` 로 두되, **실무에서는 이름/주소/ID 정합성 검수까지 통과한 항목만 `entries[]`에 반영**한다.

## 입력/출력

### 입력
- `references/seoul-major-complexes.seed-input.json`
- shape:

```json
{
  "seeds": [
    {
      "name": "리센츠",
      "city": "서울특별시",
      "district": "송파구",
      "neighborhood": "잠실동",
      "aliases": ["잠실 리센츠", "잠실리센츠"]
    }
  ]
}
```

### 출력
- `references/candidate-seeds.generated.json`
- 핵심 필드:
  - `entries[]`: 자동 검증상 승격 후보
  - `results[]`: 전체 생성 결과 + evidence
  - `unresolved[]`: 후속 수동 검증 대상

## 상태값 운영 기준

### `verified`
다음을 모두 만족하는 항목으로 본다.
- `complex_id`가 있음
- 상세 조회된 단지명 정규화 결과가 seed 이름과 정확히 맞거나 매우 강하게 일치함
- 주소에 구/동 힌트가 자연스럽게 맞음
- 오검출 정황이 없음

운영 액션:
- `candidate-seeds.json`의 `entries[]`에 바로 반영 가능
- warm-cache baseline으로 사용 가능

### `weak-verified`
다음을 만족하는 항목으로 본다.
- `complex_id`가 있음
- 이름/주소가 대체로 맞지만 일부 힌트만 확보됐거나 429 직전 등으로 근거가 약함
- 사람이 빠르게 다시 봤을 때 오검출 가능성이 낮음

운영 액션:
- 자동 반영 후보는 될 수 있지만, **서울 주요 단지 운영 seed는 사람이 한 번 더 보고 `entries[]`에 승격**하는 편이 안전
- 저장 시 note에 검수 근거를 남긴다

### `unresolved`
다음을 의미한다.
- `complex_id`를 못 찾았거나
- 후보는 있었지만 이름/주소 검증까지 못 갔거나
- broad query만으로는 신뢰할 수 있는 후보를 고르지 못함

운영 액션:
- `entries[]`에는 넣지 않음
- `manual_review_queue`로 넘겨 direct URL/ID를 확보한 뒤 재검증

### `blocked`
다음을 의미한다.
- 403/429/검색 HTML 차단 등 외부 제약 때문에 자동 검증 흐름이 끊김
- 결과 부재가 곧 단지 부재를 뜻하지는 않음

운영 액션:
- `entries[]`에는 넣지 않음
- 차단이 풀릴 때까지 broad query 재시도보다 direct URL/ID 수동 확보를 우선
- 운영 가치가 높은 단지(예: 신월시영아파트, 은마)는 우선 보강 큐로 올린다

## 생성 순서
1. 입력 seed의 이름/지역을 바탕으로 alias를 자동 확장한다.
2. 기존 `references/candidate-seeds.json`의 verified baseline과 이름/alias exact 매칭을 먼저 본다.
3. `candidate-cache.json` exact/contains 매칭으로 warm-cache 힌트를 찾는다.
4. 네이버 검색 HTML에서 complex link/ID를 추출한다.
5. 가능하면 단지 상세 API로 이름/주소/세대수를 조회해 검증한다.
6. `confidence`, `verification_status`, `candidate_pool`, `evidence`, `blocked_reasons`를 남긴다.

## 운영 권장
- 생성 파일의 `entries[]`는 그대로 신뢰하지 말고, **오검출 여부를 반드시 다시 본다.**
- 특히 잠실 대단지처럼 비슷한 문맥이 자주 섞이는 곳에서는 다른 complex ID로 잘못 수렴할 수 있다.
- `results[]`에 complex_id가 있어도 `verification_status`가 `unverified`면 자동 투입하지 않는다.
- `verification_status`가 `weak-verified`여도 서울 주요 단지는 수동 검수 후 승격한다.
- 403/429가 반복되면 broad query 대신 direct complex URL/ID로 수동 보강한다.

## preview / apply 운영 절차

### 1. generated 초안 생성
```bash
python skills/naver-real-estate-search/scripts/build_candidate_seeds.py --print-summary
```

### 2. preview 확인
```bash
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --json
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --only-names "리센츠,은마" --json
```

여기서 확인할 것:
- `accepted[]`에 들어간 단지가 정말 운영 승격 대상인지
- `rejected[]`의 `complex_id`가 오검출인지
- `manual_review_queue_count`가 기대와 맞는지

### 3. 운영 반영
```bash
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --apply-target --apply-cache --json
```

반영 결과:
- `references/candidate-seeds.json`의 `entries` / `manual_review_queue` 갱신
- accepted 항목만 `data/candidate-cache.json`에 warm-cache

### 4. 수동 보강
자동 승격이 어려운 단지는 direct complex URL/ID 확보 후 다음처럼 수동 보강한다.

```bash
python skills/naver-real-estate-search/scripts/search_real_estate.py --seed-candidate --complex-id <ID> --candidate-name "단지명" --candidate-address "주소" --candidate-aliases "별칭1,별칭2"
```

## 실제 검수 요약 (2026-03-20)

### 운영 반영
- `리센츠 -> 1147`: 유지 (`verified`)

### generated에서 제외
- `엘스`: generated가 `1147`(리센츠)로 잘못 수렴해서 제외
- `트리지움`: generated가 `1147`(리센츠)로 잘못 수렴해서 제외

### 수동 검증 대기
- `은마`
- `래미안대치팰리스`
- `아크로리버파크`
- `래미안원베일리`
- `목동신시가지7단지`
- `신월시영아파트`
- `답십리두산위브`

### 우선 보강 추천 순서
1. `신월시영아파트` — alias 난이도가 높고 403 영향이 커서 baseline 가치가 큼
2. `답십리두산위브` — 실사용 질의 빈도가 높고 현재 cold-start에서 빈 응답이 나기 쉬움
3. `은마`, `래미안대치팰리스` — 대치권 대표 비교 질의 대응용
4. `래미안원베일리`, `아크로리버파크` — 반포권 대표 비교 질의 대응용
5. `목동신시가지7단지` — 숫자 단지형 alias 안정화용
6. `엘스`, `트리지움` — 잠실권 분리 baseline 확정용

complex ID를 아직 못 찾았더라도 아예 버리지 말고 `manual_review_queue`와 `seed-input`에 남겨 둔다. 그러면 후보 탐색 시 reference-seed fallback으로 노출할 수 있어, 실사용에서 `0건` 대신 검수 대기 후보 힌트를 줄 수 있다.

## 한계
- 검색 HTML 구조 변화에 취약하다.
- 네이버 상세 API 429 발생 시 검증 성공률이 크게 떨어진다.
- warm-cache가 부족하면 broad query만으로는 서울 주요 단지 전체를 안정적으로 맞추기 어렵다.
- 따라서 자동 생성은 초안/보조 도구로 보고, 운영 seed는 검증 승격 단계를 두는 것이 안전하다.
