---
name: oo-label-studio
description: "Label Studio (labelstud.io). Use this skill for ANY Label Studio request — reading, creating, and updating data. Whenever a task involves Label Studio, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Label Studio"
  author: "OOMOL"
  version: "1.0.4"
  services: ["label_studio"]
  icon: "https://static.oomol.com/logo/third-party/label_studio.svg"
---

# Label Studio

Operate **Label Studio** through your OOMOL-connected account. This skill calls the `label_studio` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Label Studio. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "label_studio" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "label_studio" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_project` — Create a Label Studio project with a title and optional labeling configuration. [write]
- `create_task` — Create one Label Studio task from JSON task data. [write]
- `get_current_user` — Retrieve the Label Studio user associated with the connected API key.
- `get_project` — Retrieve one Label Studio project by ID.
- `list_projects` — List Label Studio projects visible to the connected API key.
- `list_tasks` — List Label Studio tasks, optionally filtered by project and Data Manager query.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Label Studio state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Label Studio is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/label_studio
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Label Studio homepage: https://labelstud.io
- API documentation: https://api.labelstud.io/api-reference/introduction/getting-started
