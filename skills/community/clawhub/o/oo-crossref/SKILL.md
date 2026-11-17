---
name: oo-crossref
description: "Crossref (crossref.org). Use this skill for ANY Crossref request — searching and reading data. Whenever a task involves Crossref, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Crossref"
  author: "OOMOL"
  version: "1.0.4"
  services: ["crossref"]
  icon: "https://static.oomol.com/logo/third-party/crossref.svg"
---

# Crossref

Operate **Crossref** through your OOMOL-connected account. This skill calls the `crossref` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Crossref. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "crossref" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "crossref" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `export_work_citation` — Export one DOI as BibTeX, RIS, CSL JSON, a formatted citation, RDF, Turtle, or UNIXREF XML.
- `get_resource` — Get one Crossref journal, member, funder, DOI prefix, or work type record.
- `get_work` — Get the current Crossref metadata record for one DOI.
- `get_work_agency` — Get the DOI registration agency reported by Crossref for one work.
- `list_changed_works` — Page through Crossref works created, updated by members, or re-indexed since a point in time.
- `list_citation_locales` — List the locale identifiers accepted for formatted Crossref citations.
- `list_citation_styles` — List the CSL style identifiers accepted for formatted Crossref citations.
- `list_resources` — List or search Crossref journals, members, funders, work types, or licenses.
- `list_scoped_works` — List works associated with one Crossref journal, member, funder, DOI prefix, or work type.
- `list_works` — Search, filter, sort, sample, facet, or page through works registered with Crossref.
- `match_reference` — Find the most relevant Crossref work candidates for a formatted bibliographic reference.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Crossref state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Crossref is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/crossref
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Crossref homepage: https://www.crossref.org/
- API documentation: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
