---
name: northdata
description: Use NorthData (German commercial-register + financials API) to look up companies, owners, representatives, financials, publications, and person records. Triggers on queries about NorthData itself, looking up a specific German company (GmbH, UG, KG, HRB/HRA register entries), finding owners / Geschäftsführer / Gesellschafter, reading a company's revenue / earnings / balance sheet, searching by NACE segment or legal form or geography, checking NorthData credit usage, or power-searching for acquisition / lead candidates. Activates for terms like "northdata", "north data", "Handelsregister", "HRB", "HRA", "Gesellschafter", "Geschäftsführer", "GmbH Finanzen", "Firma recherchieren", "NACE-Suche", "Power Search", "company profile". Provides best-practice guidance for both the `northdata` CLI (Claude Code / terminal) and the NorthData MCP server (Claude Desktop / any MCP client) — whichever is available in the current environment.
---

# NorthData Companion Skill

This skill is the best-practice guide for working with the NorthData API through either:

1. **`northdata` CLI** — a command-line tool, typically used in Claude Code or a terminal.
2. **NorthData MCP server** — a set of tools exposed over the Model Context Protocol, typically used in Claude Desktop / Cursor / other MCP clients.

Both surfaces are built on the same `NorthDataClient` and share the same credit-guard discipline. Pick whichever is available in the current environment — this skill covers both.

## Detect what's available

Before deciding, check what's reachable:

| Check | Available? |
|---|---|
| MCP tools named `suggest`, `company`, `person`, … | Use MCP. |
| `northdata` on `$PATH` (try `which northdata` or `northdata --version`) | Use CLI. |
| Neither | Ask the user to install — point at `northdata-cli` (pipx) and/or the MCP server config. |

If both are available: **prefer MCP** when running inside an MCP-aware client (clearer tool telemetry, structured errors). **Prefer CLI** in Claude Code or any shell-driven context.

## The one rule you must internalize

**NorthData charges per returned company, not per HTTP call.** A single `search --limit 100` costs up to 100 credits in one go. Every billed call goes through the two-tier credit guard:

| Tier | Default | How to relax |
|---|---|---|
| Approval threshold — `limit > 25` needs `--approve-high-cost` (CLI) or `approve_high_cost=true` (MCP) | `25` | `NORTHDATA_APPROVAL_THRESHOLD` env |
| Absolute maximum — hard cap, flag-immune | `100` | `NORTHDATA_ABSOLUTE_MAX` env — set by a human, never by an agent |

Never suggest raising either without a clear reason from the user.

## Default workflow (use this order)

1. **Start free.** `suggest`, `reference_*`, `billing` — zero credits. Use them to find the right company / confirm register IDs / check remaining quota before committing.
2. **Dry-run anything billed.** Both surfaces accept `--dry-run` (CLI) or `dry_run=true` (MCP). Use it first when parameters are uncertain — it builds the URL without calling the API.
3. **One `company` call is usually enough.** It returns owners, representatives, financials, sheets, events, contact extras. Don't also call `publications` or `person` unless you specifically need shareholder lists or a person's birth date.
4. **Log watch.** After billed calls, `credits` (CLI) / `local_credit_log` (MCP) shows what this session spent. `billing` shows what NorthData counts remotely.

## Tool reference

### Free tools

| Purpose | CLI | MCP |
|---|---|---|
| Autocomplete a name | `northdata suggest "Example GmbH"` | `suggest` |
| Current period usage | `northdata billing` | `billing` |
| API reference (standards, countries, …) | `northdata reference overview` | `reference_overview` |
| Segment codes for a standard | `northdata reference segments --standard NACE2025` | `reference_segment_codes` |
| Local (session) credit log | `northdata credits` | `local_credit_log` |

### Billed tools

| Purpose | CLI | MCP | Cost |
|---|---|---|---|
| Full company profile | `northdata company --name "X" --city "Y"` or `--register "HRB 1/München"` | `company` | **1** |
| Person lookup (birth date, roles) | `northdata person Max Mustermann --city München` | `person` | **1** |
| Publications (e.g. Gesellschafterliste) | `northdata publications --name "X" --source Hrb` | `publications` | **1** |
| Power search (filtered) | `northdata search --segment-codes 62 --legal-forms GmbH --limit 5` | `search` | **up to `limit`** |

