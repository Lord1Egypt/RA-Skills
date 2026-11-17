---
name: oo-elasticsearch
description: "Elasticsearch (elastic.co). Use this skill for ANY Elasticsearch request — reading, creating, updating, and deleting data. Whenever a task involves Elasticsearch, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Elasticsearch"
  author: "OOMOL"
  version: "1.0.8"
  services: ["elasticsearch"]
  icon: "https://static.oomol.com/logo/third-party/Elasticsearch.svg"
---

# Elasticsearch

Operate **Elasticsearch** through your OOMOL-connected account. This skill calls the `elasticsearch` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Elasticsearch. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "elasticsearch" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "elasticsearch" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `bulk_index_documents` — Apply many Elasticsearch document writes in one bulk request. Each operation names its own index, and per-operation failures are reported in the response instead of failing the whole request. [destructive]
- `count_documents` — Count Elasticsearch documents matching a query without returning any hits, which is cheaper than a search when only the size of a result set matters.
- `create_index` — Create one Elasticsearch index with explicit mappings, settings, and aliases. [write]
- `delete_by_query` — Delete Elasticsearch documents matching a query. This destroys data and cannot be undone, so a bounded maxDocs and at least one of query, termFilters, rangeFilters, or timeFilter are required, the index name must be exact, and _all is rejected. That makes it impossible to empty an entire index by accident. The action waits for the deletion to finish, and a large maxDocs can outlast that wait: a timeout does not cancel the deletion, which keeps running on the cluster with no task id to poll, so a retry after a timeout deletes a further batch. [destructive]
- `delete_document` — Delete one Elasticsearch document by id. A missing document returns a not_found result instead of raising an error. [destructive]
- `delete_index` — Permanently delete one or more Elasticsearch indices by exact name. This destroys data and cannot be undone, so wildcards, comma-separated lists, and _all are rejected, and expectedCount must equal the number of names supplied. [destructive]
- `get_cluster_health` — Get detailed Elasticsearch cluster health including shard counts and an optional per-index breakdown.
- `get_cluster_nodes` — List Elasticsearch cluster nodes with uptime, heap, disk, and role information. Node uptime is what makes the cumulative counters from get_index_stats interpretable.
- `get_document` — Get one Elasticsearch document by id. A missing document returns found as false instead of raising an error.
- `get_index_schema` — Get mappings, settings, aliases, and field statistics for one Elasticsearch index.
- `get_index_stats` — Get document, store, search, get, and indexing statistics for Elasticsearch indices. Counters such as searchQueryTotal are cumulative since each node started rather than a time window, so compare them against the node uptime in counterWindow before concluding that a zero means the index is never queried.
- `get_task` — Get the state and progress of one Elasticsearch task, such as a reindex started by the reindex action.
- `index_document` — Index or replace one document in an Elasticsearch index. Supplying documentId replaces that document, while omitting it lets Elasticsearch generate an id. [destructive]
- `list_aliases` — List Elasticsearch aliases and the indices behind them, optionally filtered by alias or index pattern.
- `list_indices` — List Elasticsearch indices visible to the connected user.
- `list_shards` — List Elasticsearch shard placement, state, and size, optionally limited to an index pattern or a shard state.
- `ping_cluster` — Check whether the Elasticsearch cluster is reachable and return its health status.
- `query_index` — Search an Elasticsearch index with text queries, filters, pagination, sorting, and aggregations.
- `reindex` — Start an Elasticsearch reindex from one index to another and return a task id to poll with get_task. The copy runs in the background, so this action returns before the data has moved. [write]
- `update_aliases` — Atomically add or remove Elasticsearch alias assignments in a single request, which is how an alias is switched between indices without downtime. This action cannot delete an index; use delete_index for that. [destructive]
- `update_index_mappings` — Add or update field mappings on an existing Elasticsearch index. Existing field types cannot be changed in place, so incompatible changes require a new index and a reindex. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Elasticsearch state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Elasticsearch is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, custom credential) at:

  ```text
  https://console.oomol.com/connections/elasticsearch
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Elasticsearch homepage: https://www.elastic.co/elasticsearch
- API documentation: https://www.elastic.co/docs/api/doc/elasticsearch/
