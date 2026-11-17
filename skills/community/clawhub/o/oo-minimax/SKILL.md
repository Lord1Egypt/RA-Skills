---
name: oo-minimax
description: "MiniMax (minimax.io). Use this skill for ANY MiniMax request — reading, creating, updating, and deleting data. Whenever a task involves MiniMax, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "MiniMax"
  author: "OOMOL"
  version: "1.0.7"
  services: ["minimax"]
  icon: "https://static.oomol.com/logo/third-party/minimax.svg"
---

# MiniMax

Operate **MiniMax** through your OOMOL-connected account. This skill calls the `minimax` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected MiniMax. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "minimax" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "minimax" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_response` — Create a non-streaming MiniMax response using the OpenAI Responses API shape. [write]
- `create_video_generation_v2` — Create a MiniMax H3 video generation task with text, image, video, or audio content. [write]
- `delete_video_generation_v2` — Delete a MiniMax H3 video generation task. [destructive]
- `download_video` — Download a generated MiniMax video and store it in connector transit storage.
- `estimate_input_tokens` — Estimate MiniMax response input tokens without invoking the model.
- `image_to_video` — Create a MiniMax asynchronous image-to-video task from a public URL or data URI first frame. [write]
- `list_models` — List OpenAI-compatible MiniMax models available to the API key.
- `list_video_generation_v2` — List MiniMax H3 video generation tasks.
- `query_video_generation` — Query a MiniMax video generation task and return its status and file identifier.
- `query_video_generation_v2` — Query a MiniMax H3 video generation task.
- `retrieve_model` — Retrieve OpenAI-compatible metadata for one MiniMax model.
- `text_to_audio` — Synthesize text into audio with the MiniMax T2A v2 API. [write]
- `text_to_video` — Create a MiniMax asynchronous text-to-video generation task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change MiniMax state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — MiniMax is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/minimax
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- MiniMax homepage: https://www.minimax.io
- API documentation: https://platform.minimax.io/docs/api-reference/api-overview
