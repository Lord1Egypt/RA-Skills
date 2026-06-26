# Alert and Morning Briefing

## Alert rule concept

대기질 감시는 지역 + 항목 + 임계 등급 조합으로 저장한다.

예시:

- 성동구 / pm2_5 / 나쁨 이상
- 서울 / pm10 / 매우나쁨 이상
- 분당 / overall / 나쁨 이상

## Rule storage

`data/alert-rules.json` 에 단순 JSON 배열로 저장한다.

권장 필드:

- id
- user
- region
- metric (`pm2_5`, `pm10`, `overall`)
- threshold (`좋음`, `보통`, `나쁨`, `매우나쁨`)
- created_at

## Morning briefing

아침 브리핑은 날씨 + 대기질을 합쳐 짧게 정리한다.

권장 순서:

1. 지역
2. 현재/오늘 기온 흐름
3. 하늘/강수 요약
4. PM2.5 / PM10 / 종합 판단
5. 외출 팁 한 줄

## OpenClaw usage

- 단발 조회: `now`, `morning-brief`
- 반복 알림: `alert-add` 후 OpenClaw cron으로 `alert-check`
- 알림 메시지는 새 rule hit만 전달하거나, 조건 충족 시마다 전달하는 정책을 나중에 선택할 수 있다.
