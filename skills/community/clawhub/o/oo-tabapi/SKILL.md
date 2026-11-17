---
name: oo-tabapi
description: "TabAPI (tabapi.com). Use this skill for ANY TabAPI request — searching and reading data. Whenever a task involves TabAPI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TabAPI"
  author: "OOMOL"
  version: "1.0.4"
  services: ["tabapi"]
  icon: "https://static.oomol.com/logo/third-party/tabapi.svg"
---

# TabAPI

Operate **TabAPI** through your OOMOL-connected account. This skill calls the `tabapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TabAPI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tabapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tabapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `capture_url_screenshot` — Capture the first viewport of one public HTTP or HTTPS URL and return a temporary hosted PNG URL.
- `extract_url_markdown` — Fetch one public HTTP or HTTPS URL through TabAPI and return clean Markdown with page metadata.
- `find_adsense_publisher_sites` — Find domains whose homepages were observed displaying one Google AdSense publisher identifier.
- `get_dns_records` — Resolve DNS records for one hostname through TabAPI's Cloudflare and Google DNS-over-HTTPS lookup.
- `get_domain_backlinks` — Retrieve backlink overview metrics and a sample of top referring pages for one domain or hostname.
- `get_domain_rdap` — Retrieve structured RDAP registration data for one domain, with a WHOIS-derived fallback when necessary.
- `get_domain_traffic` — Retrieve modeled website traffic, rank, engagement, source, keyword, region, and AI-referral estimates for one domain.
- `get_domain_whois` — Retrieve the original port-43 WHOIS text for one registrable domain.
- `google_search` — Search Google and return normalized organic results, ads, answer boxes, knowledge graph data, People Also Ask, and related searches.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TabAPI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TabAPI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tabapi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TabAPI homepage: https://tabapi.com
- API documentation: https://tabapi.com/docs
