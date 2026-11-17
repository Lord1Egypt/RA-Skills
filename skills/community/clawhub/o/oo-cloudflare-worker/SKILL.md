---
name: oo-cloudflare-worker
description: "Cloudflare Worker (workers.cloudflare.com). Use this skill for ANY Cloudflare Worker request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare Worker, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare Worker"
  author: "OOMOL"
  version: "1.0.9"
  services: ["cloudflare_worker"]
  icon: "https://static.oomol.com/logo/third-party/Cloudflare.svg"
---

# Cloudflare Worker

Operate **Cloudflare Worker** through your OOMOL-connected account. This skill calls the `cloudflare_worker` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare Worker. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare_worker" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare_worker" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_build` — Cancel a queued or running Workers Builds job. [destructive]
- `create_manual_build` — Start a Workers Builds job from a configured trigger and branch or commit. [write]
- `create_worker` — Create a Cloudflare Worker using the Workers beta API. [write]
- `delete_worker` — Delete a Cloudflare Worker and its associated resources using the Workers beta API. [destructive]
- `delete_worker_script` — Delete a Cloudflare Worker script. [destructive]
- `delete_worker_script_secret` — Delete a secret binding from a Cloudflare Worker script. [destructive]
- `edit_worker` — Partially update a Cloudflare Worker using the Workers beta API while leaving omitted fields unchanged. [write]
- `get_build` — Get the current status and outcome of one Workers Builds job.
- `get_build_logs` — Get one page of log lines for a Workers Builds job.
- `get_worker` — Get one Worker by Worker ID using the Workers beta API.
- `get_worker_script_content` — Fetch the raw source content for a Cloudflare Worker script.
- `get_worker_script_secret` — Get one secret binding attached to a Cloudflare Worker script.
- `get_worker_script_settings` — Get Worker metadata and configuration for a Cloudflare Worker script.
- `list_accounts` — List Cloudflare accounts visible to the current credential.
- `list_build_triggers` — List Workers Builds triggers configured for one Worker script tag.
- `list_builds` — List Workers Builds jobs for one Worker script tag.
- `list_worker_script_secrets` — List secret bindings attached to a Cloudflare Worker script.
- `list_worker_scripts` — List Worker scripts in a Cloudflare account.
- `list_workers` — List Workers in a Cloudflare account using the Workers beta API.
- `patch_worker_script_settings` — Patch Worker metadata and configuration for a Cloudflare Worker script. [write]
- `put_worker_script_content` — Replace only the content of a Cloudflare Worker script without changing metadata. [destructive]
- `put_worker_script_secret` — Add or replace a secret_text binding on a Cloudflare Worker script. [destructive]
- `search_worker_scripts` — Search Worker scripts in a Cloudflare account by name or script tag.
- `update_worker` — Replace a Cloudflare Worker using the Workers beta API, setting omitted fields to API defaults. [destructive]
- `upload_worker_script` — Create or replace a Cloudflare Worker script by uploading a module bundle as multipart/form-data. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare Worker state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare Worker is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential, OAuth2) at:

  ```text
  https://console.oomol.com/connections/cloudflare_worker
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cloudflare Worker homepage: https://workers.cloudflare.com
- API documentation: https://developers.cloudflare.com/workers/
