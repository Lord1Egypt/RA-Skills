---
name: oo-itunes-search
description: "iTunes Search API (performance-partners.apple.com). Use this skill for ANY iTunes Search API request — searching and reading data. Whenever a task involves iTunes Search API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "iTunes Search API"
  author: "OOMOL"
  version: "1.0.4"
  services: ["itunes_search"]
  icon: "https://static.oomol.com/logo/third-party/itunes_search.svg"
---

# iTunes Search API

Operate **iTunes Search API** through your OOMOL-connected account. This skill calls the `itunes_search` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

iTunes Search API needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "itunes_search" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "itunes_search" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `lookup_store` — Look up iTunes Store and Apple Books Store records by identifier, and optionally return the content related to each record, such as the albums of an artist or the tracks of an album. Identifier lookups are faster than searching and produce no false positives.
- `search_store` — Search the iTunes Store and Apple Books Store for music, movies, podcasts, apps, audiobooks, TV shows and books, and return the matching store records.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change iTunes Search API state — confirm the exact payload and effect with the user before running.**
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

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- iTunes Search API homepage: https://performance-partners.apple.com/search-api
- API documentation: https://performance-partners.apple.com/search-api
