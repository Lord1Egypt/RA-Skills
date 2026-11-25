---
name: oo-oomol-rag
description: "OOMOL RAG (knowledge-base.oomol.com). Use this skill for ANY OOMOL RAG request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL RAG, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OOMOL RAG"
  author: "OOMOL"
  version: "1.0.4"
  services: ["oomol_rag"]
  icon: "https://static.oomol.com/logo/third-party/oomol_rag.svg"
---

# OOMOL RAG

Operate **OOMOL RAG** through your OOMOL-connected account. This skill calls the `oomol_rag` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

OOMOL RAG needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "oomol_rag" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "oomol_rag" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

### Choose the shortest workflow

Use `retrieve` immediately when the knowledge base already contains the source material. There is no need to list files first.

```bash
oo connector run "oomol_rag" \
  --action "retrieve" \
  --data '{"query":"How do I deploy this project?","topK":5}' \
  --json
```

Use these action paths for other tasks:

- Add knowledge: `upload_file` -> `wait_for_file_ready` -> `retrieve`.
- Inspect sources: `list_files` to discover file IDs, then `get_file` for one file.
- Export a source: `download_file` returns a temporary public URL.
- Remove a source: `delete_file` -> `wait_for_file_deleted`. Confirm deletion with the user before starting it.

`upload_file` accepts a publicly reachable HTTP or HTTPS URL, not a local path. Keep the returned `file.id`; the wait, download, and delete actions use it as `fileId`.

The wait actions return the current state; one call does not block until completion. Repeat the same call about every 15 seconds. For ingestion, continue only when `file.status` is `ready`, and stop on `failed`, `uncertain`, `deleting`, or `deleted`. For deletion, continue until `file.status` is `deleted`, and stop on `failed` or `uncertain`.

```bash
oo connector run "oomol_rag" \
  --action "upload_file" \
  --data '{"fileUrl":"https://example.com/handbook.pdf","filename":"handbook.pdf"}' \
  --json

# Repeat about every 15 seconds until file.status is "ready".
oo connector run "oomol_rag" \
  --action "wait_for_file_ready" \
  --data '{"fileId":"<file.id from upload_file>"}' \
  --json

oo connector run "oomol_rag" \
  --action "retrieve" \
  --data '{"query":"What is the expense approval process?"}' \
  --json
```

For file administration, start with a paginated listing. Pass each non-empty `nextCursor` unchanged as the next request's `cursor`; stop when `nextCursor` is an empty string.

```bash
oo connector run "oomol_rag" \
  --action "list_files" \
  --data '{"limit":50}' \
  --json

oo connector run "oomol_rag" \
  --action "list_files" \
  --data '{"cursor":"<nextCursor from the previous response>","limit":50}' \
  --json

oo connector run "oomol_rag" \
  --action "download_file" \
  --data '{"fileId":"<file.id from list_files>"}' \
  --json
```

### Create or edit an editable knowledge article

Use `create_article` -> `save_article_draft` -> `get_article`. Stop at a draft unless the user also requested publishing. When requested, use `publish_article` -> `wait_for_article_ready`.

Generate a UUIDv7 once per creation intent and pass it as `articleId`. Generate distinct stable `saveId` and `publishId` values for each save and publication. After a network failure, retry with the identical ID and payload; do not generate another ID or silently overwrite a concurrent edit.

For `save_article_draft`, use the returned `revision`, a `title`, and native BlockNote content:

```json
{
  "articleId": "<stable article ID>",
  "revision": 1,
  "saveId": "<stable save ID>",
  "title": "Example article",
  "content": {
    "type": "blocknote",
    "blocks": [
      {
        "id": "intro",
        "type": "paragraph",
        "content": [{ "type": "text", "text": "Article text", "styles": {} }],
        "children": []
      }
    ]
  }
}
```

Use `--data @draft.json` for document bodies. For Markdown input, use `create_article_from_markdown` or `save_article_markdown`; `content` remains native BlockNote JSON. On an existing article, read it first, check `formatVersion`, and preserve its block structure and IDs. Do not reinterpret legacy editor JSON as BlockNote.

On 409, fetch the latest article and reconcile changes before saving a new operation. Publication uses the saved `revision` and a stable `publishId`. Poll about every 15 seconds; stop on `failed` or `uncertain`. `ready` means `syncRevision` is indexed: a newer draft may exist, so compare `syncRevision` to the revision you published. An uncertain synchronization outcome requires investigation, not a fresh publication ID.

`list_articles` returns metadata and a `nextCursor`; `get_article` returns the full body. `delete_article` removes the editable article and excludes its index from retrieval while preserving the original converted file. Delete only when requested by the user.

### Write directly from Markdown

Use `create_article_from_markdown` with `articleId`, `saveId`, `title`, and `markdown` to create a draft in one connector action. Creation and saving are separate API requests: conversion is validated before creation, but a later save failure may leave an empty draft. Retry the same article ID, save ID and exact payload to resume; do not generate another article ID. An existing edited article is protected by revision checking.

Use `save_article_markdown` with `articleId`, the latest `revision`, a new stable `saveId`, `title`, and `markdown` to **replace the entire body**. This is not append or patch. Blocks and images absent from the Markdown are removed from the draft. An empty Markdown string clears the body. Preserve leading spaces for indented code, and use JSON `@file` input for multiline source. For precise edits to existing BlockNote blocks or private assets, use the native `save_article_draft` action instead.

