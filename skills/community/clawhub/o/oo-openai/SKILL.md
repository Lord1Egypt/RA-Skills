---
name: oo-openai
description: "OpenAI (openai.com). Use this skill for ANY OpenAI request — reading, creating, and updating data. Whenever a task involves OpenAI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OpenAI"
  author: "OOMOL"
  version: "1.0.1"
  services: ["openai"]
  icon: "https://static.oomol.com/logo/third-party/OpenAI.svg"
---

# OpenAI

Operate **OpenAI** through your OOMOL-connected account. This skill calls the `openai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected OpenAI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "openai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "openai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_batch` — Cancel one OpenAI batch job by its identifier. [write]
- `create_audio_transcription` — Transcribe one uploaded audio file with the OpenAI audio transcription API. [write]
- `create_audio_translation` — Translate one uploaded audio file into English with the OpenAI audio translation API. [write]
- `create_batch` — Create an OpenAI batch job from an uploaded input file. [write]
- `create_embeddings` — Create embeddings with an OpenAI embedding model. [write]
- `create_image` — Generate images with the OpenAI image generation API. [write]
- `create_moderation` — Classify text or image inputs with the OpenAI Moderations API. [write]
- `create_response` — Create a non-streaming OpenAI response through the Responses API. [write]
- `create_speech` — Synthesize speech audio from text with the OpenAI audio speech API. [write]
- `get_batch` — Fetch one OpenAI batch job by its identifier.
- `get_input_token_counts` — Count how many input tokens a Responses-style OpenAI request would consume.
- `get_model` — Retrieve the metadata for a single OpenAI model by ID.
- `get_response` — Retrieve one stored OpenAI response by its identifier.
- `list_input_items` — List the stored input items for one OpenAI response.
- `list_models` — List the OpenAI models available to the current API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OpenAI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — OpenAI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=openai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OpenAI homepage: https://openai.com/api/
