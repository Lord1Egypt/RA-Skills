# naver-news-briefing

네이버 Search API 기반으로 **뉴스 검색 / 브리핑 / 지속 감시 / 키워드 그룹 / 자동화 계획 생성**을 수행하는 OpenClaw 스킬입니다.

> [!IMPORTANT]
> 이 스킬은 **네이버 개발자센터에서 발급받은 Search API 자격증명(client_id, client_secret)이 있어야만 정상 동작**합니다.
> 설치만으로 바로 검색되지는 않으며, **최초 1회 자격증명 입력(onboarding/setup)** 을 반드시 거쳐야 합니다.

이 스킬의 핵심은 단순 검색이 아니라 **채팅형 한국어 요청을 실제 운영 가능한 로컬 설정으로 연결**하는 데 있습니다.
즉, 사람이 이렇게 말하면:

- `반도체 뉴스 1시간마다 모니터링해줘`
- `매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘`
- `증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘`

이 스킬은 이를 **정규화된 질의 + 저장 가능한 watch/group 설정 + cron 연결 힌트 + 추천 실행 명령**으로 바꿉니다.

## 설치 / 링크

- GitHub: <https://github.com/twbeatles/openclaw-naver-news-briefing>
- ClawHub 홈: <https://clawhub.com>
- 설치 명령: `clawhub install naver-news-briefing`

## 대표 예시 요청 모음

- `최근 3일 반도체 뉴스 브리핑해줘`
- `반도체 뉴스 1시간마다 모니터링해줘`
- `매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘`
- `증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘`
- `환율이랑 2차전지 뉴스 묶어서 아침 브리핑용 그룹 만들어줘`

---

## 핵심 기능

- 한국어 자연어 뉴스 검색
- `-제외어` 필터링
- 최근 기간 해석
  - `오늘`, `최근 3일`, `최근 2주`, `한달`, `이번주`, `지난주`
- 문장형 한국어 요청 정규화
- 원샷 브리핑
- watch rule 저장 / 목록 / 삭제 / 신규 기사 체크
- 키워드 그룹 저장 / 수정 / 삭제
- 멀티 브리핑 템플릿
  - `concise`
  - `analyst`
  - `morning-briefing`
  - `watch-alert`
- 자연어 자동화 계획 파싱
  - `interval / daily / weekly / manual`
  - 일정 설명 + cron 힌트 + 추천 템플릿 + 추천 저장 대상
- `plan-save`로 watch/group 저장
- **저장 시 운영 메타데이터까지 같이 보존**
  - label
  - tags
  - template
  - schedule
  - operator_hints
- 기본 텍스트 출력 + `--json` 구조화 출력

---

## 빠른 시작

### 0) 먼저 준비할 것

이 스킬을 처음 쓰는 사용자는 먼저 아래를 준비해야 합니다.

- 네이버 개발자센터에서 발급받은 `client_id`
- 네이버 개발자센터에서 발급받은 `client_secret`

자격증명이 없으면 `search`, `watch-add`, `watch-check`, `brief-multi`, `plan-save` 같은 실제 운영 명령은 정상적으로 끝까지 진행되지 않습니다.

### 1) 최초 온보딩: 자격증명 저장

명령줄 인자를 한 번에 넣는 방식:

```bash
python scripts/naver_news_briefing.py setup --client-id YOUR_ID --client-secret YOUR_SECRET
python scripts/naver_news_briefing.py check-credentials --json
```

더 사용자 친화적인 대화형 방식:

```bash
python scripts/naver_news_briefing.py setup
```

위처럼 `setup`만 실행하면 CLI가 `client_id`, `client_secret`를 순서대로 물어봅니다.
특히 `client_secret`는 화면에 그대로 보이지 않도록 입력됩니다.

저장 직후 실제 API까지 바로 확인하고 싶다면:

```bash
python scripts/naver_news_briefing.py setup --live-check
python scripts/naver_news_briefing.py setup --test-search "최근 1일 반도체 뉴스"
```

설명:

- `setup`은 최초 1회 실행하는 온보딩 명령입니다.
- 입력값에 공백/줄바꿈이 섞였거나 지나치게 짧으면 저장 전에 먼저 알려줍니다.
- 자격증명은 `data/config.json`에 저장됩니다.
- Windows에서는 가능하면 DPAPI 기반으로 `client_secret`를 보호합니다.
- `check-credentials --json`으로 첫 입력이 제대로 끝났는지 바로 검증하세요.
- 일반 텍스트 확인용으로는 `python scripts/naver_news_briefing.py check-credentials` 도 사용할 수 있습니다.
- 실제 API까지 확인하려면 `python scripts/naver_news_briefing.py check-credentials --live-check` 를 사용할 수 있습니다.

