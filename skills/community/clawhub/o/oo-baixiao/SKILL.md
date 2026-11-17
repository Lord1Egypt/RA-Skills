---
name: oo-baixiao
description: "Baixiao AI (know-pa.cn). Use this skill for ANY Baixiao AI request — reading, creating, and updating data. Whenever a task involves Baixiao AI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Baixiao AI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["baixiao"]
  icon: "https://static.oomol.com/logo/third-party/baixiao.png"
---

# Baixiao AI

Operate **Baixiao AI** through your OOMOL-connected account. This skill calls the `baixiao` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Baixiao AI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "baixiao" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "baixiao" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `advanced_search` — Search across Baixiao's databases by title, author, journal, publisher, publication period, document type, and language.
- `call_tool` — Call a current Baixiao MCP tool with JSON arguments after inspecting its live schema and behavior annotations with list_tools. [write]
- `citation_graph` — Traverse the works that cite a paper or the references cited by that paper for literature-review expansion.
- `corpus_search` — Search Baixiao's curated humanities and social-science corpus, especially for Chinese-language scholarship and Chinese authors.
- `external_search` — Search Baixiao's international academic coverage for English-language papers and citable metadata.
- `fetch_metadata` — Complete a partial or messy citation into clean publication metadata and return alternate matches.
- `fetch_metadata_batch` — Complete multiple partial references into clean publication metadata in one request.
- `find_reviewers` — Suggest potential peer reviewers by ranking authors of topic-matching works while excluding manuscript authors when requested.
- `get_pdf` — Get a short-lived PDF download link for an available document in Baixiao's public corpus; a successful lookup consumes the connected account's credits.
- `grants_award_search` — Search Baixiao's awarded research projects by topic, investigator, institution, geography, funder, program, discipline, outcome, or year.
- `grants_cfp_search` — Search Baixiao's research funding calls by topic, geography, funder, status, deadline, year, and minimum award amount.
- `hk_grants_search` — Search Baixiao's Hong Kong RGC funded-project collection by free text and award period.
- `journal_fit` — Recommend publication venues for a manuscript by ranking journals with topic-matching works in Baixiao's databases.
- `list_my_kbs` — List the connected user's available Baixiao knowledge bases and their collection IDs for later searches.
- `list_tools` — Discover the current Baixiao literature, knowledge-base, policy, and research-funding MCP tools with their live input schemas and behavior annotations.
- `my_kb_search` — Search the connected user's personal, team, teaching, and subscribed Baixiao knowledge bases.
- `policy_search` — Search Baixiao's central and local Chinese government policy collection by text, issuer, author, period, or document type.
- `verify_reference` — Look up one reference across Baixiao's databases and report its match status, best candidate, confidence, and metadata warnings.
- `verify_references` — Batch-check a bibliography across Baixiao's databases and return per-reference match results with aggregate counts.
- `xi_thought_search` — Search Baixiao's New Thought collection of key theoretical and ideological texts by topic, author, period, or document type.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Baixiao AI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Baixiao AI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/baixiao
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Baixiao AI homepage: https://www.know-pa.cn/
