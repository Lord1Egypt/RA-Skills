---
name: oo-allratestoday
description: "AllRatesToday (allratestoday.com). Use this skill for ANY AllRatesToday request — searching and reading data. Whenever a task involves AllRatesToday, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AllRatesToday"
  author: "OOMOL"
  version: "1.0.1"
  services: ["allratestoday"]
  icon: "https://static.oomol.com/logo/third-party/allratestoday.svg"
---

# AllRatesToday

Operate **AllRatesToday** through your OOMOL-connected account. This skill calls the `allratestoday` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

AllRatesToday needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "allratestoday" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "allratestoday" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `convert` — Convert an amount between two of the 30 ECB reference currencies using the latest daily rate. Free and needs no API key.
- `get_latest_rates` — Get the latest daily ECB reference exchange rates against a base currency. Covers the 30 currencies the European Central Bank publishes; rates update once per working day around 16:00 CET. Free and needs no API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AllRatesToday state — confirm the exact payload and effect with the user before running.**
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

- AllRatesToday homepage: https://allratestoday.com
- API documentation: https://allratestoday.com/free-exchange-rate-api/
