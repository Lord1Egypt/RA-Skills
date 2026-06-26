---
name: oo-jimeng-ai
description: "Jimeng AI (volcengine.com). Use this skill for ANY Jimeng AI request — reading, creating, and updating data. Whenever a task involves Jimeng AI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Jimeng AI"
  author: "OOMOL"
  version: "1.0.1"
  services: ["jimeng_ai"]
  icon: "https://static.oomol.com/logo/third-party/jimeng_ai.png"
---

# Jimeng AI

Operate **Jimeng AI** through your OOMOL-connected account. This skill calls the `jimeng_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Jimeng AI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "jimeng_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "jimeng_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_image_generation_4_0_result` — Get the result of a Jimeng AI Image Generation 4.0 async task.
- `get_image_generation_4_6_result` — Get the result of a Jimeng AI Image Generation 4.6 async task.
- `get_marketing_video_agent_result` — Get the result of a Lilinque Marketing Video Agent async task.
- `get_smart_upscale_result` — Get the result of a Jimeng AI Smart Upscale async task.
- `get_smart_video_agent_1_0_result` — Get the result of a Lilinque Smart Video Agent 1.0 async task.
- `get_smart_video_agent_2_0_with_reference_result` — Get the result of a Lilinque Smart Video Agent 2.0 async task with reference videos.
- `get_smart_video_agent_2_0_without_reference_result` — Get the result of a Lilinque Smart Video Agent 2.0 async task without reference videos.
- `get_text_to_image_3_0_result` — Get the result of a Jimeng Text-to-Image 3.0 async task.
- `get_text_to_image_3_1_result` — Get the result of a Jimeng Text-to-Image 3.1 async task.
- `get_video_generation_3_0_1080p_result` — Get the result of a Jimeng AI Video Generation 3.0 1080P async task.
- `get_video_generation_3_0_720p_result` — Get the result of a Jimeng AI Video Generation 3.0 720P async task.
- `get_video_generation_3_0_pro_result` — Get the result of a Jimeng AI Video Generation 3.0 Pro async task.
- `submit_image_generation_4_0` — Submit a Jimeng AI Image Generation 4.0 async task. [write]
- `submit_image_generation_4_6` — Submit a Jimeng AI Image Generation 4.6 async task. [write]
- `submit_image_to_video_first_frame_3_0_1080p` — Submit a Jimeng AI Video Generation 3.0 1080P image-to-video first-frame async task. [write]
- `submit_image_to_video_first_frame_3_0_720p` — Submit a Jimeng AI Video Generation 3.0 720P image-to-video first-frame async task. [write]
- `submit_image_to_video_first_tail_frame_3_0_1080p` — Submit a Jimeng AI Video Generation 3.0 1080P image-to-video first-and-last-frame async task. [write]
- `submit_image_to_video_first_tail_frame_3_0_720p` — Submit a Jimeng AI Video Generation 3.0 720P image-to-video first-and-last-frame async task. [write]
- `submit_marketing_video_agent` — Submit a Lilinque Marketing Video Agent async task. [write]
- `submit_smart_upscale` — Submit a Jimeng AI Smart Upscale async task. [write]
- `submit_smart_video_agent_1_0` — Submit a Lilinque Smart Video Agent 1.0 async task. [write]
- `submit_smart_video_agent_2_0_with_reference` — Submit a Lilinque Smart Video Agent 2.0 async task with reference videos. [write]
- `submit_smart_video_agent_2_0_without_reference` — Submit a Lilinque Smart Video Agent 2.0 async task without reference videos. [write]
- `submit_text_to_image_3_0` — Submit a Jimeng Text-to-Image 3.0 async task. [write]
- `submit_text_to_image_3_1` — Submit a Jimeng Text-to-Image 3.1 async task. [write]
- `submit_video_generation_3_0_1080p` — Submit a Jimeng AI Video Generation 3.0 1080P async task. [write]
- `submit_video_generation_3_0_720p` — Submit a Jimeng AI Video Generation 3.0 720P async task. [write]
- `submit_video_generation_3_0_pro` — Submit a Jimeng AI Video Generation 3.0 Pro async task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Jimeng AI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Jimeng AI is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=jimeng_ai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Jimeng AI homepage: https://www.volcengine.com/product/jimeng
