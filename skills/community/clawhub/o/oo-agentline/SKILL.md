---
name: oo-agentline
description: "AgentLine (agentline.cloud). Use this skill for ANY AgentLine request — reading, creating, updating, and deleting data. Whenever a task involves AgentLine, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AgentLine"
  author: "OOMOL"
  version: "1.0.1"
  services: ["agentline"]
  icon: "https://static.oomol.com/logo/third-party/agentline.png"
---

# AgentLine

Operate **AgentLine** through your OOMOL-connected account. This skill calls the `agentline` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AgentLine. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "agentline" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "agentline" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_agent` — Create a voice agent with default instructions, greeting, voice and owner phone. [write]
- `create_contact` — Save a contact for an agent. Each phone number can appear once per agent; duplicates return HTTP 409. [write]
- `delete_agent` — Permanently delete an agent and its calls, transcripts, messages, contacts and webhook. Assigned numbers are detached but remain active on the account. [destructive]
- `delete_contact` — Permanently delete a contact. Calls, messages and transcripts with that number are unaffected. [destructive]
- `get_account_voice` — Read the account default voice and its resolved voice UUID.
- `get_agent` — Get a voice agent's full configuration.
- `get_contact` — Get one contact from an agent's contact list.
- `list_agents` — List all voice agents configured on the account.
- `list_contacts` — List contacts sorted by name. Advance offset by limit until it reaches total to retrieve further pages.
- `list_voices` — List available voice presets and IDs for agent and account configuration.
- `reset_account_voice` — Reset the account voice setting to the system default for future calls. [write]
- `set_account_voice` — Set the default voice for future calls unless overridden by the agent or call. [write]
- `update_agent` — Update a voice agent for future calls. Omitted fields retain their values; active calls are unaffected. [write]
- `update_contact` — Update contact fields. Omit a field to retain it; set label to null or an empty string to clear it. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AgentLine state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AgentLine is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/agentline
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- AgentLine homepage: https://agentline.cloud
- API documentation: https://docs.agentline.cloud/introduction
