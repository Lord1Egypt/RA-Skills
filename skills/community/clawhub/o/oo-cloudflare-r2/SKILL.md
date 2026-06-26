---
name: oo-cloudflare-r2
description: "Cloudflare R2 (cloudflare.com). Use this skill for ANY Cloudflare R2 request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare R2, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare R2"
  author: "OOMOL"
  version: "1.0.3"
  services: ["cloudflare_r2"]
  icon: "https://static.oomol.com/logo/third-party/Cloudflare.svg"
---

# Cloudflare R2

Operate **Cloudflare R2** through your OOMOL-connected account. This skill calls the `cloudflare_r2` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare R2. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare_r2" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare_r2" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_bucket` — Create an R2 bucket in a Cloudflare account. [write]
- `delete_bucket` — Delete an R2 bucket by name. [destructive]
- `delete_bucket_cors_policy` — Delete the bucket-level CORS policy for an R2 bucket. [destructive]
- `get_bucket` — Get one R2 bucket by name.
- `get_bucket_cors_policy` — Fetch the bucket-level CORS policy for an R2 bucket.
- `list_accounts` — List Cloudflare accounts visible to the current credential.
- `list_buckets` — List the R2 buckets in a Cloudflare account.
- `update_bucket` — Update mutable R2 bucket properties such as default storage class or jurisdiction. [write]
- `update_bucket_cors_policy` — Replace the bucket-level CORS policy for an R2 bucket. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare R2 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare R2 is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential, OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=cloudflare_r2
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Cloudflare R2 homepage: https://www.cloudflare.com
