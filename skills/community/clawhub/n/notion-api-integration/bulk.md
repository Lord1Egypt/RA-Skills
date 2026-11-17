# Bulk Work — Imports, Exports, Backfills

Volume changes the problem. At 50 rows everything works; at 5,000 the job is dominated by the rate limit, by partial failure, and by what happens when it is re-run.

**Contents:** [Budget the Job First](#budget-the-job-first) · [The Four Rules of a Restartable Job](#the-four-rules-of-a-restartable-job) · [Importing From Another Tool](#importing-from-another-tool) · [Backfilling a Property](#backfilling-a-property) · [Exporting a Workspace](#exporting-a-workspace) · [Concurrency](#concurrency) · [The Dry Run](#the-dry-run) · [Reporting](#reporting)

**Before starting or restarting any bulk job**, read `runs/<year>.md` and the relevant `mappings/<source>-to-notion.md` if `## Boxes` names them. A rerun that has not read the mapping creates duplicates nobody will find.

## Budget the Job First

Requests, then duration, stated before the first call.

| Job | Requests | 5,000 records at 3 req/s |
|---|---|---|
| Read all rows | ⌈rows ÷ 100⌉ | 50 requests, ~17s |
| Read all rows + full relations | rows + ⌈rows ÷ 100⌉ | 5,050 requests, ~28 min |
| Create rows (properties only) | 1 per row | 5,000 requests, ~28 min |
| Create rows with an idempotency check | 2 per row | 10,000 requests, ~56 min |
| Create rows with content blocks | 1 + ⌈blocks ÷ 100⌉ per row | 2 per row typical, ~56 min |
| Update one property on every row | 1 per row + the read | ~28 min |
| Upload and attach a file per row | ≥3 per row | 15,000 requests, ~1h 23m |

Formula: duration = requests ÷ `rate_limit_rps`. If the answer is hours, say so before starting — the design conversation ("do we need the idempotency check on the first run?") only happens if the number is on the table.

## The Four Rules of a Restartable Job

1. **Checkpoint by data, never by cursor.** Cursors expire and do not survive a restart. Sort ascending by `created_time` or by the external key, and store the last key processed in `runs/<year>.md` as you go (`pagination.md`).
2. **Write the mapping as you create.** One row appended to `mappings/<source>-to-notion.md` per created page, immediately — not accumulated in memory and flushed at the end, because the crash happens before the flush.
3. **Make creation idempotent.** Before creating, filter the target on `external_id`: `{"property": "external_id", "rich_text": {"equals": "recAbc123"}}`. One extra request per row buys a rerun that is safe. Skip it only on a first run into an empty target, and say that you skipped it.
4. **Collect failures, do not abort on them.** A 400 on row 812 is a data problem with row 812. Log the id and the message, continue, and report the list at the end. Aborting turns one bad record into a job nobody can finish.

## Importing From Another Tool

1. **Model first.** Decide property types from the queries you will run, not from the source's column types (SKILL.md Data Model Defaults). Record the decision in `artifacts/decision-<what>.md`.
2. **Create the target schema with `external_id` in it** from the start (`databases.md`). Adding it later is a second full pass.
3. **Import 10 records. Open them in the UI.** Wrong select options, truncated text and mangled dates are visible in ten seconds and invisible in a JSON response.
4. **Run the rest with checkpointing**, pacing at `rate_limit_rps`, appending to the mapping.
5. **Reconcile**: count rows in the target, compare to the source, and query for rows with an empty `external_id` — those are pre-existing or duplicated.
6. **Relations last.** They need both sides to exist. Import both sources, then a second pass that reads the mapping and writes the relation values — which is exactly why the mapping file exists.

Source-specific friction worth expecting: attachments (`files.md`), long text over the 2,000-character rich text cap, users that must be resolved to Notion ids (`users.md`), and formulas that have no equivalent and must be computed and written as plain values.

## Backfilling a Property

- Query only the rows that need it — `{"property": "external_id", "rich_text": {"is_empty": true}}` — rather than every row. The filter is free and the writes are not.
- One write per row, and a write bumps `last_edited_time` on every page it touches. If a polling sync watches that field, a backfill looks like the whole workspace changed at once (`sync.md`). Pause the sync or raise its watermark deliberately.
- Under `write_mode: confirm-writes`, state the affected count from the query before the first write.

## Exporting a Workspace

- Rows are the cheap part; **content is the expensive part** — one request per container per 100 children, recursive (`blocks.md`).
- Full relations need the property-item endpoint per page (`properties.md`).
- Files must be downloaded as you walk, because the URLs expire (`files.md`).
- Unsupported block types return empty. Count them and report the count rather than shipping a silently lossy export.
- Write to disk per page. An export that holds everything in memory dies at the size where you most needed it.

## Concurrency

- The rate limit is per integration, so parallel workers do not go faster — they go 429. Two or three workers behind one shared token bucket smooth out latency; more just add retries.
- Appends to the same parent must be sequential or the block order interleaves (`blocks.md`).
- A single central pacer is the only design that survives a cron job running at the same time as an interactive session on the same token.

## The Dry Run

With `write_mode: dry-run`, the job prints what it would send and runs nothing. What a good dry run reports:

- Total requests and estimated duration at `rate_limit_rps`
- Counts by action: create, update, skip-because-already-mapped
- The first three payloads in full, so property names can be eyeballed against the schema box
- Every validation problem detectable without the API: text over 2,000 characters, select values not in the schema's option list, unresolvable user names, missing required title

## Reporting

**Every bulk run gets its row in `~/Clawic/data/notion-api-integration/runs/<year>.md`** — date, job, target, attempted, created, updated, failed, last processed key, measured duration, whether 429s appeared — written while it runs, not after. Per-record failures go in the failure list under that run. The id pairs go to `mappings/<source>-to-notion.md`. If the procedure is worth repeating, the runbook goes to `artifacts/runbook-<what>.md`, with its `## Boxes` line written in the same turn.

Without those rows, the next session cannot tell a finished import from one that stopped at 60%, and the only safe assumption — start over — is the expensive one.
