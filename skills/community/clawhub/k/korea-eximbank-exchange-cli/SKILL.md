---
name: Korea Eximbank Exchange CLI
slug: korea-eximbank-exchange-cli
version: 0.1.0
description: Korea Eximbank (한국수출입은행) OpenAPI 환율(AP01/AP02/AP12) 조회 CLI — 날짜/통화 필터, JSON/CSV 출력 지원
homepage: https://github.com/ChloePark85/korea-eximbank-exchange-cli
license: MIT
authors:
  - name: Chloe Park
    url: https://github.com/ChloePark85
repository:
  type: git
  url: https://github.com/ChloePark85/korea-eximbank-exchange-cli.git
metadata:
  openclaw:
    requires:
      env:
        - KOREAEXIM_API_KEY
    primaryEnv: KOREAEXIM_API_KEY
    tags:
      - latest
categories:
  - Data & APIs
  - Finance
---

# Korea Eximbank Exchange CLI

Korea Eximbank (한국수출입은행) OpenAPI 기반 환율 조회 CLI이다. 지정한 날짜의 KRW 기준 환율표(AP01/일반고시환율 등)를 JSON/CSV로 출력한다.

- 공식 API: https://www.koreaexim.go.kr/site/program/financial/exchangeJSON
- 인증키: 환경변수 `KOREAEXIM_API_KEY` 사용

## 설치

```bash
pip install -e .
```

## 사용법

```bash
export KOREAEXIM_API_KEY="<발급키>"
eximbank-exchange --date 2024-12-31 --table AP01 --format json | jq '.'
```

옵션:
- `--date YYYY-MM-DD` 또는 `YYYYMMDD` (기본: 오늘, KST)
- `--table AP01|AP02|AP12` (기본: AP01)
- `--format json|csv` (기본: json)
- `--filter <CURRENCY>` 특정 통화만 필터 (예: USD, JPY)

## 예시

```bash
eximbank-exchange --date 2025-01-02 --table AP01 --filter USD --format csv
```

## 주의사항
- 영업일이 아닌 경우 API는 빈 배열([])을 반환할 수 있다.
- 요청 제한이 있을 수 있으며, 오류 시 API의 `msg` 필드를 확인하라.
