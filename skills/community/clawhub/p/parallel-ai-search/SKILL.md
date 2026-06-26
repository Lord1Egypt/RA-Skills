---
name: parallel-ai-search
description: Use Parallel's parallel-cli to do live web search, URL extraction (clean markdown), deep research reports, bulk data enrichment (CSV/JSON), FindAll entity discovery, and web monitoring. Use when the user asks to look something up online, needs current sources/citations, provides URLs to read or summarise, requests deep/exhaustive research, wants to enrich a dataset with web-sourced fields, wants a list of entities (companies/people/places), or wants to monitor the web for changes over time.
compatibility: Requires parallel-cli installed + authenticated (PARALLEL_API_KEY or parallel-cli login) and internet access.
metadata:
  author: openclaw
  version: "2.0.0"
  homepage: "https://docs.parallel.ai/integrations/cli"
  openclaw: '{"emoji":"🔎","primaryEnv":"PARALLEL_API_KEY","cli":"parallel-cli"}'
allowed-tools: Bash(parallel-cli:*) Bash(curl:*) Bash(pipx:*) Read
---

# Parallel AI Search (CLI Master)

This is a **single “master” skill** that replaces the earlier Node-script-based version of `parallel-ai-search`.

It routes to the right `parallel-cli` capability for the task:

- **Search**: quick web lookup with citations (`parallel-cli search`)
- **Extract**: turn URLs (including PDFs and JS-heavy pages) into clean, LLM-ready text (`parallel-cli extract`)
- **Deep research**: multi-source reports with processor tiers (`parallel-cli research ...`)
- **Enrich**: add web-sourced columns to CSV/JSON (`parallel-cli enrich ...`)
- **FindAll**: discover entities from the web with optional enrichments (`parallel-cli findall ...`)
- **Monitor**: track web changes on a cadence, optionally via webhook (`parallel-cli monitor ...`)

## Routing rules (pick ONE)

Choose the smallest / cheapest action that solves the user’s request:

1. **Extract** — if the user gives one or more URLs *or* says “read/summarise this page”, “extract”, “quote”, “pull the content”, “what does this page say”.
2. **Deep research** — ONLY if the user explicitly asks for *deep*, *exhaustive*, *comprehensive*, *thorough investigation*, or a multi-source “report”.
3. **Enrich** — if the user provides a list/table (CSV/JSON/inline objects) and wants new columns like CEO, revenue, funding, contact info, etc.
4. **FindAll** — if the user wants you to **discover many entities** (companies/people/venues/etc.) that match criteria.
5. **Monitor** — if the user wants **ongoing tracking** (“alert me”, “track changes”, “monitor this weekly”) rather than a one-off answer.
6. **Search** — default for everything else that needs current web info or citations.

Optional manual prefixes if the user invoked this skill directly:
- `search: ...`
- `extract: ...`
- `research: ...`
- `enrich: ...`
- `findall: ...`
- `monitor: ...`

If a prefix is present, honour it.

## Setup and authentication (only when needed)

Before running any Parallel command, ensure auth works:

```bash
parallel-cli auth
```

If `parallel-cli` is missing, install it:

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

If you cannot use the install script, use pipx:

```bash
pipx install "parallel-web-tools[cli]"
pipx ensurepath
```

Then authenticate (choose one):

```bash
# Interactive OAuth (opens browser)
parallel-cli login

# Headless / SSH / CI
parallel-cli login --device

# Or environment variable
export PARALLEL_API_KEY="your_api_key"
```

## Output & citation rules

- **Always cite web-sourced facts** with inline markdown links: `[Source Title](https://...)`.
- **End with a Sources list** whenever you used Search/Extract/Research output.
- Prefer **official/primary** sources when available.
- For long outputs, save to files in `/tmp/` and summarise in-chat.

## Search (default web lookup)

Use Search for fast, cost-effective answers with citations.

### Command template

```bash
parallel-cli search "$OBJECTIVE"   --mode agentic   --max-results 10   --json
```

Add any of these only when relevant:
- `--after-date YYYY-MM-DD` (freshness constraint)
- `--include-domains a.com b.org` (restrict sources)
- `--exclude-domains spam.com` (block sources)
- one or more `-q "keyword query"` flags (extra keyword probes)
- `-o "/tmp/$SLUG.search.json"` (save full JSON to a file)

### Parse + respond

From the JSON results, extract **title**, **url**, and any **publish_date** / **excerpt** fields.
Answer the user’s question, and cite each claim inline.

