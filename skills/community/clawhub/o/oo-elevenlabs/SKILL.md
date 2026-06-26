---
name: oo-elevenlabs
description: "ElevenLabs (elevenlabs.io). Use this skill for ANY ElevenLabs request — reading, creating, updating, and deleting data. Whenever a task involves ElevenLabs, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ElevenLabs"
  author: "OOMOL"
  version: "1.0.2"
  services: ["elevenlabs"]
  icon: "https://static.oomol.com/logo/third-party/ElevenLabs.svg"
---

# ElevenLabs

Operate **ElevenLabs** through your OOMOL-connected account. This skill calls the `elevenlabs` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ElevenLabs. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "elevenlabs" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "elevenlabs" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_sound_effect` — Generate a sound effect from a text prompt and upload the binary audio result to connector transit storage. [write]
- `delete_history_item` — Delete one ElevenLabs history item by history item ID. [destructive]
- `get_audio_from_history_item` — Download the audio for one ElevenLabs history item and upload the binary result to connector transit storage.
- `get_generated_items` — List generated ElevenLabs history items with pagination and optional voice filtering.
- `get_history_item_by_id` — Get one ElevenLabs history item by history item ID without downloading its audio.
- `get_models` — List the available ElevenLabs models and their text-to-speech capabilities.
- `get_user_info` — Get the current ElevenLabs user profile together with the embedded subscription snapshot.
- `get_user_subscription_info` — Get the current ElevenLabs subscription details for the authenticated user.
- `get_voice` — Get one ElevenLabs voice by voice ID, with optional settings included.
- `get_voice_settings` — Get the synthesis settings configured for one ElevenLabs voice.
- `get_voices` — List the available ElevenLabs voices with their key metadata and settings.
- `search_voices` — Search ElevenLabs voices with v2 pagination, filtering, sorting, and optional total count.
- `text_to_speech` — Generate speech audio from text by calling ElevenLabs text-to-speech and uploading the binary result to connector transit storage.
- `text_to_speech_with_timestamps` — Generate speech audio with character-level timing, upload the audio to connector transit storage, and return timing metadata.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ElevenLabs state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ElevenLabs is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=elevenlabs
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ElevenLabs homepage: https://elevenlabs.io
