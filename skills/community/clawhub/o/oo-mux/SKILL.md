---
name: oo-mux
description: "Mux (mux.com). Use this skill for ANY Mux request — reading, creating, updating, and deleting data. Whenever a task involves Mux, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mux"
  author: "OOMOL"
  version: "1.0.6"
  services: ["mux"]
  icon: "https://static.oomol.com/logo/third-party/mux.svg"
---

# Mux

Operate **Mux** through your OOMOL-connected account. This skill calls the `mux` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mux. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mux" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mux" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_direct_upload` — Cancel a waiting Mux Direct Upload so it cannot create an asset. [destructive]
- `create_asset` — Create a Mux on-demand video asset from a publicly accessible media URL and return its initial processing state. [write]
- `create_direct_upload` — Create a signed Mux Direct Upload URL without proxying video bytes through the connector. [write]
- `create_playback_id` — Create a public, signed, or DRM playback ID for an existing Mux asset. [write]
- `delete_asset` — Permanently delete a Mux video asset and all of its data. [destructive]
- `get_asset` — Retrieve the latest processing state and media details for one Mux video asset.
- `get_direct_upload` — Retrieve the status, signed URL, and resulting asset ID for a Mux Direct Upload.
- `get_playback_id` — Resolve a Mux playback ID to its asset or live stream and access policy.
- `list_assets` — List Mux video assets with cursor or page-based pagination and source filters.
- `list_direct_uploads` — List Mux Direct Uploads in the current environment.
- `update_asset` — Update the passthrough value or customer metadata for an existing Mux video asset. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mux state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mux is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/mux
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Mux homepage: https://www.mux.com
- API documentation: https://www.mux.com/docs/core/make-api-requests
