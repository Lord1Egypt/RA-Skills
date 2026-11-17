---
name: oo-trilium
description: "TriliumNext Notes (triliumnotes.org). Use this skill for ANY TriliumNext Notes request — reading, creating, updating, and deleting data. Whenever a task involves TriliumNext Notes, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TriliumNext Notes"
  author: "OOMOL"
  version: "1.0.5"
  services: ["trilium"]
  icon: "https://static.oomol.com/logo/third-party/trilium.svg"
---

# TriliumNext Notes

Operate **TriliumNext Notes** through your OOMOL-connected account. This skill calls the `trilium` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TriliumNext Notes. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "trilium" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "trilium" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_attribute` — Create a label or relation attribute on a Trilium note. [write]
- `create_branch` — Place an existing Trilium note under another parent, or update that placement if it exists. [write]
- `create_note` — Create a note and place it under a parent in the Trilium note tree. [write]
- `delete_attachment` — Delete a Trilium attachment. [destructive]
- `delete_attribute` — Delete a Trilium label or relation attribute. [destructive]
- `delete_branch` — Delete a Trilium branch; deleting a note's final branch also deletes the note. [destructive]
- `delete_note` — Delete a Trilium note and all of its placements from the note tree. [destructive]
- `get_attachment` — Get Trilium attachment metadata by attachment id.
- `get_attribute` — Get a Trilium label or relation attribute by attribute id.
- `get_branch` — Get a Trilium note-tree branch by branch id.
- `get_note` — Get Trilium note metadata by note id.
- `get_note_content` — Read the text content of a text-based Trilium note.
- `list_note_attachments` — List attachment metadata owned by a Trilium note.
- `search_notes` — Search Trilium notes using full text, labels, subtree constraints, and ordering options.
- `update_attachment` — Update mutable metadata on a Trilium attachment. [write]
- `update_attribute` — Update the value or position of a Trilium label, or the position of a relation. [write]
- `update_branch` — Update the position, prefix, or expanded state of a Trilium branch. [write]
- `update_note` — Update mutable metadata on a Trilium note. [write]
- `update_note_content` — Replace the text content of a text-based Trilium note. [destructive]
- `upload_attachment` — Download a public file URL and upload it as a Trilium note attachment. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TriliumNext Notes state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TriliumNext Notes is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/trilium
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TriliumNext Notes homepage: https://triliumnotes.org
- API documentation: https://docs.triliumnotes.org/user-guide/advanced-usage/etapi
