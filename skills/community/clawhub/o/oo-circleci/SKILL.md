---
name: oo-circleci
description: "CircleCI (circleci.com). Use this skill for ANY CircleCI request — reading, creating, and updating data. Whenever a task involves CircleCI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CircleCI"
  author: "OOMOL"
  version: "1.0.1"
  services: ["circleci"]
  icon: "https://static.oomol.com/logo/third-party/CircleCI.svg"
---

# CircleCI

Operate **CircleCI** through your OOMOL-connected account. This skill calls the `circleci` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CircleCI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "circleci" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "circleci" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_current_user` — Get the currently authenticated CircleCI user profile.
- `get_job_artifacts` — List artifacts for a CircleCI job.
- `get_job_details` — Get CircleCI job details by project slug and job number.
- `get_pipeline` — Get a CircleCI pipeline by pipeline ID.
- `get_project` — Get CircleCI project details by project slug.
- `get_workflow_summary` — Get CircleCI Insights summary metrics for a workflow.
- `list_insights_summary` — Get CircleCI Insights summary metrics for an organization.
- `list_pipelines_for_project` — List CircleCI pipelines for a project.
- `list_project_env_vars` — List masked CircleCI environment variables for a project.
- `list_workflows_by_pipeline` — List workflows for a CircleCI pipeline.
- `trigger_pipeline` — Trigger a new CircleCI pipeline for a project. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CircleCI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CircleCI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=circleci
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- CircleCI homepage: https://circleci.com
