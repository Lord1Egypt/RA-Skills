# naver-real-estate-search

네이버 부동산 기반으로 대한민국 아파트/빌라/오피스텔 매물 조회, 단지 후보 탐색, 비교 브리핑, 가격 감시를 수행하는 OpenClaw 스킬입니다.

## 주요 개선점
- alias/후보 캐시 구조 강화 (`candidate-cache.json` v3 스타일)
- candidate-cache seed/수동 학습 CLI 추가 (`--seed-candidate`, `--seed-candidate-file`, `--show-cache`)
- 서울 주요 단지용 candidate seed 자동 생성기 추가 (`scripts/build_candidate_seeds.py`)
- 지역명/단지명 파서 보강, cold-start 후보 탐색 품질 개선
- `신월시영아파트`, `답십리두산위브` 같은 실사용 질의에 대해 reference-seed/manual-review fallback 보강
- 429 감지 시 direct URL/complex ID 우선 흐름을 유지하는 fallback 메타 추가
- 동일 평형 기준 비교 요약 추가
- 한국어 비교 브리핑과 대표 매물 요약 개선
- watch schema 확장: `last_seen`, `events`, dedupe, 새 매물/가격하락 감지
- 상위 레이어(텔레그램/브리핑) 연동용 stdout JSON 구조 개선

## candidate seed 운영 흐름

### 1) generated 초안 만들기
```bash
python skills/naver-real-estate-search/scripts/build_candidate_seeds.py --print-summary
python skills/naver-real-estate-search/scripts/build_candidate_seeds.py --input skills/naver-real-estate-search/references/seoul-major-complexes.seed-input.json --output skills/naver-real-estate-search/references/candidate-seeds.generated.json --pause 0.1 --print-summary
```

- 입력: `references/seoul-major-complexes.seed-input.json`
- 출력: `references/candidate-seeds.generated.json`
- 각 결과에는 `confidence`, `verification_status`, 자동 생성 `aliases`, `candidate_pool`, `evidence`, `blocked_reasons`가 포함됩니다.
- 자동 생성 결과는 **운영 seed가 아니라 generated 초안**입니다.

### 2) preview로 승격 후보 / 검수 큐 확인
```bash
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --json
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --only-names "리센츠,은마" --json
```

- 기본 동작은 preview입니다. 파일은 바꾸지 않습니다.
- `verified/weak-verified + complex_id + confidence` 기준으로 accepted 후보를 고릅니다.
- 나머지는 `manual_review_queue`로 정리할 후보로 봅니다.
- 일부 단지만 볼 때는 `--only-names`, 빼고 싶을 때는 `--exclude-names`를 씁니다.

### 3) 실제 반영
```bash
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --apply-target --apply-cache --json
```

- `--apply-target`: `references/candidate-seeds.json` 갱신
- `--apply-cache`: accepted 항목만 `data/candidate-cache.json` warm-cache
- preview 없이 곧바로 apply하지 말고, 최소 한 번은 summary를 확인하는 편이 안전합니다.

현재 2026-03-20 기준 운영 검수 결과:
- 운영 유지: `리센츠`
- 오검출 제외: `엘스`, `트리지움`
- manual review: `은마`, `래미안대치팰리스`, `아크로리버파크`, `래미안원베일리`, `목동신시가지7단지`, `신월시영아파트`, `답십리두산위브`

> 실사용 안정화 메모: production complex ID를 아직 못 확보한 단지도 `manual_review_queue` + `seoul-major-complexes.seed-input.json`에 남겨 두면, `--list-candidates`에서 완전 빈 응답 대신 **reference-seed 후보 힌트**를 돌려줄 수 있습니다.

## 스크립트

