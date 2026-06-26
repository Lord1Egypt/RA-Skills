---
name: oo-rocket-reach
description: "RocketReach (rocketreach.co). Use this skill for ANY RocketReach request — searching and reading data. Whenever a task involves RocketReach, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "RocketReach"
  author: "OOMOL"
  version: "1.0.1"
  services: ["rocket_reach"]
  icon: "https://static.oomol.com/logo/third-party/RocketReach.svg"
---

# RocketReach

Operate **RocketReach** through your OOMOL-connected account. This skill calls the `rocket_reach` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected RocketReach. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "rocket_reach" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "rocket_reach" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_person_status` — Check the current status of one or more RocketReach person lookups.
- `get_account` — Retrieve the authenticated RocketReach account profile.
- `get_company_funding` — Retrieve the revenue and funding-investor data exposed on a RocketReach company profile by looking up the target company first.
- `get_company_industries` — Retrieve the industry and industry-keyword data exposed on a RocketReach company profile by looking up the target company first.
- `get_company_size` — Retrieve the employee-count data exposed on a RocketReach company profile by looking up the target company first.
- `lookup_company` — Look up a RocketReach company profile by id, name, or domain.
- `lookup_person` — Look up a RocketReach person profile by id, email, name, or LinkedIn URL through the official lookup endpoint.
- `lookup_person_and_company` — Look up a RocketReach person profile and return any company profile embedded in the official lookup response.
- `search_companies` — Look up a company by exact name, domain, or id and return it as a single-item company list for search-style compatibility.
- `search_people` — Search RocketReach people with the official structured query object and pagination controls.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change RocketReach state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — RocketReach is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=rocket_reach
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- RocketReach homepage: https://rocketreach.co
