---
name: oo-pinata
description: "Pinata (pinata.cloud). Use this skill for ANY Pinata request — reading, creating, updating, and deleting data. Whenever a task involves Pinata, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pinata"
  author: "OOMOL"
  version: "1.0.5"
  services: ["pinata"]
  icon: "https://static.oomol.com/logo/third-party/pinata.svg"
---

# Pinata

Operate **Pinata** through your OOMOL-connected account. This skill calls the `pinata` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pinata. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pinata" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pinata" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_file_to_group` — Add a Pinata file to a Pinata group. [write]
- `create_group` — Create a Pinata file group on the public or private IPFS network. [write]
- `delete_file` — Delete one Pinata file by ID from the public or private IPFS network. [destructive]
- `get_file` — Get one Pinata file by ID from the public or private IPFS network.
- `get_group` — Get one Pinata group by ID from the public or private IPFS network.
- `list_files` — List Pinata files from the public or private IPFS network with optional filters.
- `list_groups` — List Pinata file groups from the public or private IPFS network.
- `pin_by_cid` — Ask Pinata to pin an existing public IPFS CID.
- `query_pin_requests` — Query Pinata pin-by-CID requests with optional filters and pagination.
- `remove_file_from_group` — Remove a Pinata file from a Pinata group. [destructive]
- `update_file` — Update a Pinata file name or key-value metadata. [write]
- `update_group` — Update a Pinata group name or public visibility setting. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pinata state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pinata is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pinata
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Pinata homepage: https://pinata.cloud
- API documentation: https://docs.pinata.cloud/api-reference/introduction
