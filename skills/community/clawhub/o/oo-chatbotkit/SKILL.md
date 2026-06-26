---
name: oo-chatbotkit
description: "ChatBotKit (chatbotkit.com). Use this skill for ANY ChatBotKit request — reading, creating, and updating data. Whenever a task involves ChatBotKit, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ChatBotKit"
  author: "OOMOL"
  version: "1.0.1"
  services: ["chatbotkit"]
  icon: "https://static.oomol.com/logo/third-party/Chatbotkit.svg"
---

# ChatBotKit

Operate **ChatBotKit** through your OOMOL-connected account. This skill calls the `chatbotkit` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ChatBotKit. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chatbotkit" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chatbotkit" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `attach_dataset_file` — Attach an existing ChatBotKit file to a dataset.
- `complete_conversation` — Send a message to a ChatBotKit conversation and receive the next assistant reply. [write]
- `create_bot` — Create a new ChatBotKit bot. [write]
- `create_conversation` — Create a new ChatBotKit conversation with either a bot reference or inline bot configuration. [write]
- `create_conversation_message` — Append a message to an existing ChatBotKit conversation. [write]
- `create_dataset` — Create a new ChatBotKit dataset for knowledge retrieval. [write]
- `create_dataset_record` — Create a new record inside a ChatBotKit dataset. [write]
- `create_file` — Create a new ChatBotKit file resource. [write]
- `detach_dataset_file` — Detach a ChatBotKit file from a dataset.
- `download_file` — Fetch the download URL for an existing ChatBotKit file.
- `fetch_bot` — Fetch a single ChatBotKit bot by ID.
- `fetch_conversation` — Fetch a single ChatBotKit conversation by ID.
- `fetch_dataset` — Fetch a single ChatBotKit dataset by ID.
- `fetch_file` — Fetch a single ChatBotKit file by ID.
- `fetch_usage` — Fetch account-wide ChatBotKit usage statistics for tokens, conversations, messages, and database resources.
- `list_bots` — List ChatBotKit bots with optional pagination and metadata filtering.
- `list_conversation_messages` — List messages inside a ChatBotKit conversation.
- `list_conversations` — List ChatBotKit conversations with optional pagination and metadata filtering.
- `list_dataset_files` — List files attached to a ChatBotKit dataset.
- `list_dataset_records` — List records inside a ChatBotKit dataset.
- `list_datasets` — List ChatBotKit datasets with optional pagination and metadata filtering.
- `list_files` — List ChatBotKit files with optional pagination and metadata filtering.
- `search_dataset` — Run semantic search against a ChatBotKit dataset.
- `sync_file` — Trigger synchronization for an existing ChatBotKit file. [write]
- `update_bot` — Update an existing ChatBotKit bot. [write]
- `update_dataset` — Update an existing ChatBotKit dataset. [write]
- `upload_file` — Upload content to an existing ChatBotKit file using the official JSON upload modes. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ChatBotKit state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ChatBotKit is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=chatbotkit
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ChatBotKit homepage: https://chatbotkit.com
