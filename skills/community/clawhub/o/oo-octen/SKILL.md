---
name: oo-octen
description: "Octen (octen.ai). Use this skill for ANY Octen request — reading, creating, and updating data. Whenever a task involves Octen, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Octen"
  author: "OOMOL"
  version: "1.0.2"
  services: ["octen"]
  icon: "https://static.oomol.com/logo/third-party/octen.svg"
---

# Octen

Operate **Octen** through your OOMOL-connected account. This skill calls the `octen` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Octen. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "octen" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "octen" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `answer` — Generate a grounded answer with citations from live search. Returns the complete response.
- `broad_search` — Decompose a question into concurrent web searches and return the combined results.
- `chat` — Run an OpenAI-compatible model conversation with tools and optional live web search. Returns the complete non-streaming response.
- `embed_multimodal` — Embed text, images and video into a shared vector space, optionally fusing inputs.
- `embed_text` — Create semantic vectors for text queries or documents.
- `extract` — Extract clean text or Markdown and media from URLs, preserving per-URL failures.
- `generate_grounded` — Start image or video generation grounded in live web references; wait with get_grounded_generation. [write]
- `generate_images` — Generate or edit images, downloading reference image URLs and returning temporary file URLs instead of base64.
- `generate_video` — Start video generation from text and optional reference images; wait with get_video. [write]
- `get_grounded_generation` — Read grounded generation status, result URL and source references.
- `get_video` — Read a video generation task and its signed download URL when completed.
- `messages` — Run an Anthropic-compatible model conversation with tools, thinking and optional live web search. Returns the complete response.
- `research` — Research a question and collect the SSE report and evidence as JSON. May return a plan requiring caller selections; resume with plan_id and selections.
- `search` — Search the live web with domain, time, language, highlight and full-content options.
- `search_business` — Search business news and retrieve company and person entity cards.
- `search_images` — Search images by text or reference image, with domain and safe-search filters.
- `search_news` — Search recent news and optionally group related coverage into subjects.
- `search_videos` — Search videos by text. Requires Octen invite-only beta access.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Octen state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Octen is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/octen
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Octen homepage: https://octen.ai
- API documentation: https://docs.octen.ai/overview/quickstart
