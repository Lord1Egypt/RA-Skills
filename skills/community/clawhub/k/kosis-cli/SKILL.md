---
name: kosis-cli
description: Query Korea's national statistics portal (KOSIS, kosis.kr) via the official OpenAPI. Title search, category browsing, table metadata (items + dimensions + periods), and actual statistics data — population, employment, prices, business demographics, household income, regional indicators, etc. Use when a task needs Korean national statistics by organization/topic — e.g. "monthly CPI 2020-2025", "population by 시군구", "employment rate by age band", "household income decile". Pairs with bank-of-korea-ecos-cli (macro) and opendart-cli (corporate filings) to complete the Korean public-data toolchain.
version: 0.1.0
license: MIT
---

# kosis-cli

Minimal command-line wrapper for **KOSIS — 국가통계포털 (Korean Statistical Information Service)** OpenAPI.

KOSIS is the central registry for Korean national statistics maintained by Statistics Korea (통계청), aggregating ~1,000 datasets from 100+ government agencies. This wrapper exposes five operations:

1. `search` — keyword search across statistic titles (e.g. "소비자물가", "출생").
2. `list` — browse the statistics tree by topic/agency (참조 ID listing).
3. `meta` — fetch metadata for a specific table: classification items, period type, last updated.
4. `data` — pull actual numeric data for a `(orgId, tblId)` with item/dimension/period filters.
5. `bulk` — pull a large pre-saved `userStatsId` slice (saved on kosis.kr OpenAPI 활용신청).

All output is compact JSON (`format=json&jsonVD=Y`), one row per line (JSONL) so it pipes directly into `jq`.

## When to use this skill

Use when the task is **Korean national statistics shaped**:
- "Monthly CPI from 2020 to last month"
- "Population of every 시군구 in the latest census year"
- "Employment rate by gender × age band, 2024"
- "Number of newly registered businesses by industry, 통계청 기준"
- "Household income, 5분위, by year"

Do **not** use this skill for:
- **Macro-economic time series** (rates, FX, money supply, GDP components) → use `bank-of-korea-ecos-cli` (ECOS is more granular and timely for those).
- **Listed-company financial statements** → use `opendart-cli`.
- **Stock prices** → use `krx-stock-cli`.
- **Real-estate transaction data** → use the Ministry of Land's RTMS API (not yet wrapped).

## Prerequisites

1. Get an API key (인증키) at <https://kosis.kr/openapi/devGuide/devGuide_0102.do>. Sign up with a 통합인증 (KOSIS) account, click 활용 신청, fill out the application — keys are auto-issued instantly for the public catalog.
2. Export it:
   ```bash
   export KOSIS_API_KEY="N0NoeXVSRzlhUm5..."
   ```
3. Dependencies: `bash`, `curl`, `jq` (default on macOS/Linux).

## Commands

```bash
# 1) Title search
scripts/search.sh "소비자물가"
scripts/search.sh "출생률" --page 1 --per-page 20

# 2) Browse the catalog tree
scripts/list.sh                          # top-level topic categories
scripts/list.sh --vw-cd MT_OTITLE        # browse by agency instead of topic
scripts/list.sh --parent A               # children of category A (인구·가구)

# 3) Metadata for a specific table
#    orgId=101 (통계청), tblId=DT_1B040A3 (주민등록인구현황)
scripts/meta.sh 101 DT_1B040A3
scripts/meta.sh 101 DT_1B040A3 --type ITM     # only classification items
scripts/meta.sh 101 DT_1B040A3 --type OBJ     # only object dimensions

# 4) Actual data
#    Most-recent 3 monthly periods, all items, all L1 objects
scripts/data.sh 101 DT_1B040A3 --prd-se M --recent 3

#    Specific period range with explicit item & objects
scripts/data.sh 101 DT_1B040A3 \
  --prd-se M \
  --from 202401 --to 202412 \
  --itm "T20 T21" \
  --obj-l1 "11 21 22" \
  --obj-l2 ALL

# 5) Bulk fetch by user-saved slice
#    (after 활용신청 on kosis.kr, you receive userStatsId values)
scripts/bulk.sh 134567 --recent 12
```

Every script prints one JSON object per line on stdout; errors go to stderr with a non-zero exit code.

## Example JSONL output (`data.sh`)

```jsonl
{"PRD_DE":"202412","PRD_SE":"M","TBL_NM":"행정구역(시군구)별 주민등록인구","ITM_NM":"총인구수","C1_NM":"전국","DT":"51234567","UNIT_NM":"명","ORG_ID":"101","TBL_ID":"DT_1B040A3"}
```

Field cheatsheet:
- `PRD_DE` — period (YYYYMM for M, YYYY for Y, YYYYQ for Q)
- `PRD_SE` — period type (M/Q/Y/H/IR)
- `ITM_NM` / `ITM_ID` — measure (e.g. "총인구수", "남자")
- `C1_NM` … `C8_NM` — dimension labels (region, age, etc.) — number depends on table
- `DT` — value (string; cast to number caller-side)
- `UNIT_NM` — unit ("명", "원", "%", …)

## Rate limits & quotas

- Default key: **10,000 requests/day**, soft cap.
- Per-call response cap: **10,000 rows**. Use `--page` / `--per-page` (max 100,000 for `bulk`) and tighten with `--recent N` or explicit `--from/--to` when the slice is wide.
- The scripts **do not** retry on 429 / quota-exceeded — back off in the caller.

## Common `vwCd` (view code) values for `list`

| vwCd | Tree |
|---|---|
| `MT_ZTITLE` (default) | 국내통계 주제별 (population, prices, labor, …) |
| `MT_OTITLE` | 국내통계 기관별 (Statistics Korea, KEPCO, MOLIT, …) |
| `MT_CHITLE` | 대상별 통계 (women, youth, seniors, …) |
| `MT_GTITLE01` | e-지방지표 주제별 |
| `MT_GTITLE02` | e-지방지표 지역별 |

## Notes for agents

- **`orgId` + `tblId` is the primary key** of any table. Always start from `search` or `list` to discover it; do not guess.
- KOSIS items (`itmId`) and objects (`objL1` … `objL8`) are **table-specific** — always run `meta.sh` first to learn the codes for a table you haven't touched before.
- For period-aware tables, `prdSe` is required: `M` (월), `Q` (분기), `Y` (연), `H` (반기), `IR` (부정기).
- `--recent N` is shorthand for `newEstPrdCnt=N` and is the simplest way to get "the latest N periods" without computing dates.
- A 0-row response is a valid result (filter matched nothing); a row with `err` indicates a parameter mismatch.
- Korean column names (`*_NM`) are present alongside codes (`*_ID`) — prefer codes for joins/filters, names for display.

## Reference

- KOSIS OpenAPI dev guide: <https://kosis.kr/openapi/devGuide/devGuide_0101.do>
- Error codes: <https://kosis.kr/openapi/devGuide/devGuide_0103.do>
- Topic tree (browser): <https://kosis.kr/statisticsList/statisticsListIndex.do>
- License: MIT (this CLI wrapper). The underlying data is public under 공공누리 제1유형.