## Extract (read one or more URLs)

Use Extract when you need the actual contents of specific URLs (webpages, PDFs, JS-heavy sites).

### Command template

```bash
parallel-cli extract "$URL" --json
```

Add when relevant:
- `--objective "Focus area"` (e.g., pricing, API usage, constraints)
- `--full-content` (only if the user needs the whole page)
- `--no-excerpts` (if you only want full content)
- `-o "/tmp/$SLUG.extract.json"` (save full JSON to a file)

### Respond

- If the user asked for a **summary**, summarise with citations to the extracted URL.
- If the user asked for the **verbatim text**, provide the extracted markdown *only if it is reasonably sized*; otherwise provide the key sections + offer to read more from the saved output.

## Deep research (only when explicitly requested)

Deep research is slower and may cost more than Search. Use it only when the user explicitly wants depth.

### Step 1 — start (always async)

```bash
parallel-cli research run "$QUESTION" --processor pro-fast --no-wait --json
```

Parse `run_id` (and any monitoring URL) from JSON and tell the user the run started.

### Step 2 — poll (bounded timeout)

Choose a short slug filename (lowercase-hyphen), then:

```bash
parallel-cli research poll "$RUN_ID" -o "/tmp/$SLUG" --timeout 540
```

- Share the **executive summary** printed by the poll command.
- Mention the output files:
  - `/tmp/$SLUG.md`
  - `/tmp/$SLUG.json`

If polling times out, re-run the same poll command — the run continues server-side.

## Enrich (CSV/JSON or inline data)

Use Enrich to add web-sourced columns to structured data.

### Step 1 — (optional) suggest columns

```bash
parallel-cli enrich suggest "$INTENT" --json
```

Use this when the user knows the goal but not the exact output schema.

### Step 2 — run (always async for large jobs)

For CSV:

```bash
parallel-cli enrich run   --source-type csv   --source "input.csv"   --target "/tmp/enriched.csv"   --source-columns '[{"name":"company","description":"Company name"}]'   --intent "$INTENT"   --no-wait --json
```

For inline JSON rows:

```bash
parallel-cli enrich run   --data '[{"company":"Google"},{"company":"Apple"}]'   --target "/tmp/enriched.csv"   --intent "$INTENT"   --no-wait --json
```

Parse `taskgroup_id` from JSON.

### Step 3 — poll

```bash
parallel-cli enrich poll "$TASKGROUP_ID" --timeout 540 --json
```

After completion:
- Tell the user the output file path (the `--target` you chose).
- Preview a few rows (using file read tools if available) and report row counts.

If poll times out, re-run it — the job continues server-side.

## FindAll (entity discovery)

Use FindAll when the user wants you to discover a set of entities (e.g., “AI startups in healthcare”, “roofing companies in Charlotte”, “YC devtools companies”).

### Step 1 — run

```bash
parallel-cli findall run "$OBJECTIVE" --generator core --match-limit 25 --no-wait --json
```

Useful options:
- `--dry-run --json` to preview schema before spending money
- `--exclude '[{"name":"Example Corp","url":"example.com"}]'` to avoid known entities
- `--generator preview|base|core|pro` (core default; pro for hardest queries)

Parse `run_id` from JSON.

### Step 2 — poll + fetch results

```bash
parallel-cli findall poll "$RUN_ID" --json
parallel-cli findall result "$RUN_ID" --json
```

Respond with:
- total entities found
- a clean list/table of the best matches (name + URL + key attributes)
- any caveats about ambiguous matches

## Monitor (web change tracking)

Use Monitor when the user wants ongoing tracking.

Create:

```bash
parallel-cli monitor create "$OBJECTIVE" --cadence daily --json
```

Optional:
- `--cadence hourly|daily|weekly|every_two_weeks`
- `--webhook https://example.com/hook` (deliver events externally)
- `--output-schema '<JSON schema string>'` (structured events)

Manage:

```bash
parallel-cli monitor list --json
parallel-cli monitor get "$MONITOR_ID" --json
parallel-cli monitor update "$MONITOR_ID" --cadence weekly --json
parallel-cli monitor delete "$MONITOR_ID"
parallel-cli monitor events "$MONITOR_ID" --json
parallel-cli monitor simulate "$MONITOR_ID" --json
```

Respond with the monitor id and how to retrieve events (or confirm webhook delivery).

## Reference material

- Copy/paste command templates and patterns: `references/command-templates.md`
- Troubleshooting common failures: `references/troubleshooting.md`
