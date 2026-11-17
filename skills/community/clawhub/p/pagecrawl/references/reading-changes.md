# Reading what changed

## Contents
- Fewest calls for common questions
- Polling from an automation
- Evidence and screenshots
- What to avoid
- Output formats

## Fewest calls for common questions

| Question | Calls |
|---|---|
| "What changed today?" | `get-changes-since(since="today", min_priority=50)`, then `get-check-diff` for the ones worth describing |
| "Give me this week's summary" | `get-summary(period="7d")`, then `get-changes-since(since="7 days ago", min_priority=50)` |
| "What are the prices right now?" | `list-monitors(search="...")` to find the IDs, then one `get-latest-values(monitor_ids=[...])` |
| "What changed on X last time?" | `get-check-diff(monitor_id="X")`; without `check_id` it returns the latest check that found a change |
| "How has X moved over time?" | `get-monitor-history(monitor_id="X", changes_only=true, limit=20)` |
| "Which monitors need my attention?" | `list-monitors(has_unseen=true, sort_by="latest_change")` |
| "Find what we monitor about a topic" | `search(query="...")`, then `fetch(id="...")` for the results that matter |

`get-summary` accepts the periods `today`, `yesterday`, `24h`, `7d`, `30d` and `90d`, or a `since` and `until`. It returns counts by importance, active and paused monitors, the numeric monitors that moved and by how much, and a timeline of recent changes.

`get-changes-since` returns up to 200 changes per call (`limit`, default 50), each with `monitor_name`, `checked_at`, `ai_summary`, `priority_score` (importance, 0 to 100), the changed values, and the IDs needed for `get-check-diff`. `min_priority` filters on the server, which is faster than filtering afterwards.

## Polling from an automation

To collect only new changes on a schedule:

1. First call: `get-changes-since(since="24 hours ago")`.
2. Store `next_cursor` from the response. It is returned even when there are no changes.
3. Every later call: `get-changes-since(after_check_id=<stored next_cursor>)`. Results come oldest first, nothing is repeated, and nothing is skipped.

Do not move `since` forward between calls: a moving date either repeats changes or misses ones that landed mid-request. For pushing changes to another system as they happen, a webhook is better than polling; see [automation.md](automation.md).

## Evidence and screenshots

- `get-screenshot(monitor_id="...")` returns the latest stored screenshot as an image. Pass `check_id` for an earlier check, or `element_id` for one tracked element. It never fetches the live page.
- `get-archive` reads stored archives of a capture, for monitors with archiving turned on:
  - `get-archive(action="wayback-calendar", monitor_id="...")` lists the days with a capture.
  - `get-archive(action="wayback-resolve", monitor_id="...", as_of="2026-03-01")` finds the capture current on that date.
  - `get-archive(action="info", monitor_id="...", check_id=123)` describes one capture, with its timestamp proofs and links.
  - `get-archive(action="verify", monitor_id="...", check_id=123)` says whether the archive still matches what was sealed.
- Archives show what a page said on a date. Point the user to the capture's link rather than restating it as fact.

## What to avoid

- Calling `get-monitor-history` once per monitor to build a digest. `get-summary` and `get-changes-since` answer for every monitor in one call.
- Describing a change from `ai_summary` alone. Read `get-check-diff` first.
- Loading the live page to confirm a change, or calling `trigger-check` to refresh before answering. The stored result is the answer; say when it was checked.
- Reporting every change at equal weight. Lead with the highest `priority_score`.

## Output formats

Daily or weekly briefing:

```
This week: <n> notable changes across <m> pages (<k> minor ones not listed).

1. <Monitor name>: <what changed, with old and new values>. <Why it matters>. Importance <score>. <link>
2. ...
```

A numeric change reads best with both values, for example "Netflix US pricing: the Standard plan rose from $15.49 to $17.99 a month (+16%)."

Rules for any format:

- Say what changed in plain words, from the diff, with old and new values for numbers (and the percentage when it helps).
- Include each monitor's `link` so the user can open the change in PageCrawl.
- Group related changes (several pages of one competitor, one product across shops).
- When nothing significant changed, say so in one line, for example "Nothing notable changed this week; 6 minor edits on 4 pages."
- Use dates and times from the results (`checked_at`), in the user's timezone if known.
