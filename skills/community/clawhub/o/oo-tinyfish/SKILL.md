---
name: oo-tinyfish
description: "TinyFish (tinyfish.ai). Use this skill for ANY TinyFish request — reading, creating, updating, and deleting data. Whenever a task involves TinyFish, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TinyFish"
  author: "OOMOL"
  version: "1.0.2"
  services: ["tinyfish"]
  icon: "https://static.oomol.com/logo/third-party/tinyfish.svg"
---

# TinyFish

Operate **TinyFish** through your OOMOL-connected account. This skill calls the `tinyfish` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TinyFish. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tinyfish" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tinyfish" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_profile_setup_session` — Cancel a profile setup session without saving browser state. [destructive]
- `cancel_research_run` — Cancel a research run and return whether its state changed. [destructive]
- `cancel_run` — Cancel an asynchronous automation run. Already terminal runs retain their status. Runs started through the synchronous API cannot be cancelled. [destructive]
- `cancel_runs` — Cancel up to 100 automation runs. Already terminal runs retain their existing status; missing IDs are returned separately. [destructive]
- `connect_vault` — Connect 1Password or Bitwarden and immediately sync display-safe credential metadata. [write]
- `create_browser_session` — Create a remote browser session and return CDP connection details for an external browser client. [write]
- `create_monitor` — Create a Page or Topic Monitor with a schedule and baseline run; requires a personal API key. [write]
- `create_profile` — Create a Browser Context Profile for reusable browser state. [write]
- `create_profile_setup_session` — Start an interactive setup browser to sign in and capture state for a profile. [write]
- `delete_monitor` — Delete a Monitor and stop its scheduled runs. [destructive]
- `delete_profile` — Delete a Browser Context Profile and its saved state. [destructive]
- `delete_profile_domain` — Delete cookies and storage for one saved profile domain. [destructive]
- `disconnect_vault` — Disconnect a password manager and remove its stored enabled items. [destructive]
- `fetch_urls` — Fetch up to ten URLs with content extraction, selectors and conditional request support; inspect per-URL errors.
- `get_monitor` — Get a Page or Topic Monitor and its configuration.
- `get_profile` — Get a Browser Context Profile and its saved domain metadata.
- `get_research_run` — Get research progress, final reports, sources and terminal outcome.
- `get_run` — Retrieve an automation run and captured steps. Prefer screenshot URLs for JSON clients; use get_step_screenshot or get_step_html to transfer captured files.
- `get_runs` — Retrieve up to 100 automation runs, including per-run results, steps, and missing IDs.
- `get_step_html` — Download a captured automation-step HTML snapshot and return a file-transit URL. Requires capture_config.html when submitting the run.
- `get_step_screenshot` — Download a captured automation-step screenshot and return a file-transit URL.
- `get_wallet` — Get wallet balance, auto-reload configuration, rates, and pending top-up details.
- `list_browser_usage` — List paginated browser session usage, filtered by session, timestamps, or status.
- `list_fetch_usage` — List paginated fetch usage records.
- `list_monitors` — List Page and Topic Monitors owned by the personal API key.
- `list_profiles` — List Browser Context Profiles and tracked signed-in sites.
- `list_research_runs` — List research runs with query, state, timestamp and cursor filters.
- `list_runs` — List and search automation runs with cursor pagination, status, goal, and creation-time filters.
- `list_search_usage` — List paginated search usage records and recorded results.
- `list_vault_connections` — List connected password managers and validation status.
- `list_vault_items` — List display-safe vault item metadata available from connected password managers.
- `run_monitor` — Run a Monitor immediately and return its Page or Topic results. [write]
- `save_profile_setup_session` — Save cookies and browser storage from a setup session into its profile. [write]
- `search` — Search web pages, news or research papers with optional content fetching.
- `start_research` — Start deep or maximum-depth research and retrieve its reports through get_research_run. [write]
- `submit_run` — Submit a browser automation task asynchronously. The agent can perform arbitrary website operations; use get_run to retrieve progress and results. [destructive]
- `submit_run_batch` — Atomically submit 1–100 browser automation tasks. Shared profile_id and output_schema apply to the batch. Retrieve each run using get_run or get_runs. [destructive]
- `sync_vault_items` — Sync connected password managers and return item metadata and synchronization counts. [write]
- `terminate_browser_session` — Terminate a remote browser session; an already-ended session also succeeds. [destructive]
- `top_up_wallet` — Request a wallet top-up or submit caller-supplied MPP payment authorization. Return the payment challenge when payment is required. A pending result means payment was charged; do not pay again. [write]
- `update_monitor` — Pause or resume a Monitor, or update its schedule and optional metadata; these update modes cannot be combined. [destructive]
- `update_profile` — Update profile metadata, default selection, or proxy country. [write]
- `upload_profile_state` — Upload cookies, local storage, and session storage into a Browser Context Profile. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TinyFish state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TinyFish is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tinyfish
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TinyFish homepage: https://tinyfish.ai
- API documentation: https://docs.tinyfish.ai/
