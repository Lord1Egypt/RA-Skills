---
name: oo-agenty
description: "Agenty (agenty.com). Use this skill for ANY Agenty request — reading, creating, updating, and deleting data. Whenever a task involves Agenty, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Agenty"
  author: "OOMOL"
  version: "1.0.1"
  services: ["agenty"]
  icon: "https://static.oomol.com/logo/third-party/Agenty.svg"
---

# Agenty

Operate **Agenty** through your OOMOL-connected account. This skill calls the `agenty` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Agenty. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "agenty" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "agenty" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_list_rows` — Insert one or more rows into one Agenty list. [write]
- `capture_screenshot` — Capture a screenshot for one web page and return a downloadable file.
- `clear_list_rows` — Delete all rows from one Agenty list. [destructive]
- `convert_url_to_pdf` — Convert one web page into a PDF document and return a downloadable file.
- `copy_agent` — Clone one Agenty agent by agent identifier. [write]
- `create_agent` — Create one Agenty agent with the provided configuration. [write]
- `create_list` — Create one Agenty list. [write]
- `delete_agent` — Delete one Agenty agent by agent identifier. [destructive]
- `delete_list_row` — Delete one Agenty list row by list and row identifiers. [destructive]
- `delete_list_rows` — Delete multiple Agenty list rows by list identifier and row identifiers. [destructive]
- `download_job_file` — Download one named Agenty job file and return a downloadable file.
- `download_job_result` — Download one Agenty job export as raw text content.
- `download_list_rows` — Download all rows from one Agenty list as raw text content.
- `extract_structured_data` — Extract structured metadata such as JSON-LD, RDFa, microdata, and meta tags.
- `get_agent` — Get one Agenty agent by agent identifier.
- `get_agent_inputs` — Get the current Agenty input configuration for one agent.
- `get_agent_templates` — List public Agenty agent templates with optional pagination and sorting parameters.
- `get_job` — Get one Agenty job by job identifier.
- `get_job_logs` — Get raw log content for one Agenty job.
- `get_job_result` — Get paginated result rows for one Agenty job.
- `get_list` — Get one Agenty list by list identifier.
- `get_list_row` — Get one Agenty list row by list and row identifiers.
- `get_page_content` — Fetch the rendered HTML content for one web page.
- `get_redirects` — Return the ordered redirect chain for one URL.
- `list_agents` — List Agenty agents with optional pagination and sorting parameters.
- `list_job_files` — List the files generated for one Agenty job.
- `list_jobs` — List Agenty jobs with optional pagination, sorting, and agent filtering parameters.
- `start_job` — Start one Agenty job for an existing agent. [write]
- `stop_job` — Stop one running Agenty job by job identifier. [write]
- `update_agent` — Update one Agenty agent by agent identifier. [write]
- `update_agent_inputs` — Update the Agenty input configuration for one agent. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Agenty state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Agenty is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=agenty
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Agenty homepage: https://agenty.com
