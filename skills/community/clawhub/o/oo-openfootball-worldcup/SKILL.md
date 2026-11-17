---
name: oo-openfootball-worldcup
description: "OpenFootball World Cup (github.com). Use this skill for ANY OpenFootball World Cup request — searching and reading data. Whenever a task involves OpenFootball World Cup, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OpenFootball World Cup"
  author: "OOMOL"
  version: "1.0.4"
  services: ["openfootball_worldcup"]
  icon: "https://static.oomol.com/logo/third-party/openfootball_worldcup.svg"
---

# OpenFootball World Cup

Operate **OpenFootball World Cup** through your OOMOL-connected account. This skill calls the `openfootball_worldcup` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

OpenFootball World Cup needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "openfootball_worldcup" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "openfootball_worldcup" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `list_groups` — List World Cup groups from the public OpenFootball JSON dataset.
- `list_matches` — List World Cup matches from the public OpenFootball JSON dataset. This community dataset is not a real-time or official results source.
- `list_qualification_playoffs` — List World Cup qualification playoff matches from the public OpenFootball JSON dataset when a season publishes playoff files.
- `list_squads` — List World Cup squads from the public OpenFootball JSON dataset when a season publishes squad files.
- `list_stadiums` — List World Cup stadiums from the public OpenFootball JSON dataset.
- `list_teams` — List World Cup teams from the public OpenFootball JSON dataset.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OpenFootball World Cup state — confirm the exact payload and effect with the user before running.**
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

- OpenFootball World Cup homepage: https://github.com/openfootball/worldcup.json
- API documentation: https://github.com/openfootball/worldcup.json
