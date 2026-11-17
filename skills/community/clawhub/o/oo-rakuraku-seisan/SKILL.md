---
name: oo-rakuraku-seisan
description: "Rakuraku Seisan (rakus.co.jp). Use this skill for ANY Rakuraku Seisan request — reading, creating, and updating data. Whenever a task involves Rakuraku Seisan, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Rakuraku Seisan"
  author: "OOMOL"
  version: "1.0.2"
  services: ["rakuraku_seisan"]
  icon: "https://static.oomol.com/logo/third-party/rakuraku_seisan.svg"
---

# Rakuraku Seisan

Operate **Rakuraku Seisan** through your OOMOL-connected account. This skill calls the `rakuraku_seisan` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Rakuraku Seisan. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "rakuraku_seisan" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "rakuraku_seisan" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `download_journal_file` — Download the latest automatically generated Rakuraku Seisan journal file for an export configuration. Configure exports in Rakuraku Seisan first; historical files are unavailable through the API. Returns a temporary download URL, preserving CSV/TXT MS932 encoding or ZIP bytes. Connector download limit: 64 MiB.
- `get_import_status` — Get a Rakuraku Seisan CSV import result. A complete process may still contain failed records; inspect failureCount and download the error report from the Rakuraku Seisan CSV import status screen when needed.
- `import_master_csv` — Schedule a Rakuraku Seisan master CSV import from a public file URL. The file must use MS932 encoding and official column names in its first row, at most 5 MB and 50,000 rows. Creates or updates records; does not delete them. Poll get_import_status to check completion and failed record counts. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Rakuraku Seisan state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Rakuraku Seisan is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/rakuraku_seisan
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Rakuraku Seisan homepage: https://www.rakus.co.jp/rakurakucloud/seisan/
- API documentation: https://success-navi.rakurakucloud.jp/seisan/manual/detail/1236
