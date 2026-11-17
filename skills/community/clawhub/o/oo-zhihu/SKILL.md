---
name: oo-zhihu
description: "Zhihu (zhihu.com). Use this skill for ANY Zhihu request — reading, creating, and updating data. Whenever a task involves Zhihu, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zhihu"
  author: "OOMOL"
  version: "1.0.6"
  services: ["zhihu"]
  icon: "https://static.oomol.com/logo/third-party/zhihu.svg"
---

# Zhihu

Operate **Zhihu** through your OOMOL-connected account. This skill calls the `zhihu` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zhihu. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zhihu" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zhihu" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `favlist_contents` — List public content in one collection owned by the current Access Secret account.
- `get_pdf_parse` — Get the status and temporary result URL for a Zhihu PDF parsing task.
- `get_ppt_generation` — Get the status and temporary PPTX download URL for a PPT generation task.
- `global_search` — Search the global web index exposed by Zhihu Open Platform.
- `hot_list` — Get the current Zhihu hot list with titles, links, thumbnails, and summaries.
- `knowledge_base_items` — List content in a Zhida knowledge base using cursor pagination.
- `knowledge_bases` — List Zhida knowledge bases created by or subscribed to by the current account.
- `knowledge_file_upload` — Download a file from an HTTP URL and upload it into a Zhida knowledge base. [write]
- `knowledge_search` — Retrieve relevant document fragments from Zhida knowledge bases with RAG search.
- `submit_pdf_parse` — Download a PDF from an HTTP URL, upload it to Zhihu, and submit an asynchronous parse task. [write]
- `submit_ppt_generation` — Submit a Zhihu answer or article URL for asynchronous PPTX generation. [write]
- `user_collections` — List the current Access Secret owner's recently favorited public content.
- `user_contents` — List the current Access Secret owner's public Zhihu creations.
- `user_favlists` — List the current Access Secret owner's public Zhihu collections.
- `user_followees` — List the current Access Secret owner's public Zhihu followees.
- `zhida` — Create a non-streaming Zhihu Zhida chat completion. [write]
- `zhihu_search` — Search Zhihu content and return matching questions, answers, and articles.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zhihu state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zhihu is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zhihu
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zhihu homepage: https://www.zhihu.com
