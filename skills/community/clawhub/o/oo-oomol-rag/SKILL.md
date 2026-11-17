---
name: oo-oomol-rag
description: "OOMOL RAG (knowledge-base.oomol.com). Use this skill for ANY OOMOL RAG request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL RAG, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OOMOL RAG"
  author: "OOMOL"
  version: "1.0.1"
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

## Available actions

- `delete_file` — Start asynchronous deletion of a knowledge-base file. [destructive]
- `download_file` — Download a knowledge-base file through OOMOL file transit and return a temporary public URL.
- `get_file` — Get metadata and processing status for a knowledge-base file.
- `list_files` — List files in the current OOMOL team's knowledge base.
- `retrieve` — Retrieve the most relevant text chunks from the current OOMOL team's knowledge base.
- `upload_file` — Upload a publicly reachable file URL to the current OOMOL team's knowledge base and start asynchronous indexing. [write]
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
