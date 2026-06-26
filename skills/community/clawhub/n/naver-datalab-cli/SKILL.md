---
name: naver-datalab-cli
description: Korean search-keyword and shopping-trend analytics via the official NAVER DataLab API (openapi.naver.com/v1/datalab/*). Six subcommands wrapping 통합 검색어 트렌드 and 쇼핑인사이트 (분야별, 분야 내 키워드, 디바이스/성별/연령대 분포). Use when researching Korean consumer demand, planning SEO/content for the naver.com search market, comparing keyword popularity over time, building K-pop / K-beauty / K-commerce trend dashboards, or filling the gap that Google Trends leaves on Korean queries. Pairs with naver-papago-translate (translate insights), tistory-api-cli / velog-cli (publish trend posts), and kr-holiday-cli (align campaigns with KR calendar). Free tier (1k req/day for shopping insights, 25k req/day for search trends).
version: 0.1.0
license: MIT
---

# naver-datalab-cli

Command-line wrapper for the **NAVER DataLab Open API** — Korea's primary search-keyword and shopping-insight trend service. The Korean equivalent of Google Trends, with two key advantages on KR-market analysis:

1. **NAVER drives ~55% of Korean search traffic** (vs ~35% Google), so its trends are closer to real Korean demand.
2. **쇼핑인사이트** exposes shopping-cart-level trends across 50+ category trees with breakdown by device / age / gender — Google Trends cannot do this.

Six subcommands, one per official endpoint:

| Command | Endpoint | Purpose |
|---|---|---|
| `scripts/search.sh`        | `/v1/datalab/search`                          | 통합 검색어 트렌드 — compare up to 5 keyword groups (each with up to 20 synonyms) over time. |
| `scripts/shop-cat.sh`      | `/v1/datalab/shopping/categories`             | 쇼핑인사이트 분야별 트렌드 — compare shopping-category click volumes. |
| `scripts/shop-keyword.sh`  | `/v1/datalab/shopping/category/keywords`      | 분야 내 키워드 트렌드 — within one category, compare keyword interest. |
| `scripts/shop-device.sh`   | `/v1/datalab/shopping/category/device`        | Device split (pc / mo) for one category. |
| `scripts/shop-gender.sh`   | `/v1/datalab/shopping/category/gender`        | Gender split (f / m) for one category. |
| `scripts/shop-age.sh`      | `/v1/datalab/shopping/category/age`           | Age split (10/20/30/40/50/60) for one category. |

All output is JSONL (one row per period per group) so it pipes directly into `jq`, `csvkit`, `pandas`, or downstream skills.

## When to use this skill

- **SEO / content planning** — pick the higher-volume of "전기차 보조금" vs "EV 보조금" before writing.
- **K-commerce demand sensing** — see which sub-category in 화장품/미용 spiked last month before pitching.
- **Campaign timing** — confirm "수능 도시락" peaks early-November before launching ads.
- **Brand health** — compare brand keyword vs competitor weekly.
- **Influencer / blog audit** — back trend claims with NAVER's first-party numbers.
- **Multi-platform AI agents** — feed Korean trend signals into chat/blog/video generators.

## Do **not** use this skill for

- **Absolute search volume** — DataLab returns *relative* indices (0–100 range, normalized to the period peak), not raw query counts. NAVER intentionally never publishes raw counts.
- **Real-time trends** — DataLab data lags ~24-48 hours.
- **Google / YouTube / 다음 trends** — use `google-trends` or platform-specific skills.
- **Naver search results pages** — use `naver-search` (existing ClawHub skill).

## Prerequisites

1. **Register a NAVER Developers application** at <https://developers.naver.com/apps/#/register>:
   - Choose **검색어트렌드** AND **쇼핑인사이트** when picking APIs (you need both for full coverage).
   - Application type: usually **Web 서비스** with localhost callback is fine for personal use.
   - Approval is automatic — no business-day wait.
2. Export credentials:
   ```bash
   export NAVER_CLIENT_ID='abcdEFG12345'
   export NAVER_CLIENT_SECRET='AbCdEfGhIj'
   ```
3. Dependencies: `bash`, `curl`, `jq` (default on macOS/Linux).

Free-tier quota: **25,000 req/day** for `/v1/datalab/search`, **1,000 req/day** for shopping endpoints.

## Commands

### 1. `search` — 통합 검색어 트렌드

Compare up to 5 keyword groups over a time range:

```bash
scripts/search.sh \
  --start 2024-01-01 --end 2024-12-31 --time-unit month \
  --group "한국어:한국어,한글" \
  --group "영어:영어,English"
```

Optional filters: `--device pc|mo`, `--gender f|m`, `--ages 1,2,3` (1=under 12, 2=13-18, 3=19-24, 4=25-29, 5=30-34, 6=35-39, 7=40-49, 8=50-59, 9=60+). Up to 5 `--group` blocks; each group has 1-20 keywords.

Output (one record per group per period):
```json
{"groupName":"한국어","period":"2024-01-01","ratio":78.32}
```

### 2. `shop-cat` — 쇼핑인사이트 분야별 트렌드

```bash
scripts/shop-cat.sh \
  --start 2024-01-01 --end 2024-12-31 --time-unit month \
  --category "패션의류:50000000" \
  --category "화장품/미용:50000002"
```

Same filters as `search`. Up to 3 categories per call. Category IDs come from <https://datalab.naver.com/shoppingInsight/sCategory.naver>.

### 3. `shop-keyword` — 분야 내 키워드 트렌드

Drill into one category:

```bash
scripts/shop-keyword.sh \
  --start 2024-06-01 --end 2024-12-31 --time-unit week \
  --category 50000000 \
  --keyword "원피스:원피스" \
  --keyword "치마:치마,스커트"
```

### 4-6. `shop-device` / `shop-gender` / `shop-age`

Single-category breakdown by demographic:

```bash
scripts/shop-device.sh --start 2024-01-01 --end 2024-06-30 --time-unit month --category 50000000
scripts/shop-gender.sh --start 2024-01-01 --end 2024-06-30 --time-unit month --category 50000000
scripts/shop-age.sh    --start 2024-01-01 --end 2024-06-30 --time-unit month --category 50000000
```

Output rows include the demographic dimension:
```json
{"period":"2024-01-01","group":"pc","ratio":42.1}
{"period":"2024-01-01","group":"mo","ratio":100.0}
```

## Examples

See `examples/` for canned recipes:

- `examples/yearly-search.sh` — yearly comparison "전기차 vs 하이브리드".
- `examples/k-beauty-by-age.sh` — 화장품/미용 demographic split.
- `examples/seasonal-campaign.sh` — find "수능 도시락" peak month.

## Quirks the API doesn't document well

- `timeUnit` accepts **`date`, `week`, `month`** — *not* `day`. (Date with daily granularity *is* `date`.)
- `period` returned by daily/weekly is the *start* of the bucket, not the end.
- For shopping endpoints, the body field is `category` (singular) for the breakdown calls but `category` (array of objects) for `categories`. The wrapper hides this.
- Empty result → API returns `200 OK` with empty `results[].data`. The wrapper emits **no JSONL lines** for that group; check exit status and stderr.
- The `ratio` is **relative**, not absolute. The peak point in the entire response is normalized to 100.

## Categorical spec (excerpt)

| Code | Name |
|---|---|
| 50000000 | 패션의류 |
| 50000001 | 패션잡화 |
| 50000002 | 화장품/미용 |
| 50000003 | 디지털/가전 |
| 50000004 | 가구/인테리어 |
| 50000005 | 출산/육아 |
| 50000006 | 식품 |
| 50000007 | 스포츠/레저 |
| 50000008 | 생활/건강 |

Full tree: <https://datalab.naver.com/shoppingInsight/sCategory.naver>.

## Pairs with

- `naver-papago-translate` — translate the trend report into EN/JP/ZH for cross-market briefs.
- `tistory-api-cli` / `velog-cli` — publish weekly Korean-trend posts.
- `kr-holiday-cli` — overlay holiday/business-day calendar to interpret seasonal spikes.
- `kakao-local-cli` + `juso-address-cli` — geo-resolve any place names that emerge from trend keywords.
