---
name: oo-indeed
description: "Indeed (indeed.com). Use this skill for ANY Indeed request — reading, creating, updating, and deleting data. Whenever a task involves Indeed, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Indeed"
  author: "OOMOL"
  version: "1.0.4"
  services: ["indeed"]
  icon: "https://static.oomol.com/logo/third-party/indeed.svg"
---

# Indeed

Operate **Indeed** through your OOMOL-connected account. This skill calls the `indeed` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Indeed. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "indeed" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "indeed" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clear_sourced_job_posting_updates` — Clear updates previously applied to one sourced Indeed job posting. [destructive]
- `find_employer_jobs` — List jobs for the employer represented by the OAuth token, with filters and cursor pagination.
- `get_current_user` — Get the Indeed user and associated employers represented by the OAuth access token.
- `get_job` — Get one Indeed employer job by its EmployerJob IRI.
- `get_jobs` — Get multiple Indeed employer jobs by their EmployerJob IRIs.
- `update_sourced_job_postings` — Update supported fields on one sourced Indeed job posting. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Indeed state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Indeed is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/indeed
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Indeed homepage: https://www.indeed.com
- API documentation: https://docs.indeed.com/
