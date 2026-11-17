---
name: oo-pubmed
description: "PubMed (pubmed.ncbi.nlm.nih.gov). Use this skill for ANY PubMed request — searching and reading data. Whenever a task involves PubMed, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PubMed"
  author: "OOMOL"
  version: "1.0.4"
  services: ["pubmed"]
  icon: "https://static.oomol.com/logo/third-party/pubmed.svg"
---

# PubMed

Operate **PubMed** through your OOMOL-connected account. This skill calls the `pubmed` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PubMed. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pubmed" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pubmed" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `convert_article_ids` — Convert PMID, PMCID, DOI, or author manuscript identifiers with the PMC ID Converter. Complete mappings are available only for articles represented in PubMed Central.
- `find_related_articles` — Find normalized PubMed articles related to one source PMID.
- `get_article` — Get one normalized PubMed article by PMID.
- `get_article_references` — Get normalized PubMed references for one source PMID. References are available only when supplied by publishers or recoverable from PMC data.
- `get_articles` — Get multiple normalized PubMed articles by PMID in one request.
- `get_citing_articles` — Get normalized PubMed articles known to cite one source PMID. PubMed citation coverage depends on data supplied by publishers and NCBI sources and may be incomplete.
- `match_citation` — Match one raw biomedical citation to PubMed and return normalized candidate articles.
- `search_articles` — Search PubMed with the official query syntax and return normalized article records.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PubMed state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PubMed is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pubmed
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- PubMed homepage: https://pubmed.ncbi.nlm.nih.gov/
- API documentation: https://www.ncbi.nlm.nih.gov/books/NBK25497/
