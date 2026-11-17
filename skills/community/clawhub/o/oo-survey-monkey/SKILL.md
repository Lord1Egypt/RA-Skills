---
name: oo-survey-monkey
description: "SurveyMonkey (surveymonkey.com). Use this skill for ANY SurveyMonkey request — reading, creating, and updating data. Whenever a task involves SurveyMonkey, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SurveyMonkey"
  author: "OOMOL"
  version: "1.0.4"
  services: ["survey_monkey"]
  icon: "https://static.oomol.com/logo/third-party/survey_monkey.svg"
---

# SurveyMonkey

Operate **SurveyMonkey** through your OOMOL-connected account. This skill calls the `survey_monkey` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SurveyMonkey. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "survey_monkey" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "survey_monkey" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a SurveyMonkey contact for use in survey invitations. [write]
- `create_contact_list` — Create a SurveyMonkey contact list for survey recipients. [write]
- `create_survey` — Create a blank SurveyMonkey survey with one empty page. [write]
- `create_weblink_collector` — Create a public weblink collector for a SurveyMonkey survey. [write]
- `get_current_user` — Get the SurveyMonkey user and plan associated with the connected account.
- `get_survey_details` — Get a survey with its pages, questions, and answer choices.
- `get_survey_response_details` — Get one SurveyMonkey response including its question answers.
- `get_survey_rollups` — Get aggregate answer counts and basic statistics for every question in a SurveyMonkey survey.
- `list_collectors` — List collectors and distribution URLs for a SurveyMonkey survey.
- `list_contact_lists` — List contact lists in the connected SurveyMonkey account.
- `list_contacts` — List, filter, and search contacts in the connected SurveyMonkey account.
- `list_survey_response_details` — List detailed SurveyMonkey responses including question answers.
- `list_survey_responses` — List response metadata for a SurveyMonkey survey.
- `list_surveys` — List surveys available to the connected SurveyMonkey account.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SurveyMonkey state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SurveyMonkey is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/connections/survey_monkey
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SurveyMonkey homepage: https://www.surveymonkey.com
- API documentation: https://api.surveymonkey.com/v3/docs
