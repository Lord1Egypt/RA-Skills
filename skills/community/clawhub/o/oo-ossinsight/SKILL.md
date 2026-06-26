---
name: oo-ossinsight
description: "OSS Insight (ossinsight.io). Use this skill for ANY OSS Insight request — searching and reading data. Whenever a task involves OSS Insight, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OSS Insight"
  author: "OOMOL"
  version: "1.0.1"
  services: ["ossinsight"]
  icon: "https://static.oomol.com/logo/third-party/ossinsight.png"
---

# OSS Insight

Operate **OSS Insight** through your OOMOL-connected account. This skill calls the `ossinsight` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

OSS Insight needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ossinsight" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ossinsight" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_issue_creators_history` — Get historical issue creator counts for a GitHub repository.
- `get_pull_request_creators_history` — Get historical pull request creator counts for a GitHub repository.
- `get_stargazers_history` — Get the historical stargazer count for a GitHub repository.
- `list_collection_repos` — List repositories in an OSS Insight collection.
- `list_collections` — List all OSS Insight repository collections.
- `list_hot_collections` — List hot OSS Insight collections with representative repositories.
- `list_issue_creator_countries` — List countries or regions of issue creators for a GitHub repository.
- `list_issue_creator_organizations` — List organizations of issue creators for a GitHub repository.
- `list_issue_creators` — List issue creators for a GitHub repository.
- `list_pull_request_creator_countries` — List countries or regions of pull request creators for a GitHub repository.
- `list_pull_request_creator_organizations` — List organizations of pull request creators for a GitHub repository.
- `list_pull_request_creators` — List pull request creators for a GitHub repository.
- `list_stargazer_countries` — List countries or regions of stargazers for a GitHub repository.
- `list_stargazer_organizations` — List organizations of stargazers for a GitHub repository.
- `list_trending_repos` — List recently trending GitHub repositories from OSS Insight.
- `rank_collection_repos_by_issues` — Rank repositories in an OSS Insight collection by issue growth.
- `rank_collection_repos_by_pull_requests` — Rank repositories in an OSS Insight collection by pull request growth.
- `rank_collection_repos_by_stars` — Rank repositories in an OSS Insight collection by star growth.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OSS Insight state — confirm the exact payload and effect with the user before running.**
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

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OSS Insight homepage: https://ossinsight.io
