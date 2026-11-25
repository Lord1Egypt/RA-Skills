---
name: oo-qwen
description: "Qwen (qwen.ai). Use this skill for ANY Qwen request — reading, creating, updating, and deleting data. Whenever a task involves Qwen, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Qwen"
  author: "OOMOL"
  version: "1.0.7"
  services: ["qwen"]
  icon: "https://static.oomol.com/logo/third-party/qwen.svg"
---

# Qwen

Operate **Qwen** through your OOMOL-connected account. This skill calls the `qwen` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Qwen. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "qwen" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "qwen" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `analyze_document` — Analyze documents or text with Qwen-Doc-Turbo.
- `create_designed_voice` — Create a Qwen-Audio custom voice from a text description. [write]
- `create_voice_clone` — Create a Qwen-Audio custom voice from a public audio sample. [write]
- `delete_custom_voice` — Delete one Qwen-Audio cloned or designed voice. [destructive]
- `extract_text` — Extract text and structured information from an image with Qwen3.5-OCR.
- `generate_image` — Generate or edit images with the Qwen Image 3.0 family. [write]
- `generate_speech` — Generate speech with Qwen-Audio TTS. [write]
- `get_custom_voice` — Get one Qwen-Audio cloned or designed voice.
- `get_image_translation` — Retrieve a Qwen image translation task state and output.
- `get_speech_recognition` — Retrieve a Qwen-Audio transcription task and its normalized result.
- `list_custom_voices` — List Qwen-Audio cloned and designed voices together.
- `submit_image_translation` — Submit an asynchronous Qwen image translation task. [write]
- `submit_speech_recognition` — Submit a Qwen-Audio asynchronous audio or video transcription task. [write]
- `translate_text` — Translate text with Qwen-MT and optional terminology, translation memory, and domain guidance.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Qwen state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Qwen is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/qwen
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Qwen homepage: https://qwen.ai/
- API documentation: https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api