All billed tools accept `--dry-run` / `dry_run=true`.

## Common workflows

### "Find Company X and tell me about it"

1. `suggest "Company X"` (free) — pick the right one if multiple.
2. `company --register "<register from suggest>"` **or** `--name "<exact name>" --city "<city>"` (1 credit).
3. Done. Owners, representatives, financials, sheets, events all come back in one payload.

### "Who owns / runs Company X?"

`company` returns `owners` (Gesellschafter) and `representatives` (Geschäftsführer) in the same response. Don't chain multiple calls — one `company` call is enough.

For the **birth date** of a named person (e.g. succession planning), follow up with `person --first-name … --last-name … --city …` (1 credit).

### "Find me companies matching these criteria"

Use `search` (power search). Always:

- Set `segment_codes` (NACE) and `legal_forms` — an unfiltered search is expensive and rarely useful.
- Keep `limit` low (default `5`). Only raise with explicit user approval.
- Use `--dry-run` first to sanity-check parameters.
- For geo-filters combine `address` + `max_distance_km`.
- Indicators: `revenue_min/max`, `earnings_min/max` narrow down the result set before spending credits.

Example (CLI):
```bash
northdata search \
  --segment-codes "62|63" \
  --legal-forms "GmbH|UG" \
  --address "Munich" --max-distance-km 150 \
  --revenue-min 5000000 --revenue-max 50000000 \
  --limit 5 --dry-run
```

Verify the URL, then re-run without `--dry-run`.

Paginate via the `pos` token in the previous response's `nextPos`.

### "Check if a register ID is valid before I spend a credit"

`suggest` returns the canonical `register.uniqueKey` and `register.id`. That's free. Then pass `--register` to `company` exactly as shown.

### "How many credits am I using?"

- Remote total (period): `billing`
- This session only (local log): `credits` / `local_credit_log`

## Common pitfalls

### `HTTP 404 "not found"` on `company --register`

The register string must match NorthData's format. If `"HRB 296816/München"` returns 404, try:

1. `suggest` first — copy the exact `register.id` (e.g. `"HRB 296816"`) and `register.uniqueKey` from the response.
2. Fall back to `--name + --city` — more forgiving than register matching.

### Only `numberOfRequests` seems to count unique calls

NorthData's `billing` endpoint returns **unique** requests per period. Repeated identical calls (same company, same day) don't increment the counter. The local credit log counts every attempted call regardless.

### `search` with no segment filter

Never run `search` with empty `segment_codes` and `legal_forms`. The credit guard allows it, but the cost/signal ratio is terrible. Always scope.

### Umlauts in register strings

URL-encoding is automatic in both surfaces. You can pass `"München"` directly — no manual percent-encoding needed.

### `--approve-high-cost` / `approve_high_cost=true`

Only set when the user has explicitly agreed to spend more. Never set preemptively "to make it work".

## Environment knobs

| Var | Purpose |
|---|---|
| `NORTHDATA_API_KEY` | API key (required) |
| `NORTHDATA_APPROVAL_THRESHOLD` | Raises the soft threshold (default 25) |
| `NORTHDATA_ABSOLUTE_MAX` | Raises the hard ceiling (default 100) |
| `NORTHDATA_CREDIT_LOG` | Overrides local log location |

## When the user is stuck

| Symptom | Likely cause | Fix |
|---|---|---|
| `No API key found` | `NORTHDATA_API_KEY` not set | Export it, or (CLI) pass `--api-key` |
| `credit-guard: limit=X exceeds APPROVAL_THRESHOLD` | High `--limit` without opt-in | Lower limit or add `--approve-high-cost` |
| `credit-guard: limit=X exceeds ABSOLUTE_MAX` | Above hard cap | Split into paginated calls via `pos`, or raise env var |
| `api error: HTTP 429` | Rate-limited | Wait, retry later. Client already retries once. |
| `api error: HTTP 404` on `company` | Bad register ID or unknown name | Use `suggest` first to get canonical identifiers |
| Tools not visible in Claude Desktop | MCP server not registered or Claude not fully restarted | Check `~/Library/Application Support/Claude/claude_desktop_config.json`; fully quit with ⌘Q |

## Resources

- NorthData API docs: <https://github.com/northdata/api>
- CLI package: `northdata-cli/` (this repo)
- MCP server: `northdata-mcp/` (this repo)
