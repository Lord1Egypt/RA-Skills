# 가격 감시 JSON 포맷

이 스킬의 가격 감시 기능은 기본적으로 `skills/korea-domestic-flights/price-alert-rules.json` 파일을 사용한다.

OpenClaw cron/브리핑과 연결하기 쉽게 다음 원칙으로 설계한다.

- 파일 1개에 여러 감시 규칙을 저장한다.
- 각 규칙은 사람이 읽기 쉬운 `label` 과 안정적인 `id` 를 가진다.
- **동일 조건 중복 저장 방지**를 위해 `fingerprint` 를 저장한다.
- 마지막 점검 시각(`last_checked_at`)과 마지막 결과(`last_result`)를 함께 저장한다.
- **동일 최저가/동일 항공편 조건의 재알림 방지**를 위해 `notify.dedupe_key` 를 저장한다.
- **알림 문구 커스터마이즈**를 위해 `notify.message_template` 를 저장한다.
- 점검 스크립트는 목표가 충족 시 한국어 알림 메시지를 stdout 으로 출력하므로 cron/briefing 파이프에 바로 연결하기 쉽다.
- 향후 알림 채널 확장이 가능하도록 `notify` 필드를 남겨 둔다.

## 스키마 개요

```json
{
  "version": 2,
  "timezone": "Asia/Seoul",
  "updated_at": "2026-03-19T18:40:00+09:00",
  "rules": [
    {
      "id": "kdf-a1b2c3d4",
      "enabled": true,
      "label": "김포→제주,부산 주말 특가 감시",
      "fingerprint": "{...canonical json...}",
      "query": {
        "origin": "GMP",
        "destination": null,
        "destinations": ["CJU", "PUS"],
        "departure": null,
        "return_date": null,
        "date_range": {
          "start_date": "2026-03-21",
          "end_date": "2026-03-23"
        },
        "return_offset": 0,
        "adults": 1,
        "cabin": "ECONOMY",
        "trip_type": "one_way"
      },
      "target_price_krw": 70000,
      "created_at": "2026-03-19T18:35:00+09:00",
      "last_checked_at": "2026-03-19T18:39:12+09:00",
      "last_result": {
        "matched": false,
        "observed_price_krw": 81200,
        "best_option": {
          "destination": "CJU",
          "destination_label": "제주(CJU)",
          "departure_date": "2026-03-22",
          "price": 81200,
          "airline": "제주항공"
        },
        "search_type": "destination_date_matrix"
      },
      "notify": {
        "channel": "stdout",
        "dedupe_key": "{...canonical json...}",
        "last_sent_at": "2026-03-19T18:39:13+09:00",
        "message_template": "[특가] {label} {best_destination_label} {observed_price}"
      },
      "meta": {
        "source": "price_alerts.py",
        "notes": "아침 비행 우선"
      }
    }
  ]
}
```

## 필드 설명

- `version`: 저장 포맷 버전
- `timezone`: 날짜/시간 기준 타임존
- `updated_at`: 파일 마지막 갱신 시각
- `rules[]`: 감시 규칙 배열
- `rules[].id`: 안정적인 규칙 식별자
- `rules[].enabled`: 감시 활성 여부
- `rules[].label`: 사람이 읽는 규칙 이름
- `rules[].fingerprint`: 조건 중복 저장 방지용 canonical signature
- `rules[].query.origin`: IATA 코드 기준 저장
- `rules[].query.destination`: 단일 목적지용
- `rules[].query.destinations`: 다중 목적지용 배열
- `rules[].query.departure`, `return_date`: 단일 날짜 감시용
- `rules[].query.date_range`: 날짜 범위 감시용
- `rules[].query.return_offset`: 날짜 범위 왕복 감시에서 귀국일 오프셋
- `rules[].query.adults`, `cabin`: 검색 조건
- `rules[].target_price_krw`: 목표가
- `rules[].last_result`: 마지막 점검 결과 캐시
- `rules[].notify.channel`: 현재는 `stdout` 고정, 향후 확장 대비
- `rules[].notify.dedupe_key`: 최근 발송된 알림 fingerprint
- `rules[].notify.last_sent_at`: 마지막 알림 발송 시각
- `rules[].notify.message_template`: 사용자 정의 메시지 템플릿
- `rules[].meta.notes`: 사용자 메모

## 다중 목적지 감시 동작

- `destinations` 가 2개 이상이면 `price_alerts.py check` 가 자동으로 다중 목적지 검색 스크립트를 사용한다.
- 단일 날짜 감시는 `search_multi_destination.py`
- 날짜 범위 감시는 `search_destination_date_matrix.py`
- 알림은 **가장 저렴한 목적지/날짜 조합 1건** 기준으로 발생한다.

## 중복 방지 동작

### 1) 규칙 저장 단계 dedupe

동일한 검색 조건 + 목표가 조합으로 `add` 하면 새 규칙을 저장하지 않고 기존 규칙 ID 를 안내한다.

### 2) 알림 발송 단계 dedupe

`check` 중 목표가를 만족하더라도 다음 값이 같으면 같은 알림으로 간주하고 재출력하지 않는다.

- 규칙 ID
- 검색 타입
- 관측 최저가
- 최적 목적지
- 출발일/귀국일
- 항공사
- 출발/도착 시각

강제로 다시 출력하려면:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py check --no-dedupe
```

## 메시지 템플릿 변수

`add --message-template` 로 커스텀 알림 포맷을 저장할 수 있다.

자주 쓸 만한 변수:

- `{label}`
- `{route}`
- `{origin_label}`
- `{destinations_label}`
- `{best_destination_label}`
- `{target_price}` / `{target_price_krw}`
- `{observed_price}` / `{observed_price_krw}`
- `{difference_krw}`
- `{departure_date}` / `{return_date}`
- `{date_text}`
- `{airline}`
- `{departure_time}` / `{arrival_time}`
- `{cabin_label}`
- `{status_line}`

예시:

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py add \
  --origin 김포 \
  --destinations 제주,부산 \
  --date-range "내일부터 3일" \
  --target-price 80000 \
  --message-template "[특가감시] {best_destination_label} {departure_date} {observed_price} / 기준 {target_price}"
```

## 추천 cron 연결 방식

정기 점검에서 다음처럼 실행하면 된다.

```bash
python skills/korea-domestic-flights/scripts/price_alerts.py check
```

동작 방식:
- 목표가 미충족이면 `점검 완료: N개 규칙 확인, 목표가 충족 알림 없음` 출력
- 목표가 충족이면 규칙별 한국어 알림 메시지를 stdout 으로 출력
- 동일 알림은 `notify.dedupe_key` 기준으로 억제
- 일부 규칙 점검 오류가 있으면 stderr 에 오류를 남기고 JSON 저장 파일에는 `last_result.error` 를 기록

즉, 상위 OpenClaw 브리핑/cron 레이어에서는 stdout 을 메시지 본문으로 사용하고, stderr 또는 종료 코드를 장애 감지에 활용하면 된다.

## Windows 작업 스케줄러 초안

Windows 환경에서는 다음 스크립트 초안을 사용할 수 있다.

```powershell
powershell -ExecutionPolicy Bypass -File skills/korea-domestic-flights/scripts/register_price_alerts_task.ps1 -IntervalMinutes 30
```

주의:
- 이 스크립트는 **작업 등록만** 돕는다.
- 실제 알림 전송은 상위 OpenClaw cron/브리핑 파이프가 stdout 을 받아 전달하는 방식으로 연결해야 한다.
