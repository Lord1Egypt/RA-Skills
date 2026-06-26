---
name: oo-googleslides
description: "Google Slides (workspace.google.com). Use this skill for ANY Google Slides request — reading, creating, and updating data. Whenever a task involves Google Slides, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Slides"
  author: "OOMOL"
  version: "1.0.1"
  services: ["googleslides"]
  icon: "https://static.oomol.com/logo/third-party/Google%20Slides.svg"
---

# Google Slides

Operate **Google Slides** through your OOMOL-connected account. This skill calls the `googleslides` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Slides. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googleslides" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googleslides" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_presentation` — Create a blank Google Slides presentation. Optional locale, page size, and presentation ID values are forwarded when provided. [write]
- `get_page_thumbnail2` — Generate a thumbnail for a Google Slides page. Returns a temporary content URL plus thumbnail dimensions when Google provides them.
- `presentations_batch_update` — Apply raw Google Slides batchUpdate requests to a presentation. [write]
- `presentations_copy_from_template` — Copy an existing Google Slides presentation through Google Drive so the new presentation preserves the original themes, masters, and layouts. [write]
- `presentations_get` — Retrieve a Google Slides presentation by presentation ID, or search Google Drive by exact presentation title first and then fetch the presentation.
- `presentations_pages_get` — Retrieve a specific page from a Google Slides presentation, including its page elements and page-specific properties.
- `presentations_pages_get_thumbnail` — Compatibility alias for get_page_thumbnail2. Generates a thumbnail for a Google Slides page.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Slides state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Slides is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=googleslides
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Slides homepage: https://workspace.google.com/products/slides/
