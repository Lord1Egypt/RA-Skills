---
name: oo-ima
description: "ima (ima.qq.com). Use this skill for ANY ima request — reading, creating, and updating data. Whenever a task involves ima, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ima"
  author: "OOMOL"
  version: "1.0.2"
  services: ["ima"]
  icon: "https://static.oomol.com/logo/third-party/ima.svg"
---

# ima

Operate **ima** through your OOMOL-connected account. This skill calls the `ima` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ima. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ima" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ima" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_note_to_knowledge_base` — Add an existing IMA note into one IMA knowledge base. [write]
- `append_note` — Append Markdown content to an existing IMA note.
- `check_repeated_names` — Check whether file names already exist in an IMA knowledge-base folder.
- `create_note` — Create a new IMA note from Markdown content. [write]
- `get_knowledge_bases` — Fetch metadata for one or more IMA knowledge bases.
- `get_knowledge_item_original` — Fetch access information for a knowledge-base item and download URL-backed original content through file transit when available.
- `get_media_info` — Get IMA knowledge-base media access information for one media item.
- `get_note_content` — Fetch the plain-text or JSON content for one IMA note.
- `import_urls` — Import webpages or WeChat article URLs into one IMA knowledge base. [write]
- `list_addable_knowledge_bases` — List the IMA knowledge bases that accept new content.
- `list_knowledge_items` — List files and folders inside one IMA knowledge-base folder.
- `list_notebooks` — List IMA note folders for the connected account.
- `list_notes` — List notes in one IMA notebook or across all notes.
- `search_knowledge_bases` — Search IMA knowledge bases by name, or pass an empty query to list accessible knowledge bases.
- `search_knowledge_items` — Search files and folders inside one IMA knowledge base.
- `search_notes` — Search IMA notes by title or note body text.
- `upload_file_to_knowledge_base` — Upload a file from an HTTP URL into one IMA knowledge base, including duplicate checks, COS upload, and add_knowledge. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ima state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ima is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=ima
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ima homepage: https://ima.qq.com
