---
name: oo-tapd
description: "TAPD (tapd.cn). Use this skill for ANY TAPD request — searching and reading data. Whenever a task involves TAPD, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TAPD"
  author: "OOMOL"
  version: "1.0.2"
  services: ["tapd"]
  icon: "https://static.oomol.com/logo/third-party/tapd.svg"
---

# TAPD

Operate **TAPD** through your OOMOL-connected account. This skill calls the `tapd` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TAPD. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tapd" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tapd" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `count_bugs` — Count TAPD bugs matching the supplied project and filters.
- `count_iterations` — Count TAPD iterations matching the supplied project and filters.
- `count_stories` — Count TAPD stories matching the supplied project and filters.
- `count_tasks` — Count TAPD tasks matching the supplied project and filters.
- `count_wikis` — Count TAPD wikis matching the supplied project and filters.
- `get_project` — Retrieve a TAPD project by its workspace ID.
- `list_bugs` — Query one page of TAPD bugs. Filter by id to retrieve specific records. Continue with the next page until an empty page is returned.
- `list_iterations` — Query one page of TAPD iterations. Filter by id to retrieve specific records. Continue with the next page until an empty page is returned.
- `list_projects` — List all projects in a TAPD company. This endpoint does not paginate.
- `list_stories` — Query one page of TAPD stories. Filter by id to retrieve specific records. Continue with the next page until an empty page is returned.
- `list_tasks` — Query one page of TAPD tasks. Filter by id to retrieve specific records. Continue with the next page until an empty page is returned.
- `list_wikis` — Query one page of TAPD wikis. Filter by id to retrieve specific records. Continue with the next page until an empty page is returned.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TAPD state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TAPD is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tapd
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TAPD homepage: https://www.tapd.cn/
- API documentation: https://open.tapd.cn/document/api-doc/API文档/api_reference/
