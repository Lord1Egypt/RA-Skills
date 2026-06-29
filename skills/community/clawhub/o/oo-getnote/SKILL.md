---
name: oo-getnote
description: "Get 笔记 (biji.com). Use this skill for ANY Get 笔记 request — reading, creating, updating, and deleting data. Whenever a task involves Get 笔记, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Get 笔记"
  author: "OOMOL"
  version: "1.0.0"
  services: ["getnote"]
---

# Get 笔记

Operate **Get 笔记** through your OOMOL-connected account. This skill calls the `getnote` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Get 笔记. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "getnote" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "getnote" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_note_tags` — Add one or more tags to a Getnote note. [write]
- `add_notes_to_knowledge_base` — Add up to 20 notes to one Getnote knowledge base. Subscribed knowledge bases are read-only unless the user is an admin. [write]
- `create_knowledge_base` — Create a Getnote knowledge base. Upstream limits creation to 50 per day. [write]
- `delete_note` — Move a Getnote note to trash. [destructive]
- `follow_live` — Subscribe a Dedao live channel link into one Getnote knowledge base. Upstream currently supports Dedao App live links. [write]
- `get_blogger_content` — Get one Getnote blogger content detail, including original text when returned.
- `get_live_detail` — Get one Getnote live detail, including AI summary and transcript when returned.
- `get_note` — Get one Getnote note detail, including fields that are not present in lists.
- `get_save_task` — Check the progress of an asynchronous Getnote link or image save task. [write]
- `list_blogger_contents` — List content items for a subscribed blogger in a Getnote knowledge base.
- `list_knowledge_base_bloggers` — List bloggers subscribed in one Getnote knowledge base.
- `list_knowledge_base_lives` — List completed live sessions in one Getnote knowledge base.
- `list_knowledge_base_notes` — List notes in one Getnote knowledge base.
- `list_knowledge_bases` — List knowledge bases owned by the authenticated Getnote account.
- `list_note_tags` — List tags attached to one Getnote note.
- `list_notes` — List recent Getnote notes using the official cursor pagination endpoint.
- `list_subscribed_knowledge_bases` — List knowledge bases subscribed by the authenticated Getnote account. These are read-only unless the user is an admin.
- `remove_note_tag` — Remove one Getnote tag by tag ID. System tags cannot be deleted upstream. [destructive]
- `remove_notes_from_knowledge_base` — Remove notes from one Getnote knowledge base. [destructive]
- `save_note` — Save a plain-text, link, or image-URL note to Getnote. Plain text and Getnote share links are synchronous; regular links and image notes may return tasks. [write]
- `search_notes` — Run Getnote semantic search globally, or within one knowledge base when topicId is provided.
- `share_note` — Generate or retrieve the idempotent public share link for a Getnote note. [write]
- `update_note` — Update a Getnote note title, plain-text content, or tags. Tags replace the existing tag list. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Get 笔记 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Get 笔记 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=getnote
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Get 笔记 homepage: https://www.biji.com/
