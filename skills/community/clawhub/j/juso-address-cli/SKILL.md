---
name: juso-address-cli
description: Search and resolve Korean road addresses (도로명주소) via the official juso.go.kr OpenAPI. Keyword search with zip codes, English address lookup, and address-to-coordinate conversion. Use when a task needs a form-ready Korean address with 우편번호, 영문주소, or lat/lng for a specific address string — e.g. checkout forms, shipping, invoicing, 사업자 등록 forms, real-estate intake. Prefer this over Kakao/Naver geocoders when the requirement is a government-validated road address rather than a map pin.
version: 0.1.0
license: MIT
---

# juso-address-cli

Minimal command-line wrapper for the **행정안전부 주소기반산업지원서비스** (juso.go.kr) OpenAPI.

Three operations:
1. `search` — keyword search for 도로명주소 / 지번주소 with 우편번호 (KR).
2. `eng` — English road-address search (for non-Korean-speaking users).
3. `coord` — address → WGS84-ish 좌표 (entrance-coordinate API, grade-B key required).

All output is compact JSON, one object per line (JSONL) for easy piping into `jq` or agent post-processing.

## When to use this skill

Use when the task is **Korean-address-shaped**:
- "Find the full 도로명주소 and 우편번호 for 강남대로 123"
- "Normalize this user-entered address against the government registry"
- "Give me the 영문주소 for 서울특별시 종로구 세종대로 209"
- "Get the entrance lat/lng of this address so I can drop a pin"

Do **not** use this skill to:
- Do a free-form *place* search (use `kakao-local-cli` keyword search instead).
- Reverse-geocode coordinates (juso.go.kr does not publish a reverse endpoint — use `kakao-local-cli coord2addr`).

## Prerequisites

1. Request a **확인키 (confmKey)** at <https://business.juso.go.kr/addrlink/openApi/apiExprn.do>. Grade-A (개발용) is granted instantly; grade-B (운영용) is granted within 1–2 business days and is required for `coord`.
2. Export the key:
   ```bash
   export JUSO_CONFM_KEY="devU01TX0FVVEgyMDI1..."     # for search/eng
   export JUSO_CONFM_KEY_COORD="U01TX0FVVEgyMDI1..."  # grade-B, for coord
   ```
3. Dependencies: `bash`, `curl`, `jq`, `python3` (all default on macOS/Linux).

## Commands

```bash
# 1) Keyword search (도로명 or 지번)
scripts/search.sh "강남대로 123"
scripts/search.sh "세종대로 209" --per-page 20 --page 1 --history Y

# 2) English address search
scripts/eng.sh "Sejongdae-ro 209"

# 3) Address → entrance coordinates (grade-B key required)
scripts/coord.sh --admcode 1111000000 \
  --rnmgmcd 111104166021 --udrtyn 0 \
  --buldmnnm 209 --buldslno 0

# Helper: resolve a raw address string to coordinates in one call.
# Internally: search → pick first result → coord.
scripts/resolve.sh "서울특별시 종로구 세종대로 209"
```

Every script prints one JSON object per line on stdout; errors go to stderr with a non-zero exit code.

## Example JSONL output

```jsonl
{"roadAddr":"서울특별시 종로구 세종대로 209","jibunAddr":"서울특별시 종로구 세종로 55-1 정부서울청사","zipNo":"03171","bdNm":"정부서울청사","siNm":"서울특별시","sggNm":"종로구","emdNm":"세종로","rn":"세종대로","buldMnnm":"209","buldSlno":"0","admCd":"1111051500","rnMgtSn":"111104166021","bdMgtSn":"1111010100100550001000001","udrtYn":"0"}
```

## Rate limits

- juso.go.kr caps free keys at **10 requests/sec** and **30,000 requests/day** per key (grade-A) / **100,000/day** (grade-B). The scripts **do not** retry on 429 — back off in the caller.

## Notes for agents

- Always pipe `search.sh` through `jq -s '.[0]'` (or `head -n1`) when you only need the best match.
- `resolve.sh` is the one-shot convenience: it silently picks the first `search` hit and then hits `coord`, so it requires both keys. Fail back to `search.sh` alone when `JUSO_CONFM_KEY_COORD` is absent.
- The 우편번호 (`zipNo`) returned here is the **5-digit 기초구역번호** (post-2015), not the legacy 6-digit code.
- Input may mix 도로명 and 지번; juso.go.kr accepts both and returns a normalized `roadAddr`.
- English search requires the street stem in Revised Romanization (e.g. "Sejongdae-ro", not "Sejong-daero").

## Reference

- Official API docs: <https://business.juso.go.kr/addrlink/openApi/apiExprn.do>
- Error-code list: <https://business.juso.go.kr/addrlink/devCenterEventBoard/devBoardList.do?cPath=99MD>
- License: MIT (this CLI wrapper). The underlying data is public under 공공데이터 이용 약관.
