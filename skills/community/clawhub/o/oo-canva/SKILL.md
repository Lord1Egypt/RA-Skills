---
name: oo-canva
description: "Canva (canva.com). Use this skill for ANY Canva request — reading, creating, and updating data. Whenever a task involves Canva, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Canva"
  author: "OOMOL"
  version: "1.0.1"
  services: ["canva"]
  icon: "https://static.oomol.com/logo/third-party/canva.png"
---

# Canva

Operate **Canva** through your OOMOL-connected account. This skill calls the `canva` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Canva. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "canva" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "canva" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_design` — Create a new Canva design from a preset type, custom dimensions, an optional image asset, an existing design, or a brand template. [write]
- `create_design_export_job` — Start an asynchronous Canva export job for a design and return the job handle for polling. [write]
- `create_folder` — Create a Canva folder at the top level, in uploads, or inside another folder. [write]
- `create_url_asset_upload_job` — Start an asynchronous Canva asset upload job from a publicly accessible URL and return the job handle for polling. [write]
- `get_asset` — Get metadata for a Canva asset, including owner, thumbnail, and type-specific metadata.
- `get_current_user` — Get the Canva user and profile associated with the current OAuth token.
- `get_design` — Get metadata for a Canva design, including owner, URLs, and thumbnail details.
- `get_design_export_formats` — List the file formats currently available for exporting a Canva design.
- `get_design_export_job` — Get the current status and result URLs for a Canva design export job created by create_design_export_job.
- `get_url_asset_upload_job` — Get the current status and uploaded asset metadata for a Canva URL asset upload job. [write]
- `list_designs` — List metadata for the current Canva user's designs, with optional search, ownership, sorting, and pagination filters.
- `list_folder_items` — List Canva folder contents, including folders, designs, and image assets, with pagination and filtering options.
- `move_folder_item` — Move a Canva folder item to another Canva folder. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Canva state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Canva is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=canva
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Canva homepage: https://www.canva.com
