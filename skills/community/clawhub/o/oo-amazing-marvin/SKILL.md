---
name: oo-amazing-marvin
description: "Amazing Marvin (amazingmarvin.com). Use this skill for ANY Amazing Marvin request — reading, creating, and updating data. Whenever a task involves Amazing Marvin, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Amazing Marvin"
  author: "OOMOL"
  version: "1.0.2"
  services: ["amazing_marvin"]
  icon: "https://static.oomol.com/logo/third-party/amazing_marvin.png"
---

# Amazing Marvin

Operate **Amazing Marvin** through your OOMOL-connected account. This skill calls the `amazing_marvin` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Amazing Marvin. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "amazing_marvin" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "amazing_marvin" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `complete_task` — Mark a Marvin task complete. This experimental API does not reproduce all client recurrence and reward behavior. [write]
- `create_project` — Create a Marvin project with scheduling, labels, notes, and priority. [write]
- `create_task` — Create a Marvin task with scheduling, labels, notes, and optional title shortcuts. [write]
- `list_categories` — List all Marvin categories for organizing tasks and projects.
- `list_children` — List open direct child tasks and projects of a category or project; descendants are not expanded.
- `list_done_items` — List tasks and projects completed on a day. Omitted date uses the server's UTC date.
- `list_due_items` — List open tasks and projects due on or before a date. Omitted by uses the server's UTC date.
- `list_labels` — List all Marvin labels in their configured sort order.
- `list_today_items` — List tasks and projects scheduled on a day, including enabled rollover and auto-scheduled due items. Omitted date uses the server's UTC date.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Amazing Marvin state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Amazing Marvin is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/amazing_marvin
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Amazing Marvin homepage: https://amazingmarvin.com/
- API documentation: https://help.amazingmarvin.com/amazing-marvin/api-getting-started
