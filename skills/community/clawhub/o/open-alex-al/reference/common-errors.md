# Reference — Common Errors

The three errors you will actually hit with OpenAlex, their causes, and the correct agent reaction. **No API key is involved**, so none of these are auth problems.

---

## 1. HTML 404 (bad ID or path)

**What you see:** the server returns a typed "not found" error (it detects the HTML 404 page OpenAlex serves for missing IDs/paths and converts it).

**Cause:** wrong ID prefix, a typo, a deleted/merged entity, or an unknown `path` in `openalex_request`.

**Reaction:**
1. Check the prefix matches the entity (`W/A/I/S/T/C/P/F`).
2. Re-resolve the entity:
   ```json
   { "tool": "openalex_search", "arguments": { "entity": "works", "query": "<title>", "per_page": 1 } }
   ```
3. Use the returned `id` with `openalex_get`. Do **not** retry the same bad ID.

---

## 2. `429 Too Many Requests`

**What you see:** rate-limit response; the server retries with backoff, but it can still surface if sustained.

**Cause:** requests are not in the polite pool, or the agent is firing too fast / scanning broadly.

**Reaction:**
1. **Set `OPENALEX_MAILTO=you@example.com`** — the polite pool is rarely throttled. This is the primary fix.
2. Back off and reduce volume.
3. Use **cursor** paging instead of rapid `page` bursts.
4. Cache resolved IDs so you don't re-search repeatedly.

---

## 3. Empty results (not an error)

**What you see:** `results: []` with a server note. HTTP status is fine.

**Cause:** the `filter` is too narrow, a filter key/value is misspelled, or the search terms don't match.

**Reaction:**
1. Relax filters one at a time (drop `is_oa`, widen the year range).
2. Verify keys (`authorships.author.id`, `primary_topic.id`, …).
3. Try `search` instead of an exact `filter`.
4. **Say the result is empty** — never fabricate papers to fill a list.

---

## Quick map

| Error | Cause | First action |
|-------|-------|--------------|
| HTML 404 | Bad ID/path | Re-resolve via search/autocomplete; fix prefix. |
| `429` | No polite pool / too fast | Set `OPENALEX_MAILTO`; back off; use cursor. |
| Empty results | Filter too narrow | Broaden; check spelling; try `search`. |
| `400` | Bad filter syntax | Comma-separate; `key:value`; verify keys. |
| Timeout | Query too broad | Add a filter; lower `per-page`. |

> Verification needed: confirm error semantics with the MCP build and <https://docs.openalex.org>.
