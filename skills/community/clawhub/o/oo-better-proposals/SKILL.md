---
name: oo-better-proposals
description: "Better Proposals (betterproposals.io). Use this skill for ANY Better Proposals request — reading, creating, and updating data. Whenever a task involves Better Proposals, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Better Proposals"
  author: "OOMOL"
  version: "1.0.1"
  services: ["better_proposals"]
  icon: "https://static.oomol.com/logo/third-party/better_proposals.svg"
---

# Better Proposals

Operate **Better Proposals** through your OOMOL-connected account. This skill calls the `better_proposals` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Better Proposals. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "better_proposals" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "better_proposals" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_brand_settings` — Get default Better Proposals brand settings such as brand name and tax defaults.
- `get_company` — Get details for a single Better Proposals company by ID.
- `get_currency` — Get details for a single Better Proposals currency by ID.
- `get_proposal` — Get details for a single Better Proposals proposal by ID.
- `get_proposal_count` — Get the total Better Proposals proposal count for the connected account.
- `get_quote` — Get details for a single Better Proposals quote by ID.
- `get_settings` — Get current Better Proposals account settings such as tax and timezone defaults.
- `get_template` — Get details for a single Better Proposals template by ID.
- `list_companies` — List Better Proposals companies with optional pagination.
- `list_currencies` — List Better Proposals currencies with optional pagination.
- `list_document_types` — List Better Proposals document types with optional pagination.
- `list_merge_tags` — List Better Proposals custom merge tags with optional pagination. [write]
- `list_new_proposals` — List Better Proposals proposals that are currently in the new proposal lifecycle state.
- `list_opened_proposals` — List Better Proposals proposals that have been opened by recipients.
- `list_paid_proposals` — List Better Proposals proposals that have been paid.
- `list_proposals` — List Better Proposals proposals with optional pagination and document type filtering.
- `list_quotes` — List Better Proposals quotes with optional pagination.
- `list_sent_proposals` — List Better Proposals proposals that have been sent to recipients.
- `list_signed_proposals` — List Better Proposals proposals that have been signed by recipients.
- `list_templates` — List Better Proposals templates with optional pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Better Proposals state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Better Proposals is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=better_proposals
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Better Proposals homepage: https://betterproposals.io
