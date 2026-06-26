---
name: oo-googledrive
description: "Google Drive (workspace.google.com). Use this skill for ANY Google Drive request — reading, creating, updating, and deleting data. Whenever a task involves Google Drive, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Drive"
  author: "OOMOL"
  version: "1.0.3"
  services: ["googledrive"]
  icon: "https://static.oomol.com/logo/third-party/Google%20Drive.svg"
---

# Google Drive

Operate **Google Drive** through your OOMOL-connected account. This skill calls the `googledrive` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Drive. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googledrive" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googledrive" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `about.get` — Get Drive account information such as user details, quota, and supported capabilities.
- `accessproposals.list` — List pending access proposals for a specific Drive file.
- `approvals.list` — List approvals associated with a specific Drive file.
- `apps.get` — Get metadata for a specific Google Drive app by app ID.
- `changes.getStartPageToken` — Get the page token for monitoring future Drive changes.
- `changes.list` — List file and drive changes for incremental sync workflows.
- `comments.create` — Create a comment on a Drive file, optionally with anchor or quoted file content. [write]
- `comments.delete` — Permanently delete a comment thread from a Drive file. [destructive]
- `comments.get` — Get a specific comment on a Drive file by comment ID.
- `comments.list` — List comments on a Drive file with pagination.
- `comments.update` — Update the content of an existing Drive file comment. [write]
- `drives.create` — Create a new shared drive. [write]
- `drives.delete` — Permanently delete a shared drive. [destructive]
- `drives.get` — Get a shared drive by drive ID.
- `drives.hide` — Hide a shared drive from the default Drive view. [write]
- `drives.list` — List shared drives accessible to the connected account.
- `drives.unhide` — Unhide a shared drive and restore it to the default Drive view. [write]
- `drives.update` — Update metadata or restrictions on a shared drive. [write]
- `files.copy` — Copy a Drive file and optionally override official File metadata. [write]
- `files.create` — Create a Drive file with official File metadata and optional connector media upload content. [write]
- `files.delete` — Permanently delete a Drive file or folder by ID. [destructive]
- `files.emptyTrash` — Permanently empty the user's trash or a shared drive's trash. [write]
- `files.export` — Export a Google Workspace file to the requested MIME type and return a transit URL for the exported content.
- `files.generateIds` — Generate one or more Drive file IDs for later create or copy requests. [write]
- `files.get` — Get metadata for a Drive file by ID.
- `files.list` — List Google Drive files using the official Drive query and pagination parameters.
- `files.listLabels` — List the Drive labels currently applied to a file.
- `files.modifyLabels` — Add, update, or remove Drive labels on a file. [write]
- `files.update` — Patch a Drive file with official metadata, parent query parameters, and optional connector media upload content. [write]
- `permissions.create` — Create a permission on a Drive file or shared drive. [write]
- `permissions.delete` — Delete a permission from a Drive file or shared drive. [destructive]
- `permissions.get` — Get a specific permission on a Drive file or shared drive by permission ID.
- `permissions.list` — List permissions on a Drive file or shared drive.
- `permissions.update` — Update an existing Drive permission using Google Drive v3 patch semantics. [write]
- `replies.create` — Create a reply under an existing Drive file comment. [write]
- `replies.delete` — Permanently delete a specific reply from a Drive file comment thread. [destructive]
- `replies.get` — Get a specific reply under a Drive file comment.
- `replies.list` — List replies under a Drive file comment with pagination.
- `replies.update` — Update the content of an existing reply on a Drive file comment. [write]
- `revisions.delete` — Permanently delete a specific revision from a Drive file. [destructive]
- `revisions.get` — Get metadata for a specific Drive file revision.
- `revisions.list` — List revision metadata for a Drive file.
- `revisions.update` — Update revision metadata flags on a specific Drive file revision. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Drive state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Drive is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=googledrive
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Drive homepage: https://workspace.google.com/products/drive/
