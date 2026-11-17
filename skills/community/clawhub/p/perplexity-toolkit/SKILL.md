---
name: perplexity-toolkit
description: "Automate Perplexity AI search — batch, extract, aggregate, verify, and run a resident console (one tab/group, task threads, verified step gates)."
version: 1.1.0
author: mfang0126
license: MIT
metadata:
  hermes:
    tags: [search, perplexity, research, batch, automation, browser, console]
  platforms: [macos, linux]
---

# perplexity-toolkit

Automate Perplexity AI search via browser control — search, extract, batch, analyze, and run a resident console.

## Route boundary

The `perplexity` CLI is the default user-facing route for Perplexity requests
that do not explicitly ask for a web page, browser, Chrome, or WebBridge. The
CLI currently uses the toolkit's only shipped `WebBridgeDriver` underneath;
it is not an API or headless backend. Direct browser actions are reserved for
explicit browser/WebBridge requests — and within that route the
`perplexity console` (resident console) is the default executor for repeat or
one-group work; see `skills/perplexity-web-automation` and
`skills/perplexity-conversational-research` for the agent-facing policy. CLI
failure must not silently switch to the user's browser.

## When to Use

- Batch search hundreds of queries with resume support
- Extract all cited sources from Perplexity results
- Aggregate and deduplicate sources across multiple searches
- Research tasks that need Perplexity's Deep Research or Model Council modes
- Repeat or multi-turn work in one fixed tab/group (resident console)

## Quick Start

Install so that `perplexity` lands on your `PATH` — this matters because agents
often invoke a different interpreter than the one you ran `pip` with:

```bash
pipx install git+https://github.com/mfang0126/perplexity-toolkit.git
```

For development, install into the environment your agent actually runs:

```bash
git clone https://github.com/mfang0126/perplexity-toolkit.git
cd perplexity-toolkit
pip install -e .          # installs into the CURRENT environment only
```

Verify the command is reachable:

```bash
command -v perplexity && perplexity --help
```

## CLI

```bash
perplexity search "query"                            # Standard search
perplexity search "query" -m deep_research           # Deep research
perplexity search "query" -m model_council           # Model council
perplexity search "query" -f json                    # JSON output

perplexity batch -i queries.json -o results.json     # Batch from file
perplexity batch -i queries.json -o out.json -r      # Resume an interrupted batch

perplexity aggregate results.json -f markdown        # Aggregate (no browser needed)

perplexity history list --limit 20                   # List past conversations
perplexity history search "topic"                    # Find by title
```

Valid `-m/--mode` values: `search`, `deep_research`, `model_council`,
`step_by_step`. `history` requires an action (`list`, `search`, or `delete`).

## Resident console

One fixed WebBridge session (`perplexity-console`) = one tab group = one tab.
One task = one thread; every step is verified before it counts:

```bash
perplexity console ask "query" --task research-a   # creates or continues the task thread
perplexity console ask "follow-up" --task research-a
perplexity console ask "new topic" --new-thread --task other
perplexity console ask "review this" --file report.pdf   # attachments (<=8MB, verified chips)

perplexity console fill "q" [--file F]             # granular steps, joined by a staged-turn ledger
perplexity console submit | wait | extract          # each independently callable and retryable
perplexity console send "q"                         # fill + submit only
perplexity console attach --file F | files | detach NAME
perplexity console open <task|url> [--new-thread]

perplexity console models                           # list selectable models (badges + checked)
perplexity console model "Claude Sonnet 5"          # switch model (verified label readback)
perplexity console status | threads | selfcheck
```

Properties:

- **Gates, not best effort** — fill equality incl. editor state, user-turn
  ownership, completion signals, turn-scoped answer extraction; failures carry
  a machine-readable `error_code` and an evidence screenshot
  (`~/.perplexity-console/evidence/`).
- **Durable state** — `~/.perplexity-console/state.json` (session, group,
  per-task thread URL, staged turn). WebBridge session→tab mappings live only
  in the daemon; after a restart the console attach-or-recreates the tab from
  the saved thread URL.
- **Optional Jev judge** — `--judge` (or `PERPLEXITY_CONSOLE_JUDGE=1`) adds an
  advisory answer verdict and failure recovery hints; on failing fill/wait/
  extract steps the chosen remedy is **executed once** (bounded Jev-directed
  recovery: reload / wait-longer / retry, re-run under all original gates)
  while send paths stay advisory-only. One batched TypeSafe request, fail-open,
  validation-guarded. The pipeline never depends on it.
- Runs are logged to `~/.perplexity-console/runs.jsonl`.

## 4 Search Modes

| Mode | What It Does |
|------|-------------|
| Standard | Quick search with citations |
| Deep Research | Multi-step, thorough investigation |
| Model Council | Multiple models debate the answer |
| Step-by-step | Learning-oriented breakdown |

## Requirements

- Python 3.9+
- Google Chrome with the Kimi WebBridge extension, and the WebBridge daemon
  reachable at `http://127.0.0.1:10086/command`
  (override with `PERPLEXITY_WEBBRIDGE_URL`)
- A Perplexity account already logged in inside that browser (free tier works)

Every search mode drives the real browser through WebBridge; there is no API-key
or headless path. `aggregate` is the only subcommand that runs without a browser,
because it only post-processes result JSON you already fetched. The resident
console additionally keeps its own state under `~/.perplexity-console/`.
