# Wayback (Internet Archive) Fallback for `sift.fetch`

A recovery tier for `sift.fetch` that pulls a dead or hard-blocked page's closest
Internet Archive (Wayback Machine) snapshot when live retrieval has genuinely
failed. It is **recovery-only**, never a default primary path.

## Why this exists (and why it is scoped the way it is)

`dondai1234/Hound` shipped a similar archive auto-fallback and **deleted it in
v10.4.1** for two reasons: latency added to every hard-blocked fetch, and
unreliability. Both objections are answered by design here:

- **Latency objection → answered.** This is a *final* tier, invoked only after
  live + Jina have already failed on a confirmed hard-block. A successful live
  fetch never touches it, so normal fetches pay zero cost.
- **Unreliability objection → answered.** Hard 8s wall-clock timeout (two
  network calls share one budget); pure stdlib + optional `html2text` (no new
  hard dependency); archive.org rate-limits from datacenter IPs are contained by
  the timeout and degrade to a clean "unavailable" rather than a hang.

The one residual risk the original lacked discipline on — **stale-as-fresh
poisoning** — is handled explicitly: every recovered envelope forces
`source='archive.org'`, `archived_at`, `content_age_days`, and `is_stale=True`,
so downstream synthesis and `ocas-sift` fact-verify cannot mistake a years-old
snapshot for live content.

## When to fire

Fire the Wayback tier ONLY on a **confirmed hard-block** — never on soft
failures where a retry helps:

- **Fire:** page-gone (`404` / `410` / `451`), or a bot/auth wall where live is
  genuinely impossible (and webwright stealth also failed, if it was tried).
- **Do NOT fire:** soft `429` / `5xx` (retries can still recover live), or any
  case where a fresh live fetch is plausibly reachable.

Pass `archive_fallback=true` on a deliberate dead-page-recovery request to opt in
explicitly; for routine fetches the agent may auto-try Wayback only after the
full live chain (Scrapling → Jina → webwright → stealth) is exhausted on a hard
block. It is never enabled by default for perf-sensitive bulk contexts.

## How to call

```bash
# Recover and print recovered Markdown (exit 0 = recovered, 1 = nothing):
python3 scripts/wayback_fallback.py <url>

# Get the full envelope (source, archived_at, content_age_days, is_stale, …):
python3 scripts/wayback_fallback.py <url> --json
```

From Python: `from scripts.wayback_fallback import recover; env = recover(url)`.
Merge `env` into the `sift.fetch` response envelope, surfacing
`source` / `archived_at` / `content_age_days` / `is_stale` so both the user and
downstream skills see the content is **archived, not live**.

## Envelope fields (mirror the sift.fetch ResponseModel)

| Field | Meaning |
|---|---|
| `source` | `"archive.org"` when recovered; distinguishes from `"live"` |
| `archived_at` | ISO date of the snapshot; `""` when none |
| `url` | The `web.archive.org/web/<ts>id_/<url>` snapshot URL |
| `content` | Extracted Markdown (html2text if available, else minimal strip) |
| `content_ok` | `True` only if a usable snapshot was extracted |
| `status` | HTTP status of the snapshot fetch (0 if no snapshot) |
| `content_age_days` | Days between snapshot and now; `None` if unknown |
| `is_stale` | Always `True` when `source='archive.org'` |
| `next_action` | `"archive_recovered"` / `"archive_unavailable"` |

## Implementation notes

- **Availability first.** Calls `https://archive.org/wayback/available?url=`
  (CDX) for a fast existence probe before fetching the snapshot.
- **Clean snapshot.** Uses the `id_` (un-rewritten) variant so broken image
  rewrites and banner injection are minimized; extraction is higher quality.
- **Compression handled.** Sends `Accept-Encoding: identity` and defensively
  decodes gzip/deflate/brotli so the body is never binary garbage.
- **Excluded/blocked detection.** Snapshots flagged "excluded from the Wayback
  Machine" / `robotstxt` / empty are reported as unavailable, not as content.
- **Timeout budget.** `TOTAL_TIMEOUT_S = 8.0` is the cap for BOTH calls combined;
  if it blows, bail with `content_ok=False`.

## Relationship to SearXNG

SearXNG (via `web_search`) is the **discovery** layer — it finds URLs for a
query. The Wayback tier is the **retrieval** layer — it recovers the body of an
*already-known, now-dead* URL. They are not interchangeable: SearXNG cannot
recover a specific dead page's body, only surface live alternates. If the goal is
"find a *live* alternate source for rotted content," use `sift.search` (SearXNG)
to discover a fresh URL, then `sift.fetch` it — do not confuse that path with
this dead-URL recovery tier.

> **`archive_error` is not `no snapshot`.** The availability API can be down —
> it returned HTTP 502 on 2026-08-17 — and the script used to report that
> identically to a genuinely unarchived URL. It now returns
> `next_action: "archive_error"` with presence marked UNKNOWN. Treat that as
> "retry later", never as "this page was never archived".
