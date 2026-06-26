---
name: oo-wit-ai
description: "Wit.ai (wit.ai). Use this skill for ANY Wit.ai request — reading, creating, updating, and deleting data. Whenever a task involves Wit.ai, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Wit.ai"
  author: "OOMOL"
  version: "1.0.1"
  services: ["wit_ai"]
  icon: "https://static.oomol.com/logo/third-party/Wit.ai.svg"
---

# Wit.ai

Operate **Wit.ai** through your OOMOL-connected account. This skill calls the `wit_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Wit.ai. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wit_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wit_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_entity_keyword` — Add a keyword and optional synonyms to an existing Wit.ai entity. [write]
- `add_keyword_synonym` — Add a synonym to a specific keyword on a Wit.ai entity. [write]
- `add_trait_value` — Add a canonical value to an existing Wit.ai trait. [write]
- `analyze_message` — Analyze a text message and return the intents, entities, and traits inferred by Wit.ai.
- `create_entity` — Create a new Wit.ai entity with optional lookups and keywords. [write]
- `create_intent` — Create a new Wit.ai intent for labeling user messages. [write]
- `create_trait` — Create a new Wit.ai trait with one or more canonical values. [write]
- `create_utterances` — Asynchronously enqueue validated utterances for training in Wit.ai. [write]
- `delete_utterances` — Asynchronously delete validated utterances from the current Wit.ai app. [destructive]
- `detect_language` — Detect the most likely locales for a text message using Wit.ai language identification.
- `get_app` — Retrieve details and training status for a specific Wit.ai app.
- `get_entity` — Retrieve a Wit.ai entity including its roles, lookups, and keywords.
- `get_intent` — Retrieve a Wit.ai intent together with the entity bindings it uses.
- `get_trait` — Retrieve a Wit.ai trait together with its configured values.
- `list_apps` — List the Wit.ai apps accessible by the current bearer token.
- `list_entities` — List all entities defined in the current Wit.ai app.
- `list_intents` — List all intents defined in the current Wit.ai app.
- `list_traits` — List all traits defined in the current Wit.ai app.
- `list_utterances` — List validated utterances already stored in the current Wit.ai app.
- `update_entity` — Update a Wit.ai entity by sending the desired end-state definition for its schema and keywords. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Wit.ai state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Wit.ai is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=wit_ai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Wit.ai homepage: https://wit.ai
