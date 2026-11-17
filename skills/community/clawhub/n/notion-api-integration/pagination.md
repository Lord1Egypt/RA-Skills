# Pagination — Cursors, Loops, and Resumability

Every list endpoint in this API is paginated at 100. A missing loop does not error: it returns the first page and the caller believes that is everything.

**Contents:** [Response Shape](#response-shape) · [The Loop](#the-loop) · [Paginated Endpoints](#paginated-endpoints) · [Cursors Are Not Checkpoints](#cursors-are-not-checkpoints) · [Stable Ordering for Long Scans](#stable-ordering-for-long-scans) · [Cost of a Full Scan](#cost-of-a-full-scan) · [Streaming Instead of Accumulating](#streaming-instead-of-accumulating)

## Response Shape

```json
{"object": "list", "results": [...], "next_cursor": "abc123", "has_more": true}
```

`has_more` is the only authority. `next_cursor` is `null` on the last page, and `results` can legitimately be shorter than `page_size` while `has_more` is still true — never infer the end from a short page.

## The Loop

```python
def fetch_all(url, body=None, rps=3):
    results, cursor = [], None
    while True:
        payload = dict(body or {}, page_size=100)
        if cursor:
            payload["start_cursor"] = cursor
        data = post(url, json=payload)          # with retry, see errors.md
        results.extend(data["results"])
        if not data.get("has_more"):
            return results
        cursor = data["next_cursor"]
        sleep(1 / rps)
```

```javascript
async function fetchAll(url, body = {}, rps = 3) {
  const results = [];
  let cursor;
  for (;;) {
    const data = await post(url, { ...body, page_size: 100, ...(cursor && { start_cursor: cursor }) });
    results.push(...data.results);
    if (!data.has_more) return results;
    cursor = data.next_cursor;
    await sleep(1000 / rps);
  }
}
```

- `page_size` comes from `default_page_size` in `config.yaml`; lower it only when rows are wide enough to make responses slow.
- The pacing line is not optional decoration: the limit is ~3 requests/second per integration and it is shared with everything else using that token (SKILL.md Rule 5).
- Official SDKs ship an iterator helper that hides this loop. It still spends the same rate budget, so it still needs pacing around it.

## Paginated Endpoints

| Endpoint | Max per page | Note |
|---|---|---|
| Database / data source query | 100 | The one that dominates every job |
| Block children | 100 | Per container — a deep page multiplies calls (`blocks.md`) |
| Search | 100 | Also index-lagged (`search.md`) |
| Users list | 100 | Rarely more than one page |
| Comments list | 100 | Per block |
| Page property item | 100 | The 25-entry escape hatch, itself paginated (`properties.md`) |

## Cursors Are Not Checkpoints

Cursors are opaque, tied to the query that produced them, and do not survive a process restart or a schema change. A job that stores `next_cursor` and dies has stored nothing useful.

**Resume by data, not by cursor.** Sort ascending by `created_time` (or by your `external_id`) and store the last value processed. On restart, add a filter for values after it. That resumes correctly even if the source changed while the job was down — and it is what `runs/<year>.md` records as `Last processed key` (`bulk.md`).

## Stable Ordering for Long Scans

The default order of a query without `sorts` is not guaranteed to be stable across pages. If rows are edited while you page through — and on a multi-minute export they will be — an unstable sort makes rows shift between pages, so some are read twice and some never.

- Full scans: `{"sorts": [{"timestamp": "created_time", "direction": "ascending"}]}`. Created time never changes, so the ordering is stable under concurrent edits.
- Incremental sync: sort ascending by `last_edited_time` and filter `on_or_after` the last watermark, accepting that a row edited twice is processed twice — make the write idempotent instead (`sync.md`).
- Never paginate a scan sorted by a property users edit.

## Cost of a Full Scan

Requests = ⌈rows ÷ 100⌉. Duration = requests ÷ `rate_limit_rps`.

| Rows | Requests | At 3 req/s |
|---|---|---|
| 500 | 5 | ~2s |
| 4,000 | 40 | ~14s |
| 50,000 | 500 | ~3 min |

Add one request per page for any truncated relation or rollup you need in full — that term dominates everything else (`properties.md`). State the estimate before running, not after.

## Streaming Instead of Accumulating

`fetch_all` returning a list is fine at 4,000 rows and wrong at 500,000. For large jobs, yield each page and process it:

- Write results to disk or to the destination per page, so a crash costs one page.
- Append the processed key to `runs/<year>.md` as you go, not at the end (`bulk.md`).
- Never hold the whole result set to compute something a running total can compute.
