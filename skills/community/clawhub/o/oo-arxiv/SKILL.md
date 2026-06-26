---
name: oo-arxiv
description: "arXiv (arxiv.org). Use this skill for ANY arXiv request — searching and reading data. Whenever a task involves arXiv, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "arXiv"
  author: "OOMOL"
  version: "1.0.1"
  services: ["arxiv"]
  icon: "https://static.oomol.com/logo/third-party/arxiv.svg"
---

# arXiv

Operate **arXiv** through your OOMOL-connected account. This skill calls the `arxiv` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

arXiv needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "arxiv" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "arxiv" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_paper` — Get one arXiv paper by arXiv identifier.
- `get_papers` — Get multiple arXiv papers by arXiv identifiers.
- `list_recent_papers` — List recent arXiv papers for one category sorted by submission date.
- `search_by_abstract` — Search arXiv papers by abstract text.
- `search_by_all_fields` — Search arXiv papers by combining optional all-field, author, title, abstract, and category filters.
- `search_by_author` — Search arXiv papers by author name.
- `search_by_title` — Search arXiv papers by title text.
- `search_papers` — Search arXiv papers using the official arXiv API query syntax.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change arXiv state — confirm the exact payload and effect with the user before running.**
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

- arXiv homepage: https://arxiv.org/
