---
name: mfds-cli
description: Korean Ministry of Food and Drug Safety (식품의약품안전처) public API CLI. Search drug product permissions (의약품 허가정보), consumer-friendly drug info (e약은요), DUR contraindications (병용금기/특정연령금기/임부금기/효능군중복), and drug recall/sale-stop alerts. Returns clean JSONL for AI agents. Use for pharmacy AI, medication-safety bots, prescription review, supplement diligence, and Korean healthcare data pipelines. Requires a free MFDS_API_KEY from data.go.kr.
license: MIT-0
---

# mfds-cli — Korea Ministry of Food and Drug Safety (식품의약품안전처) CLI

Wraps four high-value MFDS Open APIs published on **data.go.kr**: drug master, e약은요 (consumer drug leaflet), DUR contraindications, and drug recalls / sale-stop notices. Every endpoint returns XML or JSON; this skill normalizes everything to **JSONL** so AI agents can pipe it straight into a vector store, a notebook, or another tool.

> **Why this matters**: Korean drug data is the highest-traffic public-data category on data.go.kr after real estate. Pharmacy chatbots, medication-safety agents, and clinical-decision tools need a single, clean interface — not four separate XML wrappers. This is the only ClawHub skill covering MFDS at the time of publish.

## Quick start

```bash
export MFDS_API_KEY="<your-decoded-serviceKey>"   # from data.go.kr (free, instant approval)

# Search the drug master by Korean or English name
bin/mfds-cli drug --name "타이레놀" --rows 5

# Consumer-friendly drug leaflet (efficacy, dosage, side effects, storage)
bin/mfds-cli drug-easy --name "게보린" --rows 3

# Drug-drug interaction (병용금기) lookup
bin/mfds-cli dur --type interaction --name "와파린"

# Drugs recalled or sales-suspended this year
bin/mfds-cli recall --year 2026 --rows 50
```

## Subcommands

| Command | API | Use case |
|---|---|---|
| `drug` | DrugPrdtPrmsnInfoService06 | Drug product master — 품목명/제조사/허가번호/제형/주성분 |
| `drug-easy` | DrbEasyDrugInfoService (e약은요) | Consumer leaflet — 효능/용법/주의/부작용/보관 |
| `dur` | DURPrdlstInfoService03 (8 sub-types) | DUR contraindications and warnings |
| `recall` | MdcinExecRslt2Service | Drug recall, sales-stop, disposal orders |

### Common flags

- `--key <KEY>` — override `$MFDS_API_KEY`
- `--rows N` — page size (default 30, max 100)
- `--page N` — 1-indexed page (default 1)
- `--format jsonl|json|xml` — output (default jsonl)
- `--raw` — pass through API response without normalization (for debugging)
- `--endpoint <full-url>` — escape hatch when MFDS rotates a service version

### `drug` — drug master

| Flag | Maps to | Notes |
|---|---|---|
| `--name "<text>"` | `item_name` | 품목명 (Korean or English) |
| `--maker "<text>"` | `entp_name` | 업체명 |
| `--item-seq <13-digit>` | `item_seq` | 품목기준코드 |
| `--bizrno <10-digit>` | `bizrno` | 업체 사업자등록번호 |
| `--type-code <code>` | `prduct_type` | 전문/일반/원료의약품 등 |
| `--cancel-name <text>` | `cancel_name` | 취소사유 (검색 시 취하/취소된 의약품도 포함) |

### `drug-easy` — consumer leaflet (e약은요)

| Flag | Maps to | Notes |
|---|---|---|
| `--name "<text>"` | `itemName` | 품목명 |
| `--maker "<text>"` | `entpName` | 업체명 |
| `--item-seq <13-digit>` | `itemSeq` | |
| `--query-efficacy "<text>"` | `efcyQesitm` | 효능 키워드 검색 |
| `--query-method "<text>"` | `useMethodQesitm` | 용법 키워드 |
| `--query-warning "<text>"` | `atpnQesitm` | 주의사항 키워드 |
| `--query-side-effect "<text>"` | `seQesitm` | 부작용 키워드 |
| `--query-storage "<text>"` | `depositMethodQesitm` | 보관법 키워드 |

### `dur` — DUR contraindication lookup

The DUR API publishes 8 distinct lists. Use `--type` to pick:

| `--type` | Korean | What it tells you |
|---|---|---|
| `interaction` | 병용금기 | Drug A + Drug B should not be taken together |
| `age` | 특정연령대금기 | Forbidden under N years old |
| `pregnancy` | 임부금기 | Forbidden during pregnancy + grade A/B/C/D/X |
| `capacity` | 용량주의 | Daily-dose cap warning |
| `period` | 투여기간주의 | Max consecutive days warning |
| `elderly` | 노인주의 | 65+ caution |
| `efficacy-duplicate` | 효능군중복 | Same therapeutic class — risk of double-dose |
| `extended-release` | 서방정분할주의 | Do not split this extended-release tablet |

Filters: `--name "<품목명>"`, `--ingredient "<주성분명>"`, `--type-name "<DUR유형명>"`.

### `recall` — recall / sales-stop / disposal

| Flag | Notes |
|---|---|
| `--year YYYY` | 시정조치년도 |
| `--name "<text>"` | 품목명 |
| `--maker "<text>"` | 제조/수입업체명 |
| `--action <code>` | 시정조치코드 (회수/판매중지/폐기 등) |

## Output schema (JSONL)

Each record is one line. The CLI normalizes MFDS XML/JSON into a stable shape; `_raw` retains the original API field names for fields the normalizer doesn't yet cover.

```json
{
  "type": "drug",
  "item_seq": "200005221",
  "item_name_ko": "타이레놀정500밀리그람(아세트아미노펜)",
  "item_name_en": "Tylenol Tab. 500mg (Acetaminophen)",
  "maker": "한국얀센(주)",
  "permit_no": "200500001",
  "permit_date": "20051018",
  "form_code": "정제",
  "main_ingredient": "아세트아미노펜 500mg",
  "atc_code": "N02BE01",
  "kpic_code": "643301250",
  "narcotic": false,
  "prescription": "일반의약품",
  "_raw": { "...": "..." }
}
```

## Examples

The `examples/` folder includes:
- `drug-name-to-leaflet.sh` — chain `drug` → `drug-easy` to get full consumer info from a brand name
- `prescription-safety-check.sh` — given a list of drug names, flag DUR interactions and pregnancy warnings
- `recall-watch.sh` — daily delta of recalls vs. yesterday's snapshot

## Getting an API key

1. Register at https://www.data.go.kr (Naver / Kakao social login OK).
2. Search "의약품제품허가정보" (or any of the 4 services) and click **활용신청**.
3. Approval is automatic for development tier (10,000 calls/day).
4. Copy the **decoded** service key (not the URL-encoded one) and `export MFDS_API_KEY=...`.

The same key works across all four services after you register each one.

## Rate limits

- Development tier: 10,000 requests/day per service.
- Production tier: unlimited after publishing a use case.
- The CLI does not retry on 429; if you hit it, slow down with `sleep 0.2` between calls.

## License

MIT-0 — public-domain-equivalent. MFDS data itself is **공공누리 제1유형** (free use with attribution to 식품의약품안전처).
