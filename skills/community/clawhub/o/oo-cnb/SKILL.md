---
name: oo-cnb
description: "CNB (cnb.cool). Use this skill for ANY CNB request — reading, creating, and updating data. Whenever a task involves CNB, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CNB"
  author: "OOMOL"
  version: "1.0.2"
  services: ["cnb"]
  icon: "https://static.oomol.com/logo/third-party/cnb.svg"
---

# CNB

Operate **CNB** through your OOMOL-connected account. This skill calls the `cnb` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CNB. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cnb" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cnb" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_issue` — Create a repository issue with optional labels, assignees, dates and priority. Requires repo-issue:rw. [write]
- `create_issue_comment` — Add a comment to an issue. Requires repo-notes:rw. [write]
- `create_pull_request` — Create a pull request from a source branch into a target branch. Requires repo-pr:rw. [write]
- `get_build_status` — Get the current state and pipeline progress of an existing build. Requires repo-cnb-trigger:r.
- `get_issue` — Get an issue with its full description and metadata. Requires repo-issue:r.
- `get_pull_request` — Get pull request details and mergeability information. Requires repo-pr:r.
- `get_repository` — Get repository information. Requires repo-basic-info:r.
- `list_builds` — List pipeline build history, filtered by branch, event, commit or status. Requires repo-cnb-history:r.
- `list_issue_comments` — List issue comments. Requires repo-notes:r. Increase page until an empty page is returned.
- `list_issues` — List and filter repository issues. Requires repo-issue:r. Increase page until an empty page is returned.
- `list_pull_requests` — List repository pull requests with filters. Requires repo-pr:r. Increase page until an empty page is returned.
- `list_repositories` — List repositories accessible to the current user. Requires account-engage:r. The default minimum role is Guest; increase page until an empty page is returned.
- `update_issue` — Update issue content, dates, visibility, priority or workflow state. Supply state and state_reason together. Requires repo-issue:rw. [write]
- `update_pull_request` — Update a pull request title, description or open/closed workflow state. Requires repo-pr:rw. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CNB state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CNB is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/cnb
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- CNB homepage: https://cnb.cool/
- API documentation: https://docs.cnb.cool/zh/develops/openapi.html
