---
name: oo-pkulaw
description: "PKULaw (mcp.pkulaw.com). Use this skill for ANY PKULaw request — searching and reading data. Whenever a task involves PKULaw, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PKULaw"
  author: "OOMOL"
  version: "1.0.4"
  services: ["pkulaw"]
  icon: "https://static.oomol.com/logo/third-party/pkulaw.svg"
---

# PKULaw

Operate **PKULaw** through your OOMOL-connected account. This skill calls the `pkulaw` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PKULaw. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pkulaw" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pkulaw" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a current PKULaw legal data tool with JSON arguments after checking its live schema.
- `get_law_article` — Retrieve the authoritative text of a specific provision by law title and article number.
- `list_tools` — Discover the current legal research tools and live input schemas exposed by one PKULaw MCP service.
- `search_case_documents` — Search detailed PKULaw judicial case records by title or full-text keywords, including judgment facts and reasoning.
- `search_cases` — Search authoritative PKULaw judicial cases using a natural-language fact pattern.
- `search_law_articles` — Search authoritative PKULaw provisions using a natural-language legal question or fact pattern.
- `search_laws` — Search PKULaw laws and regulations by title or full-text keywords, including source metadata and validity information.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PKULaw state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PKULaw is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pkulaw
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- PKULaw homepage: https://mcp.pkulaw.com
- API documentation: https://mcp.pkulaw.com/docs?doc=mcp-integration