### 1) 후보 탐색 / 단일 조회 / 비교
```bash
python skills/naver-real-estate-search/scripts/search_real_estate.py --query "잠실 리센츠 전세 30평대"
python skills/naver-real-estate-search/scripts/search_real_estate.py --query "잠실 리센츠와 엘스 전세 비교 30평대" --compare --json
python skills/naver-real-estate-search/scripts/search_real_estate.py --query "서울 양천구 신월동 신월시영아파트 전세" --list-candidates --json
```

### 2) 채팅형 브리핑
```bash
python skills/naver-real-estate-search/scripts/chat_real_estate.py --query "잠실 리센츠 전세 30평대"
python skills/naver-real-estate-search/scripts/chat_real_estate.py --query "잠실 리센츠와 엘스 전세 비교 30평대" --compare
```

### 3) 가격 감시 / 새 매물 감지
```bash
python skills/naver-real-estate-search/scripts/watch_real_estate.py add --name "리센츠 전세 30평대" --query "잠실 리센츠 전세 30평대" --target-max-price 950000000 --notify-on-new --notify-on-price-drop
python skills/naver-real-estate-search/scripts/watch_real_estate.py check --preview
python skills/naver-real-estate-search/scripts/watch_real_estate.py check --json
```

## 저장 파일
- `data/candidate-cache.json`: 후보 단지 alias/주소/ID 캐시
- `data/watch-rules.json`: 감시 규칙 + 최근 관측 상태 + 이벤트 히스토리
- `references/candidate-seeds.json`: 초기 alias seed / warm-cache 예시

## candidate-cache 관리
```bash
python skills/naver-real-estate-search/scripts/search_real_estate.py --seed-candidate-file
python skills/naver-real-estate-search/scripts/apply_generated_seeds.py --apply-target --apply-cache --json
python skills/naver-real-estate-search/scripts/search_real_estate.py --seed-candidate --complex-id 1147 --candidate-name "리센츠" --candidate-address "서울특별시 송파구 잠실동" --candidate-aliases "잠실 리센츠,잠실리센츠"
python skills/naver-real-estate-search/scripts/search_real_estate.py --show-cache --query "리센츠"
```

- 운영 seed 전체를 cache에 한 번에 반영할 때는 `search_real_estate.py --seed-candidate-file`를 씁니다.
- generated 초안에서 **accepted만 선별 반영**하려면 `apply_generated_seeds.py --apply-target --apply-cache`가 더 안전합니다.
- 반복 조회가 필요한 실존 단지는 먼저 cache에 seed/학습시켜 두면 alias mismatch와 cold-start 실패를 줄일 수 있습니다.
- `references/candidate-seeds.json`은 **운영 검수 통과 seed만 넣는 파일**입니다.
- generated 초안 검토 결과, 오검출/미검증 항목은 `manual_review_queue`로 분리하고 `entries[]`에는 넣지 않습니다.
- 특히 `신월시영아파트`, `은마`, `목동신시가지7단지`처럼 alias나 숫자 단지명이 흔들리는 케이스는 direct complex URL/ID 확보 전까지 운영 seed로 올리지 않는 편이 안전합니다.

## seed 검수 기준 요약
- `verified`: 이름/주소/ID 정합성이 맞아 운영 seed에 바로 반영 가능
- `weak-verified`: 자동 근거는 있으나 사람이 한 번 더 보고 승격
- `unresolved`: complex_id 미확보 또는 근거 부족, 운영 seed 제외
- `blocked`: 403/429 등 외부 차단으로 검증 중단, direct URL/ID 수동 확보 우선

서울 주요 단지 보강 우선순위:
1. 신월시영아파트
2. 은마 / 래미안대치팰리스
3. 래미안원베일리 / 아크로리버파크
4. 목동신시가지7단지
5. 엘스 / 트리지움

## 배포 체크리스트
1. self-test 실행
2. 대표 자연어 질의/후보 탐색/감시 check 실제 실행
3. `references/candidate-seeds.json`의 entries/manual_review_queue가 검수 결과와 일치하는지 확인
4. skill 패키징
5. GitHub tag/release 및 ClawHub publish
