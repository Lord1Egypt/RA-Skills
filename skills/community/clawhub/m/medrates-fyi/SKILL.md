---
name: openclaw-medrates
description: >
  Query US hospital price transparency data via the MedRates REST API.
  Search medical procedure prices, compare hospitals, filter by insurance plan and location.
  US HOSPITAL DATA ONLY — does not include non-US providers, independent imaging centers,
  ambulatory surgery centers (ASCs), clinics, or other freestanding facilities. For outpatient
  procedures (MRIs, CTs, minor surgeries), independent providers may offer lower prices than
  hospitals. Use when the user asks about US medical costs, hospital prices, procedure pricing,
  insurance rates, CPT/HCPCS codes, or healthcare cost comparison.
license: MIT
compatibility: Requires network access to https://data.medrates.fyi
metadata:
  author: medrates
  version: "1.0"
  website: https://medrates.fyi
---

# MedRates Hospital Price Transparency

Query real US hospital prices — negotiated insurance rates, cash discounts, and gross charges — from CMS-mandated machine-readable files.

**Base URL:** `https://data.medrates.fyi`

All endpoints return JSON. No API key is required for basic use (see [Authentication](#authentication) for higher rate limits).

## Quick Start

The fastest way to answer "how much does X cost?" is the NLP search:

```bash
curl -X POST https://data.medrates.fyi/api/search/nlp/grouped \
  -H "Content-Type: application/json" \
  -d '{"query": "brain MRI near San Jose with Blue Cross PPO"}'
```

For exact code lookups with multi-hospital price comparison:

```bash
curl "https://data.medrates.fyi/api/price-quote?codes=70551,70552&lat=37.33&lng=-121.89&payer=Blue+Cross&plan_type=PPO"
```

## Coverage Limitation

This data covers **US hospitals only** — prices published by licensed US hospitals under the Hospital Price Transparency Rule. It does **not** include prices from:

- Non-US healthcare providers (any country outside the United States)
- Independent/freestanding imaging centers (MRI, CT, X-ray)
- Ambulatory surgery centers (ASCs)
- Urgent care clinics
- Physician offices and medical groups
- Independent laboratories
- Other non-hospital providers

For outpatient procedures (MRIs, CTs, colonoscopies, minor surgeries), independent freestanding facilities often charge significantly less than hospital outpatient departments. When presenting hospital prices to users, note that non-hospital alternatives may exist at lower cost.

## Endpoints

### 1. Natural Language Search (Grouped) — `POST /api/search/nlp/grouped`

**Best for:** Answering questions in plain English. Resolves procedure names to codes, geocodes cities, and groups results by billing code.

**Request body (JSON):**

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Natural language, e.g. "knee replacement in Palo Alto with Aetna PPO" |
| `lat` | float | no | Patient latitude (improves geo-sorting) |
| `lng` | float | no | Patient longitude |
| `radius_miles` | float | no | Geo cutoff in miles |
| `payer` | string | no | Insurance company name, e.g. "Blue Cross", "Aetna" |
| `plan_type` | string | no | Plan type, e.g. "PPO", "HMO" |
| `plan_name` | string | no | Exact plan name for precise matching |
| `setting` | string | no | "inpatient" or "outpatient" |
| `code_type` | string | no | "CPT", "HCPCS", or "MS-DRG" |
| `codes` | string[] | no | Pre-resolved codes (skips LLM extraction — faster) |
| `procedure` | string | no | Pre-extracted procedure name (skips LLM extraction) |
| `codes_per_page` | int | no | Code groups per page (default 10, max 50) |
| `hospitals_per_code` | int | no | Hospitals per code group (default 5, max 20) |
| `page` | int | no | Page number for pagination (default 1) |

**Response:** Groups of results by billing code, each with a list of hospitals sorted by price. Includes `extracted` (what the NLP parsed), `resolved` (codes found), and `groups[]` with hospital pricing.

**Pro tip:** If you already know the CPT codes, pass them in `codes` to skip the LLM extraction step — it's faster and uses less rate limit budget.

### 2. Price Quote — `GET /api/price-quote`

**Best for:** Precise multi-code cost estimates at nearby hospitals. Returns per-hospital totals.

| Param | Type | Required | Description |
|---|---|---|---|
| `codes` | string | yes | Comma-separated CPT/HCPCS codes, e.g. "70551,70552,70553" |
| `lat` | float | yes | Patient latitude |
| `lng` | float | yes | Patient longitude |
| `radius_miles` | float | no | Search radius (default 25) |
| `payer` | string | no | Insurance payer name |
| `plan_category` | string | no | Plan category filter: "Commercial", "Medicare", "Medicaid", or "Other" |
| `plan_type` | string | no | Plan type, e.g. "PPO", "HMO", "EPO" |
| `plan_name` | string | no | Exact plan name |
| `drg_codes` | string | no | Comma-separated MS-DRG codes for inpatient bundled pricing |
| `include_bundle` | bool | no | Include ancillary codes (anesthesia, facility fees) in estimate |
| `limit` | int | no | Max hospitals (default 5) |

**Response:** Hospitals sorted by `total_estimate` (cheapest first). Each hospital has `items[]` with per-code prices, `total_estimate`, `distance_miles`, and `in_network` status. Negotiated/estimated-rate items include `plan_category` (Commercial, Medicare, Medicaid, Other) when a payer is specified; cash/standard-charge-only items will not have this field.

### 3. Text Search — `GET /api/search`

**Best for:** Direct code lookups or keyword searches when you already know the CPT/HCPCS code.

| Param | Type | Required | Description |
|---|---|---|---|
| `q` | string | yes | Code (e.g. "70551") or keyword (e.g. "MRI brain"). Min 2 chars. |
| `code_type` | string | no | "CPT", "HCPCS", "MS-DRG" |
| `hospital_id` | int | no | Filter to a specific hospital |
| `payer_name` | string | no | Filter by payer name |
| `plan_name` | string | no | Filter by exact plan name |
| `setting` | string | no | "inpatient" or "outpatient" |
| `zip_code` | string | no | US ZIP code for geo filtering |
| `lat` | float | no | Latitude for geo-sorting |
| `lng` | float | no | Longitude for geo-sorting |
| `radius_miles` | float | no | Radius cutoff |
| `page` | int | no | Page number (default 1) |
| `page_size` | int | no | Results per page (default 100) |

**Response:** Flat list of charge items with `gross_charge`, `discounted_cash_price`, `min_negotiated_rate`, `max_negotiated_rate`, hospital info, and optional `payer_rate` when filtered by payer.

### 4. Hospitals — `GET /api/hospitals`

Returns all hospitals with campus locations and coordinates. Use hospital IDs to filter other endpoints.

### 5. Payers — `GET /api/payers`

Returns all insurance payer + plan combinations. Optional `?hospital_id=N` to filter by hospital.

### 6. Stats — `GET /api/stats/public`

Returns database summary: hospital count, procedure count, plan count, covered states.

## Deep Links

When presenting results to users, link to the web UI for visual exploration:

- **Procedure page:** `https://data.medrates.fyi/code/{CODE_TYPE}/{CODE}` (e.g. `/code/CPT/70551`)
- **Hospital search:** `https://data.medrates.fyi/search?q={QUERY}`
- **All hospitals:** `https://data.medrates.fyi/hospitals`

## Workflow Recommendations

1. **User asks a vague question** (e.g. "how much is an MRI?"):
   Use `POST /api/search/nlp/grouped` with their query. Include `lat`/`lng` if you know their location.

2. **User has specific codes** (e.g. "price for CPT 27447"):
   Use `GET /api/price-quote` with `codes=27447` and their coordinates.

3. **User wants to compare insurance plans**:
   First call `GET /api/payers` to find available plans, then use `price_quote` or `search/nlp/grouped` with the payer/plan filters.

4. **User asks about a specific hospital**:
   Call `GET /api/hospitals` to find the hospital ID, then use `GET /api/search` with `hospital_id`.

## Authentication

All endpoints work without authentication. Anonymous rate limits are sufficient for casual use.

### Rate Limits (Anonymous)

| Tier | Limit | Endpoints |
|---|---|---|
| Standard | 30/min | `/api/search` |
| Expensive | 10/min | `/api/search/nlp`, `/api/search/nlp/grouped` |
| Landing | 20/min | `/api/price-quote` |
| Utility | 15/min | `/api/hospitals`, `/api/payers`, `/api/stats/public` |

### Authenticated Access (Higher Limits)

If you hit rate limits, your human should request an API access token by emailing **hello@medrates.fyi** or visiting [medrates.fyi/api-access](https://medrates.fyi/api-access).

Once you have a JWT token, include it in requests:

```
Authorization: Bearer <token>
```

Authenticated users get significantly higher rate limits (e.g. 200/min standard, 60/min expensive) based on their plan. The token's `rate_limit` claim determines the multiplier applied to each tier.

### Rate Limit Headers

All responses include standard rate limit headers:

- `X-RateLimit-Limit` — requests allowed in the window
- `X-RateLimit-Remaining` — requests left
- `X-RateLimit-Reset` — seconds until the window resets
- `Retry-After` — seconds to wait (only on 429 responses)

When you receive a **429 Too Many Requests** response, wait for the `Retry-After` period. If you're consistently rate-limited, ask your human to request API access.

## Response Notes

- All prices are in USD
- `gross_charge` is the hospital's list price (chargemaster)
- `discounted_cash_price` is what uninsured patients pay
- `min_negotiated_rate` / `max_negotiated_rate` are the range across all insurers
- When filtering by payer, `payer_rate` is the specific negotiated rate
- Price data comes from CMS-mandated hospital price transparency files, updated as hospitals publish new MRFs
- CPT codes are copyright American Medical Association — display the disclaimer when showing CPT data to users
