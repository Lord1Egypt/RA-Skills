---
name: oo-web-of-science-expanded
description: "Web of Science Expanded (clarivate.com). Use this skill for ANY Web of Science Expanded request — searching and reading data. Whenever a task involves Web of Science Expanded, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Web of Science Expanded"
  author: "OOMOL"
  version: "1.0.4"
  services: ["web_of_science_expanded"]
  icon: "https://static.oomol.com/logo/third-party/web_of_science_expanded.svg"
---

# Web of Science Expanded

Operate **Web of Science Expanded** through your OOMOL-connected account. This skill calls the `web_of_science_expanded` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Web of Science Expanded. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "web_of_science_expanded" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "web_of_science_expanded" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_citation_report` — Generate citation totals, self-citation-adjusted metrics, yearly counts, and h-index for a Web of Science query.
- `get_documents` — Get one or more Web of Science Expanded records by UID with short, full, or custom field detail.
- `list_cited_references` — List the bibliographic references cited by a Web of Science document.
- `list_citing_documents` — List Web of Science documents that cite a source document.
- `list_related_documents` — List Web of Science documents related through shared cited references.
- `search_documents` — Search Web of Science Expanded records with advanced queries, quota-aware detail selection, filters, sorting, and pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Web of Science Expanded state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Web of Science Expanded is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/web_of_science_expanded
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Web of Science Expanded homepage: https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/
- API documentation: https://developer.clarivate.com/apis/wos
