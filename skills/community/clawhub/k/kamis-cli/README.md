# kamis-cli

CLI wrapper for the official **KAMIS** (한국농수산식품유통공사 / Korea Agro-Fisheries & Food Trade Corporation) OpenAPI — daily wholesale & retail prices for ~180 농수축산물 across 6 부류, with built-in 7-day, 1-month, 1-year, and 평년 comparisons.

> Endpoint: `https://www.kamis.or.kr/service/price/xml.do`

## Why
- **AI agents** asking about Korean food/produce prices, restaurant ingredient costs, agri inflation
- **Restaurants & buyers** doing daily 도매가 spot-checks
- **Inflation reporters** comparing wholesale vs CPI-Food
- **Content creators** writing about 김장 cost, 명절 시세, etc.

## Setup
1. Apply for a free API key at https://www.kamis.or.kr/customer/reference/openapi_list.do (1-day approval).
2. `export KAMIS_CERT_KEY="..."` and `export KAMIS_CERT_ID="..."`.

The TEST/TEST credentials work for `dailyPriceByCategoryList` (smoke-tests the flow); other endpoints need a real key.

## Quick start
```bash
# 오늘 채소류 도매가 한 번에
./scripts/daily.sh --cls 02 --category 200

# 양파(서울) 4월 한 달 도매가
./scripts/period.sh --start 2026-04-01 --end 2026-04-30 \
  --category 200 --item 211 --kind 01 --rank 04 --country 1101

# 쌀 최근 가격 동향
./scripts/recent.sh --product 111
```

See `SKILL.md` for the full subcommand reference and recipe library.

## Examples
- `examples/restaurant-cost-tracker.sh` — daily Markdown cost brief for chefs/buyers (8 staple items)
- `examples/cpi-vs-wholesale.sh` — overlay 양파 도매 trend with BOK ECOS CPI-Food (requires bank-of-korea-ecos-cli)

## Pairs with
- `opendart-cli` `bank-of-korea-ecos-cli` `kr-holiday-cli` `naver-datalab-cli` `kakao-local-cli`

MIT.
