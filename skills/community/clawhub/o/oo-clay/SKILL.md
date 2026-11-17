---
name: oo-clay
description: "Clay (clay.com). Use this skill for ANY Clay request — reading, creating, updating, and deleting data. Whenever a task involves Clay, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Clay"
  author: "OOMOL"
  version: "1.0.3"
  services: ["clay"]
  icon: "https://static.oomol.com/logo/third-party/clay.png"
---

# Clay

Operate **Clay** through your OOMOL-connected account. This skill calls the `clay` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Clay. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "clay" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "clay" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_search` — Create a stateful company or people search from a Clay query. Count-mode and jobs queries are unsupported. [write]
- `get_credit_balance` — Get workspace credit balances without consuming credits.
- `get_me` — Get the Clay user and workspace associated with the API key.
- `get_routine_batch_results` — Get batch progress, a result download URL, or validation/processing failure details. Download result_url separately after completion and inspect individual item outcomes; results are not loaded into the action response.
- `get_routine_results` — Get routine progress or one page of completed results. Follow cursor until absent and check each item's status.
- `get_search_query_reference` — Get the current Clay search query grammar and fields before creating a search.
- `get_search_results` — Fetch the next page and advance a Clay search iterator. Do not retry blindly: each call advances the iterator. [write]
- `get_workflow_run_query_reference` — Get the workflow-run query grammar and supported fields (beta).
- `query_tables` — Query known Clay tables on Enterprise plans. Concurrent updates can repeat rows; deduplicate by ID. Custom ordering and aggregation do not support cursor pagination.
- `query_workflow_runs` — Search or count workflow runs (beta). Results are eventually consistent; recently changed runs may be stale or absent.
- `run_routine` — Run a configured Clay routine on 1–100 items asynchronously. The routine may perform arbitrary downstream mutations; inspect its definition before running. [destructive]
- `run_routine_batch` — Download a JSONL file, upload it to Clay, and start an asynchronous batch routine. Each line must contain id and inputs. The routine may perform arbitrary downstream mutations. Connector transfer limit: 2 GiB, five minutes each for download and upload; JSONL validation is performed by Clay. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Clay state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Clay is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/clay
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Clay homepage: https://www.clay.com/
- API documentation: https://developers.clay.com/
