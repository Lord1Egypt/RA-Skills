---
name: oo-neon-object-storage
description: "Neon Object Storage (neon.com). Use this skill for ANY Neon Object Storage request — reading, creating, updating, and deleting data. Whenever a task involves Neon Object Storage, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Neon Object Storage"
  author: "OOMOL"
  version: "1.0.0"
  services: ["neon_object_storage"]
  icon: "https://static.oomol.com/logo/third-party/neon_object_storage.svg"
---

# Neon Object Storage

Operate **Neon Object Storage** through your OOMOL-connected account. This skill calls the `neon_object_storage` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Neon Object Storage. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "neon_object_storage" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "neon_object_storage" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_bucket` — Create a Neon Object Storage bucket on a branch. [write]
- `delete_bucket` — Delete a Neon Object Storage bucket from a branch. [destructive]
- `delete_object` — Delete one object from a Neon Object Storage bucket. [destructive]
- `delete_objects_by_prefix` — Delete every object under a folder prefix in a Neon Object Storage bucket. Only objects written on this branch are removed; objects still inherited from a parent branch are left in place. [destructive]
- `download_object` — Download one Neon Object Storage object into temporary file storage, keeping its stored Content-Type.
- `generate_presigned_url` — Generate a presigned Neon Object Storage URL so the caller uploads (PUT) or downloads (GET) bytes directly, without S3 credentials. Preferred over put_object and download_object for large files. [write]
- `get_branch_storage` — Get the Neon Object Storage S3 endpoint, signing region, and addressing style for a branch. Use these values to configure any S3 client against the branch.
- `list_buckets` — List Neon Object Storage buckets visible on a branch, including buckets inherited from parent branches.
- `list_objects` — List objects in a Neon Object Storage bucket, including objects inherited from parent branches. Pass delimiter / to group keys into folders.
- `put_object` — Upload one Neon Object Storage object from a public URL, plain text, or base64 content, replacing any object with the same key. For large files prefer generate_presigned_url with operation upload so the bytes go straight to Neon. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Neon Object Storage state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Neon Object Storage is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/neon_object_storage
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Neon Object Storage homepage: https://neon.com
- API documentation: https://api-docs.neon.tech/reference/getting-started-with-neon-api
