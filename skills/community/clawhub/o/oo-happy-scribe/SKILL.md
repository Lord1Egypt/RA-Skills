---
name: oo-happy-scribe
description: "Happy Scribe (happyscribe.com). Use this skill for ANY Happy Scribe request — reading, creating, updating, and deleting data. Whenever a task involves Happy Scribe, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Happy Scribe"
  author: "OOMOL"
  version: "1.0.6"
  services: ["happy_scribe"]
  icon: "https://static.oomol.com/logo/third-party/happy_scribe.svg"
---

# Happy Scribe

Operate **Happy Scribe** through your OOMOL-connected account. This skill calls the `happy_scribe` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Happy Scribe. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "happy_scribe" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "happy_scribe" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `confirm_order` — Confirm a previously created Happy Scribe order so processing can begin. [write]
- `create_export` — Create an asynchronous export for one or more Happy Scribe transcriptions. [write]
- `create_transcription_order` — Submit a transcription or subtitling order from a public media URL. [write]
- `create_translation_order` — Submit a translation order for an existing Happy Scribe transcription. [write]
- `delete_transcription` — Delete one Happy Scribe transcription by ID. [destructive]
- `get_export` — Get the state and download link of a Happy Scribe export.
- `get_order` — Get the current state and details of a Happy Scribe order.
- `get_transcription` — Get one Happy Scribe transcription by ID.
- `list_organizations` — List the Happy Scribe organizations available to the current API key.
- `list_transcriptions` — List transcriptions in a Happy Scribe organization.
- `update_transcription` — Update editable fields on a Happy Scribe transcription. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Happy Scribe state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Happy Scribe is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/happy_scribe
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Happy Scribe homepage: https://www.happyscribe.com/
- API documentation: https://dev.happyscribe.com/sections/general/
