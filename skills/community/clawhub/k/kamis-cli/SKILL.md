---
name: kamis-cli
description: Korean agricultural/livestock/aquatic wholesale & retail price data via the official KAMIS (한국농수산식품유통공사) OpenAPI. Use for daily 도매가/소매가 lookup, 7-day & monthly & yearly trends, regional price comparison, and code lookup. Free p_cert_key from kamis.or.kr. Use when the user asks about Korean food/produce prices, market prices, agri price trends, restaurant ingredient costs, KAMIS, 농산물 가격, or 도매시장.
license: MIT
---

# KAMIS CLI — 한국 농수산물 가격 OpenAPI

Wraps **KAMIS** (Korea Agro-Fisheries & Food Trade Corporation, [kamis.or.kr](https://www.kamis.or.kr)) — the canonical source for Korean agricultural, livestock, and aquatic product prices. Daily wholesale/retail prices for ~180 items across 10 부류, with built-in 1-day/1-week/2-week/1-month/1-year/평년 comparisons.

Endpoint: `https://www.kamis.or.kr/service/price/xml.do?action={ACTION}&p_cert_key={KEY}&p_cert_id={ID}&p_returntype=json&...`

## Setup (once)

1. Apply for an API key at https://www.kamis.or.kr/customer/reference/openapi_list.do (1-business-day approval, free).
2. Export credentials in your shell:

```bash
export KAMIS_CERT_KEY="your-key"
export KAMIS_CERT_ID="your-email-id"
```

The CLI also accepts `--key` / `--id` flags. If unset, it falls back to `TEST`/`TEST` which works for `dailyPriceByCategoryList` (the most common call) but is rate-limited and may return `error_code:001` for paid endpoints.

## Subcommands

All subcommands return JSON to stdout. Pipe through `jq` for shaping.

### 1. `daily.sh` — 일일 부류별 도/소매가격 (`dailyPriceByCategoryList`)

The flagship endpoint. One call returns every item in a 부류 (category) with **today / 1 day ago / 1 week ago / 2 weeks ago / 1 month ago / 1 year ago / 평년** prices side-by-side. Perfect for AI agents asking "what's happening with onion prices this week?"

```bash
scripts/daily.sh --cls 01 --category 200 --date 2026-04-30
# 01 = 소매(retail), 02 = 도매(wholesale)
# category: 100=식량작물, 200=채소류, 300=특용작물, 400=과일류, 500=축산물, 600=수산물
# Optional: --country 1101 (서울), --kg-convert Y
```

### 2. `period.sh` — 기간별 도매가격 (`periodProductList`)

Daily prices for a specific item across a date range (≤ 1 year). Returns one row per market per day.

```bash
scripts/period.sh \
  --start 2026-01-01 --end 2026-04-30 \
  --category 200 --item 211 --kind 01 --rank 04 --country 1101
# 211 = 양파, 01 = 일반양파, 04 = 상품, 1101 = 서울
```

### 3. `period-retail.sh` — 기간별 소매가격 (`periodRetailProductList`)

Same shape as `period.sh` but soft-retail (대형마트/전통시장) instead of 도매. Use when comparing 소매 마진.

```bash
scripts/period-retail.sh --start 2026-04-01 --end 2026-04-30 --category 200 --item 211 --kind 01 --rank 04 --country 1101
```

### 4. `monthly.sh` — 월별 평균 가격 (`monthlySalesList`)

Long-term monthly averages — use for seasonality charts, YoY comparison.

```bash
scripts/monthly.sh --year 2026 --period 2024,2025 --category 200 --item 211 --kind 01
```

### 5. `yearly.sh` — 연도별 평균 가격 (`yearlySalesList`)

Annual averages.

```bash
scripts/yearly.sh --year 2026 --category 200 --item 211 --kind 01
```

### 6. `recent.sh` — 최근 가격 동향 간이조회 (`recentlyPriceTrendList`)

Lightweight time-series for a single product number — last 40 days, 30 days, 20 days, 10 days, 0 days, plus min/max. Useful for fast charts without fetching the full period dataset.

```bash
scripts/recent.sh --product 111
# 111 = 쌀
```

### 7. `codes.sh` — 코드 표 (helper, no API call)

Local lookup of category / item / kind / rank / country codes. Wraps `reference/codes.json` — the canonical KAMIS code table cached at skill install.

```bash
scripts/codes.sh categories
scripts/codes.sh items --category 200
scripts/codes.sh countries          # 17 시·군 codes
scripts/codes.sh ranks
```

## Quick recipes

**"How much have onion prices moved this week?"**
```bash
scripts/daily.sh --cls 01 --category 200 | jq '.data.item[] | select(.item_name=="양파")'
```

**"Plot 1-year retail price for rice"**
```bash
scripts/period.sh --start 2025-05-01 --end 2026-04-30 --category 100 --item 111 --kind 01 --rank 04 --country 1101 | jq '.data.item[] | {date: .yyyy + "-" + .regday, price: .price}'
```

**"Daily morning brief: top 5 climbers in 채소류"**
```bash
scripts/daily.sh --cls 02 --category 200 \
  | jq '[.data.item[] | {name: .item_name, kind: .kind_name, today: (.dpr1|gsub(",";"")|tonumber), week_ago: (.dpr3|gsub(",";"")|tonumber)} | .pct = ((.today - .week_ago) / .week_ago * 100)] | sort_by(-.pct) | .[0:5]'
```

See `examples/restaurant-cost-tracker.sh` for a full pipeline that emits a daily Slack/Telegram-ready summary.

## Pairs naturally with

- **`opendart-cli`** — overlay 식료품 corporate disclosure with raw input prices.
- **`bank-of-korea-ecos-cli`** — compare CPI-Food vs raw 농산물 도매가.
- **`kr-holiday-cli`** — exclude 명절 demand spikes from trend lines.
- **`naver-datalab-cli`** — correlate 검색량 (e.g., "양파 가격") with the price spike.
- **`kakao-local-cli`** — map 도매시장 locations.
- **`tistory-api-cli` / `velog-cli`** — auto-publish a daily-price digest.

## Notes & gotchas

- The TEST key works for `dailyPriceByCategoryList` (immediate snapshot) but several "기간" endpoints return `error_code:"001"` until you swap in your own key.
- KAMIS only retains 1 year of recent data through the public API. For older data, contact KAMIS directly (061-930-9971).
- `p_returntype=json` is supported but the API still ships an `xml.do` path — that's the actual route, not a typo.
- Numbers come as comma-formatted strings (`"62,421"`) — strip with `jq 'gsub(","; "") | tonumber'` before arithmetic.
- A few endpoints inconsistently use `p_country_code` vs `p_countycode` — the scripts normalize this for you.