### 2) 원샷 브리핑

```bash
python scripts/naver_news_briefing.py search "최근 3일 반도체 뉴스 브리핑 -광고"
```

### 3) 자연어 자동화 계획 확인

```bash
python scripts/naver_news_briefing.py plan "반도체 뉴스 1시간마다 모니터링해줘"
python scripts/naver_news_briefing.py plan "매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘" --json
python scripts/naver_news_briefing.py plan "증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘"
```

### 4) OpenClaw/cron 연동 번들 생성

```bash
python scripts/naver_news_briefing.py integration-plan "반도체 뉴스 1시간마다 모니터링해줘"
python scripts/naver_news_briefing.py integration-plan "매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘" --json
python scripts/naver_news_briefing.py integration-plan "반도체 뉴스 1시간마다 모니터링해줘" --output data/semiconductor-hourly-bundle.json --json
```

이 명령은 한 번에 아래를 만듭니다.

- 해석된 자동화 계획
- 실제 저장 명령 (`plan-save`)
- 반복 실행 명령 (`watch-check` 또는 `brief-multi`)
- cron 한 줄 예시
- OpenClaw cron/systemEvent에 붙이기 좋은 텍스트
- 사용자 확인용 짧은 한국어 문구

### 5) 계획을 실제 설정으로 저장

watch로 저장:

```bash
python scripts/naver_news_briefing.py plan-save "반도체 뉴스 1시간마다 모니터링해줘" --as watch --name semiconductor-hourly
```

group으로 저장:

```bash
python scripts/naver_news_briefing.py plan-save \
  "매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘" \
  --as group \
  --name morning-tech \
  --label "아침 브리핑" \
  --tag 테크 \
  --tag 시장
```

---

## 한국어 요청이 어떻게 해석되는가

### 예시 1) `반도체 뉴스 1시간마다 모니터링해줘`

해석 포인트:

- 작업 유형: `monitor`
- 저장 대상 추천: `watch`
- 주제 질의: `반도체`
- 일정: `1시간마다`
- 템플릿: `watch-alert`
- 후속 실행 추천: `watch-check <name> --json`

권장 운영:

1. `plan`으로 해석 확인
2. `plan-save --as watch`
3. 외부 스케줄러에서 `watch-check`를 1시간마다 실행
4. 신규 기사만 메신저로 전달

### 예시 2) `매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘`

해석 포인트:

- 작업 유형: `briefing`
- 저장 대상 추천: `group`
- 주제 질의: `반도체`, `AI 데이터센터`
- 일정: `매일 07:00`
- 템플릿: `morning-briefing`
- 후속 실행 추천: `brief-multi --group <name> --template morning-briefing`

권장 운영:

1. `plan`으로 schedule / grouping 확인
2. `plan-save --as group`
3. 외부 스케줄러에서 `brief-multi`를 07:00에 실행
4. stdout 텍스트를 텔레그램/디스코드/노션 등으로 전달

### 예시 3) `증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘`

해석 포인트:

- 작업 유형: `monitor`
- 주제 질의: `삼성전자 -증권사 -리포트`
- 일정: `15분마다`로 보수적으로 해석
- 템플릿: `watch-alert`
- 제외어 유지: `증권사`, `리포트`

이 패턴은 실무에서 꽤 중요합니다. “말고 / 빼고 / 제외”가 자동으로 `-제외어`로 정규화되므로, 채팅형 요청을 곧바로 watch로 저장하기 쉽습니다.

---

## CLI 개요

### search

```bash
python scripts/naver_news_briefing.py search "최근 3일 반도체 뉴스 브리핑 -광고"
python scripts/naver_news_briefing.py search "AI 데이터센터 뉴스" --json
```

### watch

```bash
python scripts/naver_news_briefing.py watch-add semiconductor "최근 7일 반도체 -광고"
python scripts/naver_news_briefing.py watch-add samsung-watch "삼성전자 -증권사 -리포트" --label "삼성전자 감시" --tag watch --tag 삼성 --template watch-alert
python scripts/naver_news_briefing.py watch-list
python scripts/naver_news_briefing.py watch-check semiconductor --json
python scripts/naver_news_briefing.py watch-remove semiconductor
```

### group

```bash
python scripts/naver_news_briefing.py group-add market-watch "최근 3일 반도체 -광고" "오늘 AI 데이터센터 -주가" --label "시장 체크" --tag 테크 --template morning-briefing
python scripts/naver_news_briefing.py group-list
python scripts/naver_news_briefing.py group-update market-watch --add-query "배터리 공급망 -광고" --tag 테크 --tag 공급망 --template analyst
python scripts/naver_news_briefing.py group-remove market-watch
```

