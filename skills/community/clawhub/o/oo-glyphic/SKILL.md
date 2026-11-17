---
name: oo-glyphic
description: "Glyphic (goairspeed.com). Use this skill for ANY Glyphic request — searching and reading data. Whenever a task involves Glyphic, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Glyphic"
  author: "OOMOL"
  version: "1.0.5"
  services: ["glyphic"]
  icon: "https://static.oomol.com/logo/third-party/glyphic.svg"
---

# Glyphic

Operate **Glyphic** through your OOMOL-connected account. This skill calls the `glyphic` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Glyphic. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "glyphic" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "glyphic" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_call` — Retrieve one Glyphic call by ID, including transcript, summary, media, and insights.
- `get_call_media` — Retrieve presigned media URL metadata for a Glyphic call.
- `get_call_snippets` — Retrieve snippets for a Glyphic call, including time ranges and transcript turns.
- `get_playbook` — Retrieve a Glyphic playbook by ID, including the latest version content.
- `get_playbook_version` — Retrieve a specific Glyphic playbook version by playbook ID and version ID.
- `list_call_tags` — List all Glyphic call tags for the organization.
- `list_calls` — List public Glyphic calls with optional participant, time, title, tag, and cursor filters.
- `list_playbook_versions` — List versions for a Glyphic playbook.
- `list_playbooks` — List Glyphic playbooks with cursor pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Glyphic state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Glyphic is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/glyphic
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Glyphic homepage: https://www.goairspeed.com
- API documentation: https://docs.glyphic.ai/articles/7806662155-glyphic-api
