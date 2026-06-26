# juso-address-cli

Command-line wrapper for the **행정안전부 주소기반산업지원서비스** ([juso.go.kr](https://business.juso.go.kr)) OpenAPI — search and resolve Korean road addresses (도로명주소) from the terminal or an AI agent.

## Why

Every Korean web form, checkout, shipping-label pipeline, invoice, or 사업자 등록 flow needs a **government-validated** road address with a 5-digit 우편번호. Kakao / Naver geocoders are great for map pins but return place data, not form-ready registry addresses. This CLI talks to the official source.

## What you get

- `search.sh` — keyword search (도로명/지번) returning normalized `roadAddr`, `jibunAddr`, `zipNo`, 건물관리번호 etc.
- `eng.sh` — English road-address search.
- `coord.sh` — entrance lat/lng for a resolved address (grade-B 확인키 필요).
- `resolve.sh` — one-shot: raw string → best match → coords.

Output is JSONL — one object per line — so it plays nicely with `jq`, `fx`, or an LLM tool-call.

## Setup

1. Grab a 확인키 at <https://business.juso.go.kr/addrlink/openApi/apiExprn.do>.
2. `export JUSO_CONFM_KEY=...` (and optionally `JUSO_CONFM_KEY_COORD=...` for coordinates).
3. Make scripts executable:
   ```bash
   chmod +x scripts/*.sh
   ```

## Example

```bash
./scripts/search.sh "세종대로 209" --per-page 3 | jq .
./scripts/eng.sh "Sejongdae-ro 209"
./scripts/resolve.sh "서울특별시 종로구 세종대로 209"
```

## Install as a skill

```bash
clawhub install juso-address-cli
```

Or clone this repo into any skills directory — the `SKILL.md` tells agent harnesses how to invoke the scripts.

## License

MIT for the wrapper. The underlying juso.go.kr data is published under 공공데이터 이용 약관.
