# Integration Roadmap Status

## 이미 반영된 항목

- OpenClaw 스타일 README/SKILL 정리
- Open-Meteo 기반 실사용 프로토타입
- 지역명 alias 및 동/구 fallback 강화
- 기본 지역 저장
- 위치 좌표 인자(`--lat`, `--lon`) 반영
- 대기질 alert rule 저장/점검
- 중복 알림 방지 상태 저장
- 날씨 + 대기질 아침 브리핑
- OpenClaw cron 초안 생성
- provider 레이어(`openmeteo`, `airkorea`) 준비

## 이번 단계 목표

1. 사용자 기본 위치 좌표 저장/조회
2. 기본 provider 설정 저장
3. 기본 좌표를 지역 fallback보다 우선 사용하는 흐름 강화
4. 문서에 OpenClaw 자동화 흐름을 더 명확히 반영

## 다음 실제 확장 포인트

- AIRKOREA_API_KEY 설정 후 국내 API 매핑 구현
- 채팅 플랫폼 위치 공유 메시지를 OpenClaw 상위 레이어에서 `--lat/--lon` 으로 넘기기
- `cron-plan` 결과를 실제 `cron add` 호출로 자동 연결하는 상위 래퍼 추가
