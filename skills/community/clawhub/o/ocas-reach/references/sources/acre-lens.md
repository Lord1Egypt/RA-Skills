# AcreLens — US Land Due-Diligence MCP Server

## Overview

AcreLens is an MCP server that returns structured land due-diligence reports for any US property address. Data is sourced from NREL, USGS, and FEMA with full citations.

- **MCP endpoint:** `https://mcp.acrelens.com/mcp`
- **Transport:** Streamable HTTP
- **Status:** Healthy (as of 2026-06-05)
- **Auth:** None required
- **Quality score:** A (4.4/5.0 on Glama)

## When to Use

| User intent | Tool |
|---|---|
| "Analyze this land" / "tell me about this property" | `analyze_land` (full report) |
| "How suitable is this land for X" | `get_land_quick_score` (fast screen) |
| "Compare these two parcels" | `compare_properties` |
| "Solar potential for this address" | `get_solar_potential` |
| "What are the land regulations in New Mexico" | `get_state_land_profile` |

## Tools

### analyze_land
Full land analysis report async delivery.

**Modes:** `off_grid`, `rural_residential`, `recreational`, `investment`

**Required params:**
| Param | Type | Description |
|---|---|---|
| `address` | string | Full street address (e.g. "123 Cabin Rd, Taos, NM") |
| `state` | string | 2-letter US state code |
| `mode` | string | Analysis lens — one of the four modes |

**Optional params:** `county`, `acreage`, `lat`, `lng`

**Returns:** `{report_id, status, mode, estimated_completion_seconds, poll_url}`
- Initial status: `"authorized"` or `"processing"`
- Poll the URL: 202 while processing, 200 with full report
- Report includes: scores, confidence ratings, narrative summary, source citations

**Turnaround:** 60–120 seconds async

**Pitfalls:**
- If user intent is unclear, ask which mode before calling
- Provide `lat`+`lng` to skip geocoding (faster, more reliable)
- Provide `county` for better regulation research
- Poll with exponential backoff (start at `estimated_completion_seconds`)

### compare_properties
Side-by-side comparison of 2–5 parcels.

**Required params:**
| Param | Type | Description |
|---|---|---|
| `properties` | array | 2–5 property objects `{address, state, county?, acreage?, lat?, lng?}` |
| `mode` | string | Same mode applied to all properties |

**Returns:** `{batch_id, report_ids: [...], status: "processing"}`
- Poll each `report_id` individually
- All properties use the **same mode**

**Pitfalls:**
- Max 5 properties per call
- Comparing across modes requires separate calls
- Async — same polling pattern as `analyze_land`

### get_land_quick_score
Fast 0–100 suitability score without full report.

**Required params:** `address`, `state`, `mode`

**Returns:** `{report_id, status, score, confidence, summary}`
- Score: 0–100 integer
- Confidence: `"high"`, `"medium"`, or `"low"`
- Summary: one-sentence rationale

**Pitfalls:**
- Near-synchronous (fast) but may still return `"processing"` — retry if score is null
- Less detailed than `analyze_land` — use for initial screening

### get_solar_potential
Solar energy estimate via NREL PVWatts.

**Required params:** Either `address` OR (`lat` + `lng`)

**Optional params:** `system_size_kw` (default: 5)

**Returns:** `{annual_kwh, system_size_kw, latitude, longitude, cost_bracket}`

**Pitfalls:**
- Read-only — no side effects
- Cost bracket is indicative only, not a quote
- Default 5 kW system; override with `system_size_kw`

### get_state_land_profile
State-level land intelligence — regulation, climate, solar, water, building codes.

**Required params:** `state_code` (2-letter)

**Optional params:** `mode` (filter to one mode; returns all 4 if omitted)

**Returns:** `{state_code, modes: {mode_name: {overall_score, sub_scores, summary, key_regulations}}, shared_facts}`

**Pitfalls:**
- Read-only — no side effects
- Useful for upfront research before drilling into a specific property
- Without `mode`, returns all 4 modes (more data)

## Mode Guide

| Mode | Use when the user is... |
|---|---|
| `off_grid` | looking for self-sufficient homestead land, solar/off-grid living |
| `rural_residential` | buying acreage for a home, farmhouse, rural building |
| `recreational` | looking for hunting, camping, outdoor recreation land |
| `investment` | evaluating land ROI, holding value, resale potential |

## Error Handling

| Failure | Detection | Response |
|---|---|---|
| Invalid address | 400 or error in response | Ask user to verify address + state |
| Geocoding failure | Response indicates no match | Provide `lat`+`lng` explicitly |
| Async timeout | Poll returns 202 beyond `estimated_completion_seconds` × 3 | Report timeout, suggest retry |
| MCP unreachable | HTTP error on endpoint | Skip AcreLens, note degraded mode |
| Mode not applicable | Low confidence + poor score | Suggest trying a different mode |

## Source Citations

All reports cite data from:
- **NREL** (National Renewable Energy Laboratory) — solar data
- **USGS** (US Geological Survey) — groundwater, terrain
- **FEMA** — flood zone maps

## Quota

- ~1 req/min per tool (soft cap; no published hard limit)
- Largely limited by the 60–120s async turnaround, not API rate limits
- No account tier or paid plan required
