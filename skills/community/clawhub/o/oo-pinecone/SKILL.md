---
name: oo-pinecone
description: "Pinecone (pinecone.io). Use this skill for ANY Pinecone request — reading, creating, updating, and deleting data. Whenever a task involves Pinecone, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pinecone"
  author: "OOMOL"
  version: "1.0.2"
  services: ["pinecone"]
  icon: "https://static.oomol.com/logo/third-party/pinecone.svg"
---

# Pinecone

Operate **Pinecone** through your OOMOL-connected account. This skill calls the `pinecone` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pinecone. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pinecone" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pinecone" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `configure_index` — Configure an existing Pinecone index.
- `create_index` — Create a Pinecone serverless index. [write]
- `delete_index` — Delete one Pinecone index by name. [destructive]
- `delete_vectors` — Delete vectors from a Pinecone index namespace by IDs, filter, or deleteAll. [destructive]
- `describe_index` — Describe one Pinecone index by name.
- `fetch_vectors` — Fetch Pinecone vectors by ID from one namespace.
- `get_index_stats` — Get statistics for a Pinecone index.
- `list_indexes` — List Pinecone indexes in the authenticated project.
- `list_vector_ids` — List vector IDs in a Pinecone serverless index namespace.
- `query_vectors` — Search a Pinecone index namespace with a query vector.
- `update_vector` — Update one Pinecone vector or metadata-matched records in a namespace. [write]
- `upsert_vectors` — Upsert dense or sparse vectors into a Pinecone index namespace. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pinecone state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pinecone is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pinecone
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Pinecone homepage: https://www.pinecone.io/