### brief-multi

```bash
python scripts/naver_news_briefing.py brief-multi --group market-watch --template concise
python scripts/naver_news_briefing.py brief-multi --group market-watch --query "환율 뉴스" --template morning-briefing --json
```

참고:

- `--template`를 주지 않으면 group에 저장된 template를 우선 사용합니다.
- 운영자가 template를 group 단위로 고정해 두면 cron 명령이 짧아집니다.

### plan / integration-plan / plan-save

```bash
python scripts/naver_news_briefing.py plan "반도체 뉴스 1시간마다 모니터링해줘"
python scripts/naver_news_briefing.py integration-plan "매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘" --json
python scripts/naver_news_briefing.py plan-save "증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘" --as watch --name samsung-watch
```

`integration-plan`은 `plan`보다 한 단계 더 나가서 **실행 가능한 연동 번들**을 만듭니다.

대표 필드:

- `storage.save_command`: 상태 저장용 `plan-save` 명령
- `runner.command`: 반복 실행용 핵심 명령
- `automation.schedule`: 스케줄 객체
- `automation.cron_line`: 바로 복사 가능한 cron 한 줄
- `automation.system_event_text`: OpenClaw systemEvent 초안
- `automation.openclaw_prompt`: 작업 생성기에 넘기기 좋은 요약 프롬프트
- `assistant_summary.confirmation`: 사용자에게 확인받기 좋은 짧은 문장

`plan` 출력에는 보통 다음이 들어갑니다.

- 작업 유형: `monitor / briefing / monitor+briefing`
- 해석된 질의 목록
- 일정 종류: `interval / daily / weekly / manual`
- cron 힌트
- 추천 저장 대상: `watch / group`
- 추천 템플릿
- operator hints
  - 추천 실행 명령
  - 추천 전달 포맷
  - cron 예시
- 추천 후속 명령

`plan-save`는 여기에 더해 **실제 DB에 저장되는 watch/group 객체에도 template / schedule / operator_hints / tags / context를 같이 남깁니다.**

---

## 추천 운영 패턴

### 패턴 1) 새 기사 감시형

요청:

- `반도체 뉴스 1시간마다 모니터링해줘`

추천 흐름:

```bash
python scripts/naver_news_briefing.py plan "반도체 뉴스 1시간마다 모니터링해줘"
python scripts/naver_news_briefing.py plan-save "반도체 뉴스 1시간마다 모니터링해줘" --as watch --name semiconductor-hourly
python scripts/naver_news_briefing.py watch-check semiconductor-hourly --json
```

이 방식은 **신규 기사 JSON을 메신저/웹훅 레이어로 넘기기 좋다**는 장점이 있습니다.

### 패턴 2) 아침 브리핑형

요청:

- `매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘`

추천 흐름:

```bash
python scripts/naver_news_briefing.py plan-save \
  "매일 아침 7시에 반도체랑 AI 데이터센터 뉴스 브리핑해줘" \
  --as group --name morning-tech --label "아침 브리핑"

python scripts/naver_news_briefing.py brief-multi --group morning-tech
```

이 패턴은 **group에 template를 저장해 두고 cron에서는 group 이름만 호출**하는 방식이 편합니다.

### 패턴 3) 필터 강한 실무형 감시

요청:

- `증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘`

추천 흐름:

```bash
python scripts/naver_news_briefing.py plan "증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘"
python scripts/naver_news_briefing.py plan-save "증권사 리포트 빼고 삼성전자 뉴스 계속 체크해줘" --as watch --name samsung-watch
python scripts/naver_news_briefing.py watch-check samsung-watch --json
```

---

## 온보딩 / 최초 사용 가이드

처음 설치한 사용자는 아래 순서로 시작하면 됩니다.

1. 네이버 Search API 자격증명(`client_id`, `client_secret`)을 준비합니다.
2. `setup` 명령으로 최초 입력을 완료합니다.
3. `check-credentials --json`으로 유효성을 확인합니다.
4. 그 다음에만 `search` 또는 `plan`/`plan-save` 흐름으로 넘어갑니다.

가장 안전한 첫 실행 순서:

```bash
python scripts/naver_news_briefing.py setup --live-check
python scripts/naver_news_briefing.py check-credentials --live-check
python scripts/naver_news_briefing.py search "최근 3일 반도체 뉴스 브리핑"
```

자동화 스크립트나 CI에서는 아래처럼 인자를 직접 넣는 방식도 계속 지원합니다.

```bash
python scripts/naver_news_briefing.py setup --client-id YOUR_ID --client-secret YOUR_SECRET
python scripts/naver_news_briefing.py check-credentials --json
```

