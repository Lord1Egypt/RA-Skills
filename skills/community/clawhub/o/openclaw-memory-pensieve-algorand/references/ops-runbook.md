# Ops runbook

All operations are performed via MCP tools exposed by `server.py`.
No scripts, no venv, no shell commands needed for daily use.

## Daily sequence

### 1. Capture events (throughout the day)

```
pensieve_capture(content="...", source="manual", importance=0.7, tags=["..."])
```

Safe to call multiple times — deduplicates by content hash.

### 2. Dream cycle (end of day)

```
pensieve_dream_cycle()
```

Scans last 24 h of events and promotes recurring patterns into semantic,
procedural, and self_model layers.

### 3. Anchor to Algorand

```
pensieve_anchor()
```

Encrypts and commits today's memory to the blockchain. Idempotent — safe
to call more than once; skips if the same ledger tip is already anchored.

### 4. Validate

```
pensieve_validate()
```

Runs v2.1 hardening: chain integrity, decrypt, chunk hash verification,
parity checks. Trust recovery claims only when `ok=true`.

---

## Status check (any time)

```
pensieve_status()
```

Returns layer counts, chain tip, last anchor date, and today's cost estimate.

---

## Recovery

```
pensieve_recover(date="YYYY-MM-DD")
```

Inspect recovered data without writing files.

```
pensieve_recover(date="YYYY-MM-DD", restore=True)
```

Reconstruct memory from the blockchain and write files to `memory/recovered/`:

- `memory/recovered/events_recovered_YYYY-MM-DD.jsonl`
- `memory/recovered/semantic_recovered_YYYY-MM-DD.jsonl`
- `memory/recovered/procedural_recovered_YYYY-MM-DD.jsonl`
- `memory/recovered/self_model_recovered_YYYY-MM-DD.jsonl`

Prefers fetching note data from the blockchain via txid; falls back to the
locally cached `note_b64` if the indexer is unreachable.

---

## Expected tool outputs

### `pensieve_anchor`

```json
{"ok": true, "status": "anchored", "txid": "...", "multi_tx": false, "cost_algo_estimate": 0.001}
```
or
```json
{"ok": true, "status": "noop_already_anchored", "date": "YYYY-MM-DD"}
```
or (large payload)
```json
{"ok": true, "status": "anchored", "txids": ["..."], "multi_tx": true, "total_parts": 3}
```

### `pensieve_validate`

```json
{"ok": true, "local_events": 12, "onchain_events": 12, "issues": [], "warnings": [], "recovery_verdict": "PASS"}
```

### `pensieve_recover`

```json
{"ok": true, "date": "YYYY-MM-DD", "verified": true, "events": 12, "semantic": 4, "procedural": 1, "self_model": 0}
```

---

## Common failure signatures

- `events count mismatch local=X onchain=Y` — anchor may be incomplete; re-run `pensieve_anchor`
- `entry_hash set mismatch local vs onchain` — local file modified after anchor; investigate before recovery
- `content_hash mismatch` — data may be corrupted; do not trust recovery from this anchor
- `missing parts` — multi-TX anchor is incomplete; re-anchor if local data is intact
- `no anchored rows for date` — `pensieve_anchor` was never run for that date
