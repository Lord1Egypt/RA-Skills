# Cron Enrichment Gotchas

## `llm_resolve.py` fails silently in cron context

**Symptom:** After a cron enrichment run, the log shows "Resolved 0 via LLM" and unresolved transactions pile up in `review_queue.jsonl` even though they could be resolved.

**Cause:** `llm_resolve.py` calls `hermes ask --no-stream` via `subprocess.run()`. In cron/background sessions there is no interactive Hermes session to answer, so the subprocess returns empty stdout. Every transaction gets classified as "unresolved" and written to the review queue.

**Detection:** After a cron enrichment run, check the review queue for duplicate entries (same transaction ID queued multiple times) — this indicates repeated cron runs without LLM resolution ever succeeding.

**Fix — manual LLM pass:**
```bash
python3 <hermes-home>/skills/ocas-styx/scripts/llm_resolve.py
```
Or process the queue directly using the `ask` tool in an interactive session.

**Fix — accept review queue as fallback:** When SearXNG is down AND running in cron, partially-redacted transactions will reach Stage 4 and land in the review queue. This is correct behavior — the review queue IS the fallback for unresolvable-in-automation transactions.

## Cross-database queries require ATTACH

When querying across `transactions.db` and `styx.db`, you must use `ATTACH DATABASE` — two separate `sqlite3.connect()` calls cannot join across databases in Python:

```python
import sqlite3
styx = sqlite3.connect('<hermes-home>/data/styx.db')
styx.execute("ATTACH DATABASE '<hermes-home>/data/transactions.db' AS txdb")
# Now query: SELECT ... FROM txdb.transactions t JOIN transaction_merchants tm ...
```

## Taste pipeline items fail LLM enrichment in cron

**Symptom:** `taste_full_enrich.py` reports "Failed: N" (usually 1–3 items).

**Cause:** Taste items that need LLM-based resolution (e.g., restaurant name extraction from ambiguous merchant names) rely on the same `llm_resolve.py` subprocess pattern. In cron context, these return empty.

**Impact:** Minimal. The failed items remain in the Taste items queue (`items.jsonl` with `enriched: false`) and will be retried on the next interactive run. They are NOT lost.

**Action needed:** None. Report the failures in the cron summary but do not treat them as pipeline errors. Do NOT attempt manual retry in cron context.

## `styx_universal_enrich.py` re-enriches already-known merchants when no new transactions exist

**Symptom:** Cron runs show "Enriching N merchants" even when `MAX(date)` in transactions.db hasn't advanced.

**Cause:** The script queries for merchants where Google Places might have better data, not just strictly unenriched ones. When no new transactions are pulled by Plaid sync, it still re-queries a small batch (5–15) of existing merchants against Google Places.

**Impact:** None — these are idempotent re-queries. `no_result` responses are expected for garbled names that Google can't match. Existing enrichment (searxng, plaid_merchant_name, internal) is preserved.

**Action needed:** None. Report "0 enriched, N failed (no_result)" as normal when no new transactions exist.

## Script path confusion in cron invocations

**Symptom:** Cron job instructions reference `<hermes-home>/commons/data/ocas-styx/styx_universal_enrich.py` but this path does not exist.

**Cause:** The commons data directory was part of an older data layout. Current scripts live under the profile-specific skills directory.

**Correct paths:**
- `styx_universal_enrich.py`: `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/`
- `taste_full_enrich.py`: `<hermes-home>/commons/data/ocas-taste/scripts/`
- `taste_signals_dedup.py`: `<hermes-home>/commons/data/ocas-taste/scripts/`

**Fix:** Always use the paths above. If a cron invocation specifies a different path, substitute the correct one rather than failing.