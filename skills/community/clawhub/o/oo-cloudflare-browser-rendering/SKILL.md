---
name: oo-cloudflare-browser-rendering
description: "Cloudflare Browser Run (developers.cloudflare.com). Use this skill for ANY Cloudflare Browser Run request — searching and reading data. Whenever a task involves Cloudflare Browser Run, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare Browser Run"
  author: "OOMOL"
  version: "1.0.6"
  services: ["cloudflare_browser_rendering"]
  icon: "https://static.oomol.com/logo/third-party/cloudflare_browser_rendering.svg"
---

# Cloudflare Browser Run

Operate **Cloudflare Browser Run** through your OOMOL-connected account. This skill calls the `cloudflare_browser_rendering` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare Browser Run. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare_browser_rendering" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare_browser_rendering" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_html_content` — Render a URL or raw HTML with Cloudflare Browser Run and return the fully rendered HTML content.
- `get_json` — Render a URL or raw HTML with Cloudflare Browser Run and extract structured JSON from the page.
- `get_links` — Render a URL or raw HTML with Cloudflare Browser Run and return links discovered on the page.
- `get_markdown` — Render a URL or raw HTML with Cloudflare Browser Run and return the page content as Markdown.
- `list_accounts` — List Cloudflare accounts accessible to the API token so callers can confirm account IDs used by Browser Run actions.
- `scrape_elements` — Render a URL or raw HTML with Cloudflare Browser Run and scrape selected HTML elements.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare Browser Run state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare Browser Run is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, OAuth2) at:

  ```text
  https://console.oomol.com/connections/cloudflare_browser_rendering
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cloudflare Browser Run homepage: https://developers.cloudflare.com/browser-run/
- API documentation: https://developers.cloudflare.com/browser-run/