```json
{
  "articleId": "<stable article ID>",
  "saveId": "<stable save ID>",
  "title": "Markdown guide",
  "markdown": "# Guide\n\n- First step\n- [x] Finished\n\n**Important:** save before publishing."
}
```

Supported: headings 1–6, paragraphs, bold/italic/strikethrough, inline and fenced/indented code, links and reference links, ordered/nested/task lists, blockquotes, GFM tables and horizontal rules. Standalone HTTP(S) images become image blocks; inline images become links with a warning. HTML and unsupported/relative URLs remain literal text; conversion does not fetch remote resources. Review the returned `warnings` before publishing. Limits: 200,000 source characters, 1 MiB converted content, bounded nesting and table dimensions.

Both Markdown actions save a BlockNote format-3 draft. They never publish implicitly; use the existing publication workflow with the returned article revision when publication is requested.

### Edit individual blocks without replacing the article

Read `get_article` to obtain the current `revision` and block IDs (including nested `children`). Call `patch_article_blocks` with `articleId`, that revision, a stable `saveId`, and ordered `operations`. The backend applies the whole batch in one transaction, increments the revision once, and retains the article title. Any invalid or missing target rolls back every operation.

```json
{
  "articleId": "<article ID>",
  "revision": 3,
  "saveId": "<stable patch ID>",
  "operations": [
    { "op": "update", "blockId": "paragraph-1", "props": { "textAlignment": "center" } },
    {
      "op": "insert",
      "position": "after",
      "blockId": "paragraph-1",
      "blocks": [
        {
          "id": "new-paragraph",
          "type": "paragraph",
          "content": [{ "type": "text", "text": "Added paragraph", "styles": {} }]
        }
      ]
    },
    { "op": "delete", "blockId": "obsolete-block" }
  ]
}
```

`update` merges only provided property keys. Omit `content` to preserve text and inline formatting; if supplied, it replaces only the selected block's inline/table content and should include the desired inline styles. The block's ID, type and children cannot be overwritten through an update. Other blocks, images, tables and formatting remain intact.

`insert` accepts `before`/`after` with a sibling `blockId`, or `start`/`end` with an optional `parentId` for children (omit it for root placement). Every inserted block and nested child needs a new, stable ID unique within the article. Later operations can target those new IDs. IDs deleted in the same batch cannot be reused. `delete` removes the target and its entire subtree; it does not remove other blocks or their image assets.

Use 1–100 operations on a format-3 BlockNote article. Retry the exact same original revision, save ID and operations after an uncertain response. Different payloads with the same save ID conflict. On a version conflict, read and reconcile before creating a new patch intent; never silently replace the revision. Saving a patch does not publish; use `publish_article` when knowledge-base synchronization is requested.

## Available actions

- `create_article` — Create an empty editable knowledge article as a draft. A caller-stable articleId prevents duplicate creation on retries; an existing ID returns its article without overwriting it. [write]
- `create_article_from_markdown` — Create and save an editable article from Markdown as an unpublished draft. Requires stable articleId and saveId. Creation then saving are two requests: if saving fails, a blank draft may remain; retry the identical IDs and payload to resume. Never overwrites an existing edited article; a revision conflict requires inspection. [write]
- `delete_article` — Delete an article and exclude its index from retrieval. Underlying index cleanup is asynchronous; any original converted file is preserved. [destructive]
- `delete_file` — Start asynchronous deletion of a knowledge-base file. [destructive]
- `download_file` — Download a knowledge-base file through OOMOL file transit and return a temporary public URL.
- `get_article` — Read the full editable article, its format version, revision and knowledge-base synchronization state.
- `get_file` — Get metadata and processing status for a knowledge-base file.
- `list_articles` — List knowledge articles with draft and synchronization metadata, without document bodies.
- `list_files` — List files in the current OOMOL team's knowledge base.
- `patch_article_blocks` — Atomically update, insert or delete BlockNote blocks by ID without replacing the article. Updates merge properties and replace only explicitly supplied block content, preserving other blocks, children, images and formatting. Operations run in order; a missing ID or invalid operation rolls back the entire batch. Requires format version 3 and the expected revision. Retry with identical saveId, revision and operations. Saves a draft; does not publish. [write]
- `publish_article` — Publish an exact saved revision to the knowledge base, replacing its previous index asynchronously. Retry uncertain transport outcomes with the same publishId and revision. Stop and inspect failed or uncertain synchronization states. [write]
- `retrieve` — Retrieve the most relevant text chunks from the current OOMOL team's knowledge base.
- `save_article_draft` — Save BlockNote content and title with optimistic revision checking. This only saves a draft; publish_article updates retrieval. Retry an uncertain request with the identical saveId, revision and body. [write]
- `save_article_markdown` — Replace the entire article body and title from Markdown, saving a BlockNote draft at the expected revision. This is full replacement, not append or patch; blocks and private images absent from Markdown are removed from the draft. Read and reconcile before saving; on 409 never blindly retry with a new revision. Does not publish. [write]
- `upload_file` — Upload a publicly reachable file URL to the current OOMOL team's knowledge base and start asynchronous indexing. [write]
- `wait_for_article_ready` — Poll the latest article publication once. Ready means its syncRevision is indexed; a newer draft can still be unpublished. Compare syncRevision with your requested revision when tracking a particular publication.
- `wait_for_file_deleted` — Get a file's deletion state while waiting for deletion to finish.
- `wait_for_file_ready` — Get a file's ingestion state while waiting for it to become searchable.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OOMOL RAG state — confirm the exact payload and effect with the user before running.**
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

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- OOMOL RAG homepage: https://knowledge-base.oomol.com
