---
name: oo-docsautomator
description: "DocsAutomator (docsautomator.co). Use this skill for ANY DocsAutomator request — reading, creating, and updating data. Whenever a task involves DocsAutomator, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DocsAutomator"
  author: "OOMOL"
  version: "1.0.1"
  services: ["docsautomator"]
  icon: "https://static.oomol.com/logo/third-party/docsautomator.png"
---

# DocsAutomator

Operate **DocsAutomator** through your OOMOL-connected account. This skill calls the `docsautomator` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected DocsAutomator. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "docsautomator" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "docsautomator" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_document` — Generate one DocsAutomator document synchronously and return the resulting file URLs plus signing metadata when available. [write]
- `create_document_async` — Queue one DocsAutomator document generation job and return the job handle for later polling. [write]
- `get_automation` — Get one DocsAutomator automation by automationId or docId and return its current generation-related settings.
- `get_document_job` — Get the current status of a DocsAutomator async document generation job and return the finished document result when available.
- `get_queue_stats` — Return current DocsAutomator queue statistics for the connected workspace.
- `list_automations` — List DocsAutomator automations in the current workspace with the core fields needed for document generation setup.
- `list_template_placeholders` — List the placeholder groups extracted from a DocsAutomator Google Doc template for one automation.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DocsAutomator state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — DocsAutomator is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=docsautomator
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- DocsAutomator homepage: https://www.docsautomator.co
