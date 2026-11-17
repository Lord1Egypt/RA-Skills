---
name: oo-vaquill
description: "Vaquill (vaquill.ai). Use this skill for ANY Vaquill request — reading, creating, updating, and deleting data. Whenever a task involves Vaquill, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Vaquill"
  author: "OOMOL"
  version: "1.0.2"
  services: ["vaquill"]
  icon: "https://static.oomol.com/logo/third-party/vaquill.svg"
---

# Vaquill

Operate **Vaquill** through your OOMOL-connected account. This skill calls the `vaquill` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Vaquill. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "vaquill" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "vaquill" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `compare_states` — Compare this provision against other states.
- `count_statutes` — Count the sections in a scope.
- `create_watch` — Create a board watch. [write]
- `delete_watch` — Delete a board watch. [destructive]
- `extract_citations` — Find the citations in a text and resolve each.
- `get_balance` — Get your credit balance.
- `get_citing_sections` — Find the sections that cite this one.
- `get_coverage` — Coverage matrix by jurisdiction and corpusType.
- `get_definitions` — Get the defined terms that govern this section.
- `get_pricing` — Get API credit pricing.
- `get_related_sections` — Get the sections around this one.
- `get_section` — Get statute section metadata.
- `get_section_body` — Get statute full text.
- `get_section_changes` — Get this section's change history.
- `get_section_enactments` — Which acts a state publisher lists against this section.
- `get_sections` — Get metadata for many statute sections.
- `get_session_law` — Get a state session law, by id or by citation.
- `get_session_law_body` — Get a state session law's text.
- `get_session_law_changes` — Feed of changes to the session-law registry.
- `get_session_laws` — Get many state session laws at once, by id or citation.
- `get_watch_changes` — List what changed on a watch's source.
- `get_watch_deliveries` — List delivery history for a watch.
- `get_watch_diff` — Old-vs-new text for one change.
- `list_boards` — List watchable boards.
- `list_divisions` — Browse the statutory hierarchy.
- `list_session_laws` — List a state's session laws.
- `list_watches` — List your board watches.
- `resolve_citation` — Resolve a citation to its section.
- `resolve_citations` — Resolve many citations at once.
- `search_session_laws` — Search the text of state session laws.
- `search_statutes` — Search US statutes, constitutions, court rules, and executive actions.
- `test_watch` — Send a test delivery. [write]
- `update_watch` — Update a board watch. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Vaquill state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Vaquill is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/vaquill
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Vaquill homepage: https://www.vaquill.ai
- API documentation: https://www.vaquill.ai/docs/api-guide/authentication
