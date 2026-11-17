---
name: huawei-cloud-daily-hot-topics
description: |
  Query and display today's hot topics in one shot: fetch a ranked hot list
  (rank / title / hot value / source) from public, authentication-free hot-list
  REST APIs over HTTPS (read-only), normalise the results and print them as a
  readable Markdown table by default (plain text and JSON are also available).
  Providers are abstracted and tried in order, degrading to a bundled sample
  dataset — clearly marked as sample data — when the network or every provider
  is unavailable, so a single run always yields a readable result without
  crashing. Implemented with the Python 3 standard library only; it does not
  call the Huawei Cloud CLI, any Huawei Cloud SDK, or any Huawei Cloud REST
  API, requires no AK/SK credentials, and touches no cloud resource.
  Triggers include: "查询今日热点", "今日热点榜单", "热门话题", "今日热搜",
  "热点榜", "daily hot topics", "today hot list", "trending topics".
tags: [devtools, hot-topics, query, python, utility]
---

# Daily Hot Topics

## Overview

This skill answers "what is hot today?" in a single call. It fetches a ranked
hot-topic list from public, keyless hot-list REST endpoints (read-only over
HTTPS), normalises every provider into one shape, and renders a readable list.

- **One run, one ranked list** — a single execution returns today's hot topics
  with **rank / title / hot value / source**, up to `--top` entries.
- **Multiple providers, ordered degradation** — the default chain tries several
  public sources in order; the first success wins. `--source` pins a preferred
  provider while keeping the remaining providers as fallbacks.
- **Bundled offline fallback** — if the network is unavailable or every provider
  fails, the skill falls back to a bundled sample dataset and clearly labels it
  as **sample data** (non-real-time), so the command still exits 0 and stays
  readable instead of crashing.
- **Readable by default, machine-readable on demand** — Markdown (default),
  plain text, and JSON output; results can be written to a file.
- **Self-contained** — pure Python 3 standard library (only `urllib`), zero
  third-party dependencies, no credentials.

## Prerequisites

- **Python 3.8+** available as `python3` (or `python`) on `PATH`.
- **Outbound HTTPS** to the public hot-list endpoints is *optional*: without it
  the skill degrades to the bundled `scripts/sample_data.json` and still
  succeeds.
- No Huawei Cloud credentials, CLI (KooCLI), SDK, or AK/SK are needed; this
  skill never accesses Huawei Cloud resources.
- `scripts/sample_data.json` ships with the skill and is used only as the final
  fallback.

## Workflow

1. **Resolve the provider chain** — `resolve_chain(source)` returns the ordered
   list of providers to try: the default chain for `auto`, or the requested
   source first followed by the remaining default providers.
2. **Fetch each provider** — `fetch_source(name, timeout, retries)` performs a
   read-only HTTPS GET with a bounded timeout and a small retry budget, parses
   the JSON, validates the envelope, and normalises the records.
3. **Normalise** — `normalize(records, label)` maps heterogeneous fields into
   `{rank, title, hot, source, url}`, skipping records without a usable title.
4. **Degrade** — `fetch(...)` walks the chain; the first provider that returns a
   non-empty list wins. If all fail (or `--offline` is set), it loads the bundled
   sample dataset and marks the result as sample data, collecting a warning trail.
5. **Render** — `render_markdown()` / `render_text()` / `render_json()` turn the
   result into readable output, constrained to `--top` entries.
6. **Emit** — the result goes to standard output, or to a file when `--output`
   is given.

## Core Commands

```bash
# Default: today's hot list as a Markdown table (top 10)
python3 scripts/fetch_hot_topics.py

# Plain text, only the top 5
python3 scripts/fetch_hot_topics.py --format text --top 5

# Machine-readable JSON (parseable), top 3
python3 scripts/fetch_hot_topics.py --format json --top 3

# Pin a preferred provider (falls back to the other providers, then sample data)
python3 scripts/fetch_hot_topics.py --source zhihu --top 20

# Skip the network entirely and use the bundled sample dataset
python3 scripts/fetch_hot_topics.py --offline

# List the available providers
python3 scripts/fetch_hot_topics.py --list-sources

# Write the result to a file, with a longer timeout
python3 scripts/fetch_hot_topics.py --format markdown --timeout 30 --output hot.md

# Run the bundled unit tests (offline; HTTP is mocked)
python3 -m unittest discover -s tests -v
```

The command-line entry point is `scripts/fetch_hot_topics.py`. The bundled
`scripts/sample_data.json` is what the offline fallback reads by default.

## Parameter Confirmation

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `--top` | No | Number of entries to show | `10` |
| `--source` | No | Preferred provider: `auto`, `weibo`, `zhihu`, `douyin`, `vvhan` | `auto` |
| `--format` | No | Output format: `markdown`, `text`, or `json` | `markdown` |
| `--output` | No | Write the result to a file instead of stdout | stdout |
| `--timeout` | No | Per-request timeout in seconds | `20` |
| `--retries` | No | Retry attempts per provider | `2` |
| `--offline` | No | Skip the network and use the bundled sample dataset | off |
| `--list-sources` | No | Print the available providers and exit | off |

## Reference Documents

| Document | Description |
|----------|-------------|
| [references/usage-guide.md](references/usage-guide.md) | Command recipes, provider chain, offline behaviour, extending providers |
| [references/verification-method.md](references/verification-method.md) | How the skill is verified (offline unit tests + live read-only spot checks) |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria and out-of-scope items |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/iam-policies.md](references/iam-policies.md) | Permission notes (none required) |

## Notes

- The skill is **read-only**: it fetches public hot lists over HTTPS and writes
  only to standard output or a user-chosen `--output` file. It never touches a
  cloud resource and never persists fetched data.
- Degradation is explicit: when the network or providers fail, the fallback
  result is flagged as **sample data** and a warning trail is printed, so a
  sample list is never mistaken for a live ranking.
- The exit code is `0` on success (including fallback to sample data); a non-zero
  code is returned only for invalid arguments or when `--output` cannot be written.
- Third-party public endpoints are not under our control; providers are easy to
  replace or extend by editing the `PROVIDERS` registry in the script.