---
name: oo-tomba
description: "Tomba (tomba.io). Use this skill for ANY Tomba request — searching and reading data. Whenever a task involves Tomba, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tomba"
  author: "OOMOL"
  version: "1.0.2"
  services: ["tomba"]
  icon: "https://static.oomol.com/logo/third-party/tomba.svg"
---

# Tomba

Operate **Tomba** through your OOMOL-connected account. This skill calls the `tomba` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tomba. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tomba" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tomba" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `domain_search` — Search for email addresses and company intelligence for a domain.
- `email_count` — Count known email addresses and related breakdowns for a domain.
- `email_finder` — Find the most likely professional email address for a person at a domain.
- `email_sources` — Retrieve public source URLs where Tomba found an email address.
- `email_verifier` — Verify deliverability and metadata for an email address.
- `enrich` — Enrich a known email address with person and company attributes.
- `get_account` — Retrieve information about the authenticated Tomba account.
- `linkedin` — Find contact data associated with a public LinkedIn profile URL.
- `search_companies` — Search companies with Tomba Reveal using a natural-language query or filters.
- `technology` — Detect technologies and tools used by a company domain.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tomba state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tomba is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=tomba
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Tomba homepage: https://tomba.io
