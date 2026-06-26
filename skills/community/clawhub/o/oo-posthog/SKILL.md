---
name: oo-posthog
description: "PostHog (posthog.com). Use this skill for ANY PostHog request — reading, creating, updating, and deleting data. Whenever a task involves PostHog, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PostHog"
  author: "OOMOL"
  version: "1.0.1"
  services: ["posthog"]
  icon: "https://static.oomol.com/logo/third-party/PostHog.svg"
---

# PostHog

Operate **PostHog** through your OOMOL-connected account. This skill calls the `posthog` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PostHog. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "posthog" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "posthog" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_dashboard_collaborator` — Add a collaborator to a PostHog dashboard. [write]
- `add_persons_to_static_cohort` — Add person UUIDs to a static PostHog cohort. [write]
- `bulk_update_event_definition_tags` — Bulk add, remove, or set tags on PostHog event definitions. [write]
- `bulk_update_property_definition_tags` — Bulk add, remove, or set tags on PostHog property definitions. [write]
- `cancel_query` — Cancel a PostHog async query by project ID and query ID. [write]
- `copy_dashboard_tile` — Copy an existing PostHog dashboard tile to another dashboard. [write]
- `create_annotation` — Create an annotation in a PostHog project. [write]
- `create_cohort` — Create a cohort in a PostHog project. [write]
- `create_dashboard` — Create a PostHog dashboard in a project. [write]
- `create_event_definition` — Create an event definition for a PostHog project. [write]
- `create_feature_flag` — Create a feature flag in a PostHog project. [write]
- `create_insight` — Create a saved PostHog insight in a project. [write]
- `delete_annotation` — Mark a PostHog annotation as deleted using the official soft-delete contract. [destructive]
- `delete_cohort` — Mark a PostHog cohort as deleted using the official soft-delete contract. [destructive]
- `delete_dashboard` — Mark a PostHog dashboard as deleted using the official soft-delete contract. [destructive]
- `delete_event_definition` — Delete a PostHog event definition by ID. [destructive]
- `delete_feature_flag` — Soft delete a PostHog feature flag by setting deleted to true. [destructive]
- `delete_insight` — Delete a saved PostHog insight by ID. [destructive]
- `delete_property_definition` — Delete a PostHog property definition by ID. [destructive]
- `get_annotation` — Get a PostHog annotation by ID.
- `get_async_query_status` — Retrieve the status and available result payload for a PostHog async query.
- `get_cohort` — Get a PostHog cohort by ID.
- `get_cohort_calculation_history` — Get the raw calculation history payload for a PostHog cohort.
- `get_cohort_persons` — List persons that belong to a PostHog cohort.
- `get_current_user` — Get the current user associated with the PostHog personal API key.
- `get_dashboard` — Get a PostHog dashboard by ID with a stable top-level connector shape.
- `get_event_definition` — Get a PostHog event definition by ID.
- `get_event_definition_by_name` — Get a PostHog event definition by exact event name.
- `get_event_definition_primary_properties` — Get primary properties configured for PostHog event definitions.
- `get_feature_flag` — Get a PostHog feature flag by ID.
- `get_feature_flag_dependent_flags` — List the feature flags that depend on a PostHog feature flag.
- `get_feature_flag_status` — Get the computed status for a PostHog feature flag.
- `get_feature_flags_local_evaluation` — Get the local evaluation payload for PostHog feature flags.
- `get_insight` — Get a PostHog insight by ID with a stable top-level connector shape.
- `get_project` — Get a PostHog project from the current or specified organization.
- `get_property_definition` — Get a PostHog property definition by ID.
- `list_annotations` — List annotations for a PostHog project.
- `list_cohorts` — List cohorts for a PostHog project.
- `list_dashboard_collaborators` — List collaborators for a PostHog dashboard.
- `list_dashboards` — List dashboards for a PostHog project.
- `list_event_definitions` — List event definitions for a PostHog project.
- `list_feature_flags` — List feature flags for a PostHog project.
- `list_insights` — List insights for a PostHog project.
- `list_projects` — List PostHog projects for the current or specified organization.
- `list_property_definitions` — List property definitions for a PostHog project.
- `move_dashboard_tile` — Move a PostHog dashboard tile to another dashboard. [write]
- `remove_dashboard_collaborator` — Remove a collaborator from a PostHog dashboard. [destructive]
- `reorder_dashboard_tiles` — Reorder tiles on a PostHog dashboard.
- `run_dashboard_insights` — Run all insights on a PostHog dashboard and return their results.
- `run_query` — Run a PostHog query and return a stable top-level query result shape.
- `update_annotation` — Partially update a PostHog annotation by ID. [write]
- `update_cohort` — Partially update a PostHog cohort by ID. [write]
- `update_dashboard` — Partially update a PostHog dashboard by ID. [write]
- `update_event_definition` — Partially update a PostHog event definition by ID. [write]
- `update_feature_flag` — Partially update a PostHog feature flag by ID. [write]
- `update_insight` — Update a saved PostHog insight by ID. [write]
- `update_property_definition` — Partially update a PostHog property definition by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PostHog state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PostHog is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=posthog
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- PostHog homepage: https://posthog.com
