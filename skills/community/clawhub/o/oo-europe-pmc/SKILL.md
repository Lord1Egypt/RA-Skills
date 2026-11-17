---
name: oo-europe-pmc
description: "Europe PMC (europepmc.org). Use this skill for ANY Europe PMC request — searching and reading data. Whenever a task involves Europe PMC, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Europe PMC"
  author: "OOMOL"
  version: "1.0.4"
  services: ["europe_pmc"]
  icon: "https://static.oomol.com/logo/third-party/europe_pmc.svg"
---

# Europe PMC

Operate **Europe PMC** through your OOMOL-connected account. This skill calls the `europe_pmc` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Europe PMC needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "europe_pmc" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "europe_pmc" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_article_status` — Check a batch of Europe PMC articles or preprints for publication, version, withdrawal, removal, and retraction updates.
- `get_annotations_by_articles` — Get text-mined entities and relationships for up to eight Europe PMC articles in one request.
- `get_citations` — Get publications that cite one Europe PMC publication.
- `get_data_links` — Get consolidated data, text-mined, and external links associated with one Europe PMC publication.
- `get_evaluations` — Get linked peer reviews and evaluations for one Europe PMC publication version.
- `get_full_text_xml` — Get JATS XML full text for a PubMed Central article in the Europe PMC open-access subset.
- `get_publication` — Get one Europe PMC publication by its source code and identifier.
- `get_references` — Get publications referenced by one Europe PMC publication.
- `search_annotations_by_entity` — Find Europe PMC articles containing annotations for a named biological entity.
- `search_annotations_by_provider` — Find Europe PMC articles containing annotations from a named provider.
- `search_annotations_by_relationship` — Find Europe PMC articles containing a text-mined relationship between two named entities.
- `search_annotations_by_section_or_type` — Find Europe PMC articles by annotation type, article section, or both in one cursor search.
- `search_grants` — Search Europe PMC research grants by funder, investigator, institution, topic, date, or other official GRIST fields.
- `search_publications` — Search Europe PMC literature and preprints with its official query syntax and cursor pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Europe PMC state — confirm the exact payload and effect with the user before running.**
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

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Europe PMC homepage: https://europepmc.org/
- API documentation: https://europepmc.org/developers
