---
name: oo-adyntel
description: "Adyntel (adyntel.com). Use this skill for ANY Adyntel request — searching and reading data. Whenever a task involves Adyntel, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Adyntel"
  author: "OOMOL"
  version: "1.0.4"
  services: ["adyntel"]
  icon: "https://static.oomol.com/logo/third-party/adyntel.png"
---

# Adyntel

Operate **Adyntel** through your OOMOL-connected account. This skill calls the `adyntel` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Adyntel. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "adyntel" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "adyntel" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_domain_keywords` — Get Adyntel paid and organic keyword metrics for a company domain.
- `get_tiktok_ad_details` — Get details for one TikTok ad by ID using Adyntel.
- `search_google_ads` — Search Google ads for a company domain using Adyntel's Google ad library endpoint.
- `search_linkedin_ads` — Search LinkedIn ads for a company domain or LinkedIn page ID using Adyntel.
- `search_meta_ads` — Search Facebook and Instagram ads for a company using Adyntel's Meta ad library endpoint.
- `search_tiktok_ads` — Search TikTok ads by keyword using Adyntel's TikTok ad library endpoint.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Adyntel state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Adyntel is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/adyntel
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Adyntel homepage: https://www.adyntel.com
- API documentation: https://docs.adyntel.com/