만약 자격증명이 설정되지 않았다면, 다른 명령을 먼저 시도하기보다 **다시 온보딩(setup)부터 안내하는 쪽이 맞습니다.**

### 자주 보는 초기 오류

자격증명 없이 바로 `search`나 `watch-check`를 실행하면, 이제 CLI는 단순한 실패 문구 대신 아래 방향으로 안내합니다.

- 네이버 Search API 자격증명이 아직 설정되지 않았다는 점
- 먼저 `setup`을 실행해야 한다는 점
- 이어서 `check-credentials --json`으로 검증하라는 점
- 그 다음에 실제 검색/브리핑 명령으로 넘어가라는 점

즉, **초기 사용자에게는 에러보다 온보딩 안내가 먼저 보이도록** 맞춰 두었습니다.

### 추천 health check 흐름

실제 API가 정상 응답하는지까지 보고 싶다면 아래 흐름이 가장 직관적입니다.

```bash
python scripts/naver_news_briefing.py setup --live-check
python scripts/naver_news_briefing.py check-credentials --live-check
```

원하는 테스트 질의가 있다면:

```bash
python scripts/naver_news_briefing.py setup --test-search "삼성전자 뉴스"
python scripts/naver_news_briefing.py check-credentials --live-check --query "삼성전자 뉴스"
```

## 운영자 가이드

### 1) watch와 group을 구분해서 쓰기

- **watch**: 단일 관심 주제를 새 기사 기준으로 계속 체크할 때
- **group**: 여러 주제를 묶어 반복 브리핑할 때

이 둘을 섞지 말고 역할을 분리하면 운영이 단순해집니다.

### 2) 스케줄은 외부에서, 상태는 이 스킬에서

이 스킬은 다음을 담당합니다.

- 질의 정규화
- 상태 저장
- dedupe
- 브리핑 렌더링
- 일정 의도 해석
- operator-friendly plan 출력

정확한 실행 시각은 아래 같은 외부 레이어에서 붙이세요.

- OpenClaw cron
- Windows 작업 스케줄러
- GitHub Actions
- 별도 Python worker
- PM2 / systemd timer / crontab

### 3) cron 연결 힌트

예를 들어 `plan` 출력이 아래를 주면:

- cron 힌트: `0 7 * * *`
- 추천 실행 명령: `python scripts/naver_news_briefing.py brief-multi --group morning-tech --template morning-briefing`

운영자는 이를 거의 그대로 옮길 수 있습니다.

예시:

```cron
0 7 * * * cd /path/to/workspace/skills/naver-news-briefing && python scripts/naver_news_briefing.py brief-multi --group morning-tech --template morning-briefing
```

watch 예시:

```cron
0 * * * * cd /path/to/workspace/skills/naver-news-briefing && python scripts/naver_news_briefing.py watch-check semiconductor-hourly --json
```

### 4) 저장 메타데이터를 같이 남기는 이유

`plan-save`는 단순히 검색어만 저장하지 않습니다.
아래 메타데이터를 같이 남겨 두면 운영자가 나중에 훨씬 덜 헷갈립니다.

- `label`: 사람이 읽는 용도
- `tags`: 분류 / 운영 필터링
- `template`: 출력 형식 기본값
- `schedule`: 어떤 cadence로 설계됐는지
- `operator_hints`: 추천 실행 명령 / 전달 방식 / cron 예시
- `context`: 원래 사용자의 요청 문장

### 5) 가장 안정적인 질의 형식

자연어도 되지만 아래 구조가 가장 예측 가능하게 동작합니다.

- 기간 표현 + 핵심 키워드 + 제외어

예:

- `최근 7일 반도체 공급망 -광고 -주가`
- `오늘 AI 데이터센터 -리포트`

### 6) dedupe 동작

`watch-check`는 `(watch_id, link)` 기준으로 신규 여부를 판정합니다.
같은 기사 링크는 반복 실행해도 다시 알리지 않습니다.

---

## 저장 파일

- `data/config.json`: API 자격증명 및 기본 설정
- `data/watch_state.db`: watch / group / seen-link 상태
- `references/upstream-notes.md`: upstream 설계 메모

---

## 테스트

```bash
python -m pytest scripts/tests -q
```

---

## 한계

- 기사 본문 크롤링/본문 요약은 하지 않습니다.
- 네이버 Search API의 제목 / 요약 / 링크 / 발행시각 메타데이터 기반으로 동작합니다.
- 자연어 일정 파서는 실무형 요청 위주입니다.
- 주제 없이 `매일 아침 7시에 브리핑해줘`처럼 일정만 있는 요청은 계획은 일부 만들 수 있어도 저장 가능한 watch/group으로는 제한될 수 있습니다.
