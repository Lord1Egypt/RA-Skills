---
name: oo-qianfan
description: "Baidu Qianfan (qianfan.cloud.baidu.com). Use this skill for ANY Baidu Qianfan request — reading, creating, updating, and deleting data. Whenever a task involves Baidu Qianfan, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Baidu Qianfan"
  author: "OOMOL"
  version: "1.0.1"
  services: ["qianfan"]
  icon: "https://static.oomol.com/logo/third-party/Qianfan.png"
---

# Baidu Qianfan

Operate **Baidu Qianfan** through your OOMOL-connected account. This skill calls the `qianfan` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Baidu Qianfan. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "qianfan" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "qianfan" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_batch` — Cancel a Baidu Qianfan batch prediction job by its identifier. [write]
- `cancel_video_generation_task` — Cancel a Baidu Qianfan video generation task by its task identifier. [write]
- `create_ai_search_completion` — Create a non-streaming AI search chat completion with Baidu Qianfan. [write]
- `create_air_image_generation` — Generate images with the Baidu Qianfan MuseSteamer Air image endpoint. [write]
- `create_batch` — Create a Baidu Qianfan batch prediction job from an uploaded input file. [write]
- `create_chat_completion` — Create a non-streaming OpenAI-compatible chat completion with Baidu Qianfan. [write]
- `create_completion` — Create a non-streaming fill-in-the-middle completion with Baidu Qianfan. [write]
- `create_embeddings` — Generate embedding vectors for one or more input strings with Baidu Qianfan. [write]
- `create_image_generation` — Generate images with the Baidu Qianfan general image generation endpoint. [write]
- `create_response` — Create a non-streaming stored response with the Baidu Qianfan responses API. [write]
- `create_video_generation_task` — Create a Baidu Qianfan video generation task. [write]
- `delete_response` — Delete a previously stored Baidu Qianfan response by its identifier. [destructive]
- `get_batch` — Fetch a Baidu Qianfan batch prediction job by its identifier.
- `get_file_content` — Fetch the raw content of a Baidu Qianfan file by its identifier.
- `get_response` — Fetch a previously stored Baidu Qianfan response by its identifier.
- `get_video_generation_task` — Fetch a Baidu Qianfan video generation task by its task identifier.
- `list_batches` — List Baidu Qianfan batch prediction jobs with optional pagination.
- `list_files` — List files stored in Baidu Qianfan with optional filters.
- `list_models` — List the models available to the current Baidu Qianfan API key.
- `list_response_input_items` — List the stored context items for a previously created Baidu Qianfan response.
- `list_video_generation_tasks` — List Baidu Qianfan video generation tasks with optional filters.
- `rerank` — Score and rank candidate documents against a query with a Baidu Qianfan rerank model.
- `run_paddleocr_vl` — Run the Baidu Qianfan PaddleOCR-VL endpoint on a document or image.
- `run_pp_structure_v3` — Run the Baidu Qianfan PP-StructureV3 OCR endpoint on a document or image.
- `upload_file` — Upload a file to Baidu Qianfan for batch or other file-based APIs. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Baidu Qianfan state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Baidu Qianfan is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=qianfan
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Baidu Qianfan homepage: https://qianfan.cloud.baidu.com
