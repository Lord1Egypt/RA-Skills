# Context safety — handling Noveum's large responses

Several Noveum payloads are far bigger than an agent's context can afford. Pulling them
inline truncates them mid-JSON (corrupt data you may not notice) and crowds out the task.
This reference is the discipline for staying safe. **Violating it is the #1 way agents
fail with this platform.**

## Measured sizes (live production measurements — treat as lower bounds)

| Payload | Measured |
|---|---|
| 10 traces with `includeSpans=true` (mixed span counts, mostly small) | **171 KB** |
| ONE span-heavy trace by id (49 spans) | **145 KB** — size scales with `span_count`, not trace count; budget accordingly |
| Spans of one trace (`/traces/:id/spans`) | **132 KB** |
| Scorer catalog (`GET /v1/scorers`, ~130 scorers) | **169 KB** — fetch once, keep only the name→id/type map |
| 2 traces, no spans | ~3.5 KB (metadata-first querying is cheap) |
| `GET /v1/traces/filter-values` | ~25 KB on a quiet org — **grows with activity** (user/session id lists); fetch to disk on active orgs |
| Dataset items list with `fullContent=true` | easily **multiple MB** (voice items carry full transcripts + audio metadata) |
| NovaPilot report (`analysis` JSON) | hundreds of KB |
| AutoFix run state / quality report | hundreds of KB–MB |

The hosted MCP server truncates tool results at **200,000 characters** — a truncated
JSON body parses as garbage or silently loses items. Truncation is a hard signal you
used the wrong access pattern, never something to work around by "parsing what arrived".

## The rules

1. **Count before you fetch.** Use the cheap shape endpoints first:
   `GET /v1/datasets/:slug/items/ids` (ids only), `POST /v1/etl-jobs/:id/trace-filter-preview`
   and `POST /v1/novapilot/filter-preview` (counts), `span_count` filters on trace queries.
2. **Big things go to disk, not context.** REST: run
   `python scripts/fetch_to_file.py "/v1/...?..." --out /tmp/x.json` — it streams to a
   file and prints only `{savedTo, bytes, sha256}` + a 400-char head. Then inspect
   selectively: `jq`, `grep`, or a short python snippet that prints only what you need.
   Never `cat` the file or Read it whole.
3. **On MCP, prefer `@noveum/mcp-local`** — it exists exactly for this: mirrors the
   hosted tools but saves large bodies to local files and returns a tiny
   `{savedTo, bytes, sha256}` reference. On the hosted server, budget by **span count,
   not trace count** (one 49-span trace alone is ~145 KB): filter with `span_count_lte`
   or fetch metadata first, keep `includeSpans` requests to a handful of small traces,
   `size≤20` without spans, and page with `from`.
4. **Dataset items:** ids via `GET .../items/ids`; browse the default list view only in
   small pages (some fields are never truncated, so even the default list is unbounded on
   long-text datasets — and never QA content from it: truncation is silent and unmarked);
   for full content use the single-item `GET .../items/:itemId` (returns everything, no
   flag needed) or stream the whole list **to disk** with `fullContent=true`. Never
   `fullContent=true` inline on a list.
5. **Reports:** download once to disk (`fetch_to_file.py` on the report endpoint, or the
   `noveum://novapilot-report-markdown` resource saved via mcp-local), then read
   sections — recommendations first, evidence ids on demand.
6. **Traces:** query metadata first (no spans); fetch spans per-trace — to disk
   (`fetch_to_file.py "/v1/traces/<traceId>/spans"`) — only for the traces you actually
   inspect.
7. **Poll status on LIST/summary endpoints, not by-id.** Several by-id endpoints inline
   the full payload once work completes (NovaPilot `GET /reports/:id` carries the whole
   `analysis`; AutoFix runs carry the state/quality report). Poll the list for status;
   fetch the payload to disk exactly once when terminal.
8. **Never paste large payloads to the user.** Summarize, cite counts, and reference the
   saved file path.

## Recovery signals

- A tool result containing `… [truncated N chars]` or an unparseable tail → refetch to
  disk (rule 2/3); do not retry inline with a bigger limit.
- `fetch_to_file.py` prints `contentLength` in its summary and **fails (exit 2, partial
  file removed)** if the download is shorter than the server declared — never trust a
  file from a run that didn't exit 0.
