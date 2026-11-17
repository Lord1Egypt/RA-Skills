---
name: oo-greenhouse
description: "Greenhouse (greenhouse.com). Use this skill for ANY Greenhouse request — reading, creating, and updating data. Whenever a task involves Greenhouse, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Greenhouse"
  author: "OOMOL"
  version: "1.0.4"
  services: ["greenhouse"]
  icon: "https://static.oomol.com/logo/third-party/greenhouse.svg"
---

# Greenhouse

Operate **Greenhouse** through your OOMOL-connected account. This skill calls the `greenhouse` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Greenhouse. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "greenhouse" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "greenhouse" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_candidate_note` — Create a Greenhouse candidate activity feed note using an explicit On-Behalf-Of audit user. [write]
- `get_application` — Retrieve one Greenhouse application by ID.
- `get_candidate` — Retrieve one Greenhouse candidate by ID.
- `get_job` — Retrieve one Greenhouse job by ID.
- `list_applications` — List Greenhouse applications with optional candidate, job, and status filters.
- `list_candidates` — List Greenhouse candidates with optional job, email, candidate ID, and timestamp filters.
- `list_jobs` — List Greenhouse jobs with optional status, department, and timestamp filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Greenhouse state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Greenhouse is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/greenhouse
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Greenhouse homepage: https://www.greenhouse.com
- API documentation: https://developers.greenhouse.io/harvest.html
