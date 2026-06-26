---
name: OpenDART CLI
slug: opendart-cli
displayName: OpenDART CLI
version: 0.1.0
summary: 금융감독원 DART OpenAPI를 위한 한국어 CLI. 기업 고유번호 조회/캐시, 공시 목록 검색, 기업 개황, 주요 재무제표/전체 재무제표 조회, 대주주/임원 지분 조회 지원. 한국 핀테크·투자 에이전트 필수 도구.
tags: [latest, korea, finance, dart, opendart, disclosure, fintech, cli]
license: MIT
metadata:
  openclaw:
    requires:
      env: [OPENDART_API_KEY]
    primaryEnv: OPENDART_API_KEY
---

# OpenDART CLI

금융감독원 전자공시시스템(DART)의 공개 OpenAPI를 터미널에서 사용하기 위한 경량 Python CLI이다. 한국 상장·비상장 법인의 공시 이력, 기업 개황, 재무제표, 대주주·임원 지분 현황을 JSON으로 반환한다. 에이전트 파이프라인에 붙이기 쉽게 표준 출력(JSON)을 기본으로 하며, 한국어 오류 메시지와 캐시를 제공한다.

## 주요 기능 (v0.1.0)

- `corp-code`: 고유번호 XML 다운로드·파싱·캐시 (`~/.opendart-cli/corp_codes.json`)
- `find-corp`: 회사명 또는 종목코드로 corp_code 검색
- `list`: 공시 검색 (`bgn_de`, `end_de`, `pblntf_ty`, `corp_cls` 등 필터)
- `company`: 기업 개황
- `finance`: 주요계정(`fnlttSinglAcnt`) 또는 전체재무제표(`fnlttSinglAcntAll`) 조회
- `majorstock`: 대량보유자 현황
- `elestock`: 임원 지분 현황
- `document`: 공시서류 원본(ZIP) 저장

## 설치

```bash
pipx install opendart-cli      # 권장
# 또는
uv tool install opendart-cli
# 또는 (파이썬 3.9+)
pip install opendart-cli
```

개발 모드:

```bash
git clone https://github.com/ChloePark85/opendart-cli
cd opendart-cli
pipx install -e .
```

## 환경 변수

- `OPENDART_API_KEY` (필수): opendart.fss.or.kr 에서 발급받은 40자 인증키
- `OPENDART_CACHE_DIR` (선택): 캐시 디렉토리. 기본 `~/.opendart-cli`

## 빠른 사용 예시

```bash
# 1) API 키 발급 후 환경 변수 설정
export OPENDART_API_KEY="your_40_char_key"

# 2) 전체 고유번호 다운로드 및 캐시
opendart corp-code --refresh

# 3) 회사명으로 검색 (삼성전자 -> 00126380)
opendart find-corp "삼성전자"

# 4) 최근 30일 정기공시 목록
opendart list --corp-code 00126380 --pblntf-ty A --bgn 20260320 --end 20260420

# 5) 기업 개황
opendart company --corp-code 00126380

# 6) 단일회사 주요계정 (2025 사업연도 사업보고서)
opendart finance --corp-code 00126380 --bsns-year 2025 --reprt-code 11011

# 7) 전체 재무제표
opendart finance --corp-code 00126380 --bsns-year 2025 --reprt-code 11011 --all

# 8) 대주주/임원 지분
opendart majorstock --corp-code 00126380
opendart elestock  --corp-code 00126380

# 9) 공시서류 원본 ZIP 다운로드
opendart document --rcept-no 20260320000123 --out ./disclosure.zip
```

## 보고서 코드 참고 (`--reprt-code`)

- `11011` 사업보고서 (연간)
- `11012` 반기보고서
- `11013` 1분기 보고서
- `11014` 3분기 보고서

## 공시 유형 코드 (`--pblntf-ty`)

A 정기공시, B 주요사항보고, C 발행공시, D 지분공시, E 기타공시, F 외부감사관련, G 펀드공시, H 자산유동화, I 거래소공시, J 공정위공시.

## 보안

- 인증키는 환경 변수만 사용. CLI 인자/로그에 기록되지 않도록 처리.
- 응답은 HTTPS. 캐시는 사용자 홈 디렉토리 권한으로만 저장.

## 라이선스 & 출처

MIT 라이선스. 데이터는 금융감독원 전자공시시스템(DART)의 공식 OpenAPI 응답을 그대로 전달하며, 본 스킬은 DART의 비공식 클라이언트이다.

## 링크

- GitHub: https://github.com/ChloePark85/opendart-cli
- OpenDART: https://opendart.fss.or.kr
