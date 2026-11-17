---
name: oo-tendata
description: "Tendata (tendata.cn). Use this skill for ANY Tendata request — searching and reading data. Whenever a task involves Tendata, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tendata"
  author: "OOMOL"
  version: "1.0.2"
  services: ["tendata"]
  icon: "https://static.oomol.com/logo/third-party/tendata.png"
---

# Tendata

Operate **Tendata** through your OOMOL-connected account. This skill calls the `tendata` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tendata. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tendata" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tendata" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `analyze_destinations` — Analyze matching trade volume, prices, and amount shares by destination country.
- `analyze_hs_codes` — Analyze matching trade volume, prices, and amount shares by HS code.
- `analyze_origins` — Analyze matching trade volume, prices, and amount shares by country of origin.
- `analyze_trade_trends` — Analyze matching trade activity by month, quarter, or year.
- `count_specific_trades` — Count matching trade records in specified authorized data sources without deducting points.
- `count_trades` — Count matching trade records before fetching paid details. This endpoint does not deduct points but consumes request quota.
- `get_account` — Retrieve account points balance and expiry. This endpoint does not report remaining daily request quota.
- `get_company` — Retrieve a company profile, contact methods, and trade statistics. Supply countryCode3 when known to disambiguate names.
- `get_contact_social_links` — Retrieve social profile links using the mailsouId returned by contact search. This endpoint does not deduct points.
- `get_exporter_stats` — Summarize exporter counts, trade volume, values, and average prices for a trade query.
- `get_importer_stats` — Summarize importer counts, trade volume, values, and average prices for a trade query.
- `list_charge_records` — Query one page of monthly charge records for reconciliation. Charges normally appear within five minutes; this query does not deduct points.
- `list_companies` — Search one page of company names and country codes to identify the company to query. This endpoint does not deduct points.
- `list_contacts` — Search one page of contacts associated with a company name. Results are capped at 200 per query; verify each returned companyName.
- `list_exporter_names` — List one page of exporter names matching a trade query.
- `list_exporters` — List one page of exporters with trade volume and price metrics, optionally sorted by a metric.
- `list_importer_names` — List one page of importer names matching a trade query.
- `list_importers` — List one page of importers with trade volume and price metrics, optionally sorted by a metric.
- `list_specific_trades` — Retrieve one page of trade records from specified authorized data sources. Use data source codes, not country codes.
- `list_trades` — Retrieve one page of trade records matching regular filters or advanced condition groups. Returned records may deduct account points.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tendata state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tendata is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tendata
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tendata homepage: https://www.tendata.cn/
- API documentation: https://open-api.tendata.cn/integration-guide.html
