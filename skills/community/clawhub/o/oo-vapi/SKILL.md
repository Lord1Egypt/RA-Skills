---
name: oo-vapi
description: "Vapi (vapi.ai). Use this skill for ANY Vapi request — reading, creating, updating, and deleting data. Whenever a task involves Vapi, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Vapi"
  author: "OOMOL"
  version: "1.0.1"
  services: ["vapi"]
  icon: "https://static.oomol.com/logo/third-party/Vapi.svg"
---

# Vapi

Operate **Vapi** through your OOMOL-connected account. This skill calls the `vapi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Vapi. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "vapi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "vapi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_analytics_query` — Create and execute one or more Vapi analytics queries across call and subscription data. [write]
- `create_assistant` — Create a new Vapi assistant with required transcriber, voice, and model settings plus optional messaging and duration controls. [write]
- `create_eval` — Create a Vapi eval for a mock conversation and define the checkpoint messages used to evaluate model behavior. [write]
- `create_openai_chat` — Create an OpenAI-compatible Vapi chat response using an assistant or squad, with optional session and transport settings. [write]
- `create_phone_number` — Create a Vapi phone number using Vapi, Twilio, Vonage, Telnyx, or bring-your-own provider settings. [write]
- `create_policy` — Create a Vapi monitoring policy with severity, threshold, and schedule or interval configuration. [write]
- `create_provider_resource` — Create a pronunciation dictionary provider resource in Vapi, defaulting to the 11labs pronunciation-dictionary route used by the upstream toolkit. [write]
- `create_scorecard` — Create a Vapi scorecard for observability and evaluation using structured output metrics and conditions. [write]
- `create_session` — Create a Vapi session with either an assistant identifier or an inline assistant configuration. [write]
- `delete_call` — Delete a Vapi call by its unique identifier. [destructive]
- `delete_chat` — Delete a Vapi chat by its unique identifier. [destructive]
- `delete_eval` — Delete a Vapi eval by its unique identifier. [destructive]
- `delete_eval_run` — Delete a Vapi eval run by its unique identifier. [destructive]
- `delete_phone_number` — Delete a Vapi phone number by its unique identifier. [destructive]
- `get_assistant` — Retrieve a Vapi assistant by its unique identifier.
- `get_call` — Retrieve a single Vapi call by its unique identifier.
- `get_chat` — Retrieve a Vapi chat by its unique identifier.
- `get_eval` — Retrieve a Vapi eval by its unique identifier.
- `get_file` — Retrieve Vapi file metadata by file identifier.
- `get_tool` — Retrieve a Vapi tool by its unique identifier.
- `list_assistants` — List Vapi assistants with optional created/updated timestamp filters and a configurable page size.
- `list_calls` — List Vapi calls with optional filtering by call, assistant, phone number, and created or updated timestamps.
- `list_chats` — List Vapi chats with pagination plus optional assistant, squad, session, previous chat, and timestamp filters.
- `list_evals` — List Vapi evals with pagination plus optional identifier and timestamp-based filters.
- `list_insights` — List Vapi insights with pagination plus optional identifier and timestamp filters.
- `list_monitoring_policies` — List Vapi monitoring policies with optional severity, monitor, and timestamp filters.
- `list_phone_numbers` — List Vapi phone numbers with optional created and updated timestamp filters.
- `list_provider_resources` — List Vapi provider resources for a provider and resource type with optional identifier and timestamp filters.
- `list_scorecards` — List Vapi scorecards with pagination plus optional identifier and timestamp filters.
- `list_sessions` — List Vapi sessions with pagination plus optional identifier, name, assistant, workflow, squad, and timestamp filters.
- `list_structured_outputs` — List Vapi structured outputs with pagination plus optional identifier, name, and timestamp filters.
- `test_code_tool_execution` — Execute TypeScript code inside Vapi's code tool sandbox and return the logs, result, and execution outcome.
- `update_assistant` — Update an existing Vapi assistant and keep only the fields that should change in the request body. [write]
- `update_eval` — Update a Vapi eval and keep only the fields that should change in the request body. [write]
- `update_insight` — Update a Vapi insight by replacing its name, queries, formulas, grouping, and time range settings. [write]
- `update_phone_number` — Update a Vapi phone number and keep only the fields that should change in the request body. [write]
- `update_tool` — Update a Vapi tool configuration, including function definitions, HTTP request settings, and retry policies. [write]
- `upload_file` — Upload a file to Vapi knowledge storage from a public URL or base64 payload and return the resulting file metadata. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Vapi state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Vapi is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=vapi
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Vapi homepage: https://vapi.ai
