---
name: oo-descript
description: "Descript (descript.com). Use this skill for ANY Descript request — reading, creating, updating, and deleting data. Whenever a task involves Descript, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Descript"
  author: "OOMOL"
  version: "1.0.3"
  services: ["descript"]
  icon: "https://static.oomol.com/logo/third-party/descript.svg"
---

# Descript

Operate **Descript** through your OOMOL-connected account. This skill calls the `descript` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Descript. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "descript" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "descript" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_job` — Cancel a running Descript job. [destructive]
- `get_job` — Get the current state and type-specific result of a Descript job.
- `get_project` — Get a Descript project with its media, compositions, and published links.
- `import_media` — Import URL-hosted media into a new or existing Descript project asynchronously. [write]
- `list_agent_models` — List the current Descript Underlord models and stable aliases.
- `list_jobs` — List recent Descript jobs with optional project, type, time, and pagination filters.
- `list_projects` — List projects accessible to the Drive associated with the Descript API token.
- `prompt_agent` — Submit an asynchronous Underlord request to create or edit a Descript project. [write]
- `publish_project` — Publish or republish a Descript composition and produce share and download URLs asynchronously. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Descript state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Descript is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/descript
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Descript homepage: https://www.descript.com/
- API documentation: https://docs.descriptapi.com/
