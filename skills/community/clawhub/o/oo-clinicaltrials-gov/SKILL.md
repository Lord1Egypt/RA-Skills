---
name: oo-clinicaltrials-gov
description: "ClinicalTrials.gov (clinicaltrials.gov). Use this skill for ANY ClinicalTrials.gov request — searching and reading data. Whenever a task involves ClinicalTrials.gov, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ClinicalTrials.gov"
  author: "OOMOL"
  version: "1.0.4"
  services: ["clinicaltrials_gov"]
  icon: "https://static.oomol.com/logo/third-party/clinicaltrials_gov.svg"
---

# ClinicalTrials.gov

Operate **ClinicalTrials.gov** through your OOMOL-connected account. This skill calls the `clinicaltrials_gov` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

ClinicalTrials.gov needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "clinicaltrials_gov" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "clinicaltrials_gov" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_api_version` — Get the current ClinicalTrials.gov API version and daily data refresh timestamp.
- `get_field_value_statistics` — Get value statistics for selected ClinicalTrials.gov leaf fields or field data types.
- `get_list_field_size_statistics` — Get observed list-size statistics for selected ClinicalTrials.gov array fields.
- `get_registry_size_statistics` — Get ClinicalTrials.gov registry counts and the distribution of study JSON record sizes.
- `get_studies_by_nct_ids` — Get multiple ClinicalTrials.gov studies by NCT identifier and report identifiers that were not found.
- `get_study` — Get one ClinicalTrials.gov study by NCT identifier.
- `get_study_documents` — List uploaded study protocols, statistical analysis plans, and informed consent forms with their official metadata.
- `get_study_eligibility` — Get patient-facing eligibility criteria, age and sex requirements, and study population details for one ClinicalTrials.gov study.
- `get_study_locations` — Get study sites, geographic coordinates, central contacts, local contacts, and study officials for one ClinicalTrials.gov study.
- `get_study_metadata` — Get the official ClinicalTrials.gov study data model and field definitions.
- `get_study_results` — Get posted participant flow, baseline characteristics, outcome measures, adverse events, and result notes for one ClinicalTrials.gov study.
- `list_enums` — List official ClinicalTrials.gov enumeration types, values, legacy values, and field usages.
- `list_search_areas` — List the official ClinicalTrials.gov search documents, areas, parameters, and indexed pieces.
- `search_studies` — Search ClinicalTrials.gov studies with official Essie queries, filters, field selection, sorting, and cursor pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ClinicalTrials.gov state — confirm the exact payload and effect with the user before running.**
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

- ClinicalTrials.gov homepage: https://clinicaltrials.gov/
- API documentation: https://clinicaltrials.gov/data-api/api
