# OpenClaw Skill: Korea Air Quality

`openclaw-korea-air-quality`는 대한민국 지역의 **미세먼지 / 초미세먼지 / 오존 / 대기질 요약 / 위치 기반 조회 / 알림 / 아침 브리핑**을 다루기 위한 **OpenClaw AgentSkill 저장소**입니다.

이 저장소는 일반 파이썬 앱이 아니라, **OpenClaw에서 설치·호출·자동화하는 스킬 저장소**입니다.

이 스킬이 다루는 대표 요청:
- `답십리동 미세먼지 알려줘`
- `내 위치 기준으로 공기질 알려줘`
- `초미세먼지 나쁨 이상이면 알려줘`
- `매일 아침 7시 30분에 답십리동 브리핑해줘`
- `서울, 수원, 인천 공기질 비교해줘`

## 이 저장소가 OpenClaw 스킬인 이유

- 권장 저장소명: `openclaw-korea-air-quality`
- 스킬 엔트리: `SKILL.md`
- 로컬 실행용 CLI: `scripts/air_quality.py`
- 배포 결과물: `korea-air-quality.skill`
- OpenClaw cron / 알림 / 브리핑 자동화 흐름과 연결되도록 설계됨

## 현재 상태 한눈에 보기

### 지금 바로 동작하는 것

- **AirKorea 기반 대한민국 대기질 조회**
- Open-Meteo 기반 fallback 조회
- 지역 alias / 동·구 fallback (`답십리동`, `동대문구`, `성동구`, `분당`, `판교`, `영통`, `잠실` 등)
- 사용자 기본 지역 저장/조회
- 사용자 기본 위치 좌표 저장/조회
- 저장된 위치 기반 조회 우선 적용
- 여러 지역 비교 CLI
- 대기질 알림 규칙 추가/목록/점검
- 중복 알림 방지 상태 저장
- 날씨 + 대기질 결합 아침 브리핑
- OpenClaw cron 초안 생성 (`cron-plan`)
- provider 설정 저장/조회 (`setup-provider`, `show-config`)
- AirKorea 시도 단위 실시간 측정 JSON/XML 파싱 fallback

### 참고

- 실제 국내 실측값을 쓰려면 **`AIRKOREA_API_KEY` 또는 `data/config.json`의 `airkorea_api_key`** 가 필요함
- 키가 없는 환경에서도 fallback으로 `openmeteo` provider 사용 가능

## 빠르게 써보기

### 1) 현재 대기질 조회

```bash
python scripts/air_quality.py now 답십리동
python scripts/air_quality.py now 답십리동 --provider airkorea
python scripts/air_quality.py now 서울 --json
```

### 2) 기본 지역 / 위치 저장

```bash
python scripts/air_quality.py save-default telegram:8209218742 답십리동
python scripts/air_quality.py save-location telegram:8209218742 37.5666 127.0569 --label 답십리동
python scripts/air_quality.py show-default telegram:8209218742 --json
python scripts/air_quality.py now --user telegram:8209218742
```

### 3) 여러 지역 비교

```bash
python scripts/air_quality.py compare 서울 수원 인천
```

### 4) 알림 규칙 추가 / 점검

```bash
python scripts/air_quality.py alert-add telegram:8209218742 답십리동 pm2_5 나쁨
python scripts/air_quality.py alert-list --user telegram:8209218742
python scripts/air_quality.py alert-check --user telegram:8209218742
```

### 5) 아침 브리핑

```bash
python scripts/air_quality.py morning-brief 답십리동
python scripts/air_quality.py morning-brief --user telegram:8209218742
```

### 6) OpenClaw cron 초안 생성

```bash
python scripts/air_quality.py cron-plan morning-brief telegram:8209218742 --region 답십리동 --hour 7 --minute 30 --json
python scripts/air_quality.py cron-plan alert-check telegram:8209218742 --json
```

이 출력은 OpenClaw `cron add`에 넣기 쉬운 job 초안으로 쓰는 걸 전제로 한다.

### 7) provider 설정

```bash
python scripts/air_quality.py setup-provider airkorea --airkorea-api-key "YOUR_KEY" --json
python scripts/air_quality.py show-config --json
python scripts/air_quality.py now 답십리동 --provider airkorea
```

## AirKorea OpenAPI 키 발급 받기

AirKorea 실측값을 쓰려면 공공데이터포털에서 OpenAPI 활용신청 후 서비스키를 발급받아야 한다.

권장 순서:
1. 공공데이터포털(data.go.kr)에 로그인
2. AirKorea/대기질 관련 API 페이지로 이동
   - 실시간 대기질 조회 계열: `ArpltnInforInqireSvc`
   - 측정소 정보 계열: `MsrstnInfoInqireSvc`
3. 원하는 API에 대해 **활용신청** 진행
4. 승인 후 **일반 인증키**를 확인
   - Encoding / Decoding 중 하나를 사용할 수 있지만, 구현/환경에 따라 차이가 날 수 있으니 둘 다 확인해 두는 것을 권장
5. 아래처럼 스킬에 저장

```bash
python scripts/air_quality.py setup-provider airkorea --airkorea-api-key "발급받은서비스키" --json
```

확인:

```bash
python scripts/air_quality.py show-config --json
python scripts/air_quality.py now 답십리동 --provider airkorea
```

참고:
- 활용신청 직후에는 권한 반영이 바로 안 될 수 있다.
- `ArpltnInforInqireSvc` 와 `MsrstnInfoInqireSvc` 는 같은 에어코리아 계열이지만 서비스군이 다를 수 있어, 필요한 API별로 신청 상태를 확인하는 것이 안전하다.

## 지역 해석 예시

```bash
python scripts/air_quality.py resolve-region 답십리동 --json
python scripts/air_quality.py resolve-region 판교 --json
```

## OpenClaw 자동화 흐름

이 저장소는 단발 조회보다도 **OpenClaw 자동화**에 잘 맞는다.

예:
- `초미세먼지 나쁨 이상이면 알려줘`
  - `alert-add`로 규칙 저장
  - `cron-plan alert-check ...` 로 cron 초안 생성
  - OpenClaw cron에 연결해 주기 점검
- `매일 아침 7시 30분에 답십리동 브리핑`
  - `morning-brief`
  - `cron-plan morning-brief ...`
  - OpenClaw cron으로 매일 전달

## 로컬 상태 파일 정책

이 저장소는 로컬 상태를 `data/` 아래에 저장한다.

예:
- `data/user-preferences.json`
- `data/alert-rules.json`
- `data/alert-state.json`
- `data/station-cache.json`

이 파일들은 **사용자별 상태 / 캐시 / 알림 이력**이라서 기본적으로 `.gitignore` 대상이다.
즉, 저장소에는 스킬 코드와 문서 중심으로 남기고, 개인 상태는 로컬에 남기는 방식을 권장한다.

## 지금 남아 있는 큰 작업

1. AirKorea 실 API 키 기준 실측 응답 검증/미세 조정
2. 텔레그램 위치 공유 메시지에서 위경도 자동 흡수
3. OpenClaw cron 실제 등록을 상위 래퍼로 더 자동화
4. weather 스킬과 더 자연스럽게 결합한 생활형 브리핑 고도화
