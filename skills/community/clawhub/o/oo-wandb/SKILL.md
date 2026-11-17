---
name: oo-wandb
description: "Weights & Biases (wandb.ai). Use this skill for ANY Weights & Biases request — reading, creating, and updating data. Whenever a task involves Weights & Biases, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Weights & Biases"
  author: "OOMOL"
  version: "1.0.5"
  services: ["wandb"]
  icon: "https://static.oomol.com/logo/third-party/wandb.svg"
---

# Weights & Biases

Operate **Weights & Biases** through your OOMOL-connected account. This skill calls the `wandb` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Weights & Biases. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wandb" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wandb" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `compare_artifact_versions` — Compare metadata, aliases, tags, lineage, sizes, and optionally files for two W&B artifact versions.
- `compare_runs` — Compare configuration, summary metrics, metadata, and optionally metric history for two W&B runs.
- `count_weave_traces` — Count matching classic Weave traces and root traces without returning trace payloads.
- `create_report` — Create a W&B report with narrative text, plots, and configurable panels. [write]
- `diagnose_run` — Inspect loss metrics and run state to diagnose the training health of a W&B run. [write]
- `get_artifact_details` — Get metadata, lineage, and optionally files for a W&B artifact version.
- `get_run_history` — Retrieve sampled time-series metric history for a W&B run.
- `infer_trace_schema` — Sample classic Weave traces to discover field paths, types, and frequent values. [write]
- `list_artifact_versions` — List versions of a W&B project artifact or registry collection.
- `list_automations` — List W&B Automations that trigger on artifact, run-state, or run-metric events.
- `list_entities` — List W&B user and team entities accessible with the configured API key.
- `list_integrations` — List Slack and webhook integrations available as W&B Automation targets.
- `list_projects` — List W&B projects for one entity or for all entities accessible with the configured API key.
- `list_registries` — List W&B model registries for an organization.
- `list_registry_collections` — List artifact collections within a W&B model registry.
- `log_analysis` — Log analysis rows, charts, and scalar metrics to W&B as a new run. [write]
- `probe_project` — Sample W&B runs to discover a project's metrics, configuration keys, tags, groups, and structure. [write]
- `query_wandb` — Run a read-only GraphQL query against W&B experiment data with bounded pagination.
- `query_weave_traces` — Query classic Weave traces with filters, ordering, selected columns, cost data, feedback, and detail-level controls.
- `resolve_trace_roots` — Resolve the root spans for a batch of classic Weave trace IDs.
- `search_docs` — Search the official W&B documentation for relevant guidance and examples.
- `summarize_evaluation` — Aggregate classic Weave evaluation results for a project or named evaluation.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Weights & Biases state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Weights & Biases is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/wandb
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Weights & Biases homepage: https://wandb.ai
- API documentation: https://docs.wandb.ai/platform/mcp-server
