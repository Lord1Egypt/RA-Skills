---
name: oo-perigon
description: "Perigon (perigon.io). Use this skill for ANY Perigon request — searching and reading data. Whenever a task involves Perigon, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Perigon"
  author: "OOMOL"
  version: "1.0.5"
  services: ["perigon"]
  icon: "https://static.oomol.com/logo/third-party/perigon.svg"
---

# Perigon

Operate **Perigon** through your OOMOL-connected account. This skill calls the `perigon` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Perigon. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "perigon" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "perigon" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_journalist` — Get one Perigon journalist profile by journalist ID.
- `search_articles` — Search Perigon news articles with keyword, date, entity, source, and category filters.
- `search_companies` — Search Perigon company entities by name, domain, symbol, industry, country, and exchange.
- `search_journalists` — Search Perigon journalist profiles by name, Twitter handle, post volume, and update date.
- `search_people` — Search Perigon people entities for Wikidata-backed profile metadata.
- `search_sources` — Search Perigon media sources by domain, source group, traffic, paywall, and geography filters.
- `search_stories` — Search Perigon story clusters for evolving news narratives and grouped article coverage.
- `search_topics` — Browse or search Perigon topics used to classify news content.
- `search_wikipedia` — Search Perigon Wikipedia pages by text, identity, category, revision, and pageview filters.
- `summarize_news` — Generate an AI summary over Perigon news articles matching the supplied filters.
- `vector_search_news` — Run semantic vector search over recent Perigon news articles with optional structured filters.
- `vector_search_wikipedia` — Run semantic vector search over Perigon Wikipedia content with optional structured filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Perigon state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Perigon is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/perigon
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Perigon homepage: https://perigon.io
- API documentation: https://docs.goperigon.com/
