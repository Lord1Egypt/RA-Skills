---
name: oo-cloudlayer
description: "cloudlayer.io (cloudlayer.io). Use this skill for ANY cloudlayer.io request — reading, creating, and updating data. Whenever a task involves cloudlayer.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "cloudlayer.io"
  author: "OOMOL"
  version: "1.0.1"
  services: ["cloudlayer"]
  icon: "https://static.oomol.com/logo/third-party/cloudlayer.svg"
---

# cloudlayer.io

Operate **cloudlayer.io** through your OOMOL-connected account. This skill calls the `cloudlayer` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected cloudlayer.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudlayer" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudlayer" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_html_pdf_job` — Create an asynchronous cloudlayer.io HTML-to-PDF job from base64-encoded HTML and return the new job status. [write]
- `create_template_pdf_job` — Create an asynchronous cloudlayer.io template-to-PDF job from a base64-encoded template and JSON data. [write]
- `create_url_pdf_job` — Create an asynchronous cloudlayer.io URL-to-PDF job for one public webpage and return the new job status. [write]
- `get_account` — Get the current cloudlayer.io account usage, limits, and job totals for the API key.
- `get_asset` — Get one generated cloudlayer.io asset by asset ID, including its direct download URL.
- `get_job` — Get one cloudlayer.io job by job ID to inspect status, timing, and request metadata.
- `list_assets` — List recent generated cloudlayer.io assets for the current account with optional cursor pagination.
- `list_jobs` — List recent cloudlayer.io jobs for the current account with optional cursor pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change cloudlayer.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — cloudlayer.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=cloudlayer
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- cloudlayer.io homepage: https://cloudlayer.io
