# Stage 3.3 — History

> Phase 3 (Govern). Keep a timestamped record of the data surface over time.

## Purpose

Maintain historical snapshots so consumers can see data over time, not just the current state, and so changes are auditable.

## Inputs

- Each file written by distribute (2.3).

## Logic

1. On every successful write of a file `F`, copy it to `{family}-ws/data/history/{epoch-ms}_{F}` where `{epoch-ms}` is the current Unix time in **milliseconds** (date alone is not granular enough — multiple passes can occur within a second). Source `{epoch-ms}` from the shell command in core-engine "Obtaining the Current Timestamp" — never from an internal/hosted time tool.
2. The snapshot is the exact bytes written (including the metadata envelope), so `$generatedOn` inside it records the logical generation time and the filename prefix records the snapshot time.
3. Snapshots are append-only; DFE never edits an existing snapshot.

## Output

`history/{epoch-ms}_{file}.json` per write.

## Retention

- Default: **forever**.
- A package may declare a retention policy in its `SOURCE_MAP.md` (e.g. keep last N, or keep T days).
- Pruning happens only in cleanup (3.4) — history (3.3) never deletes.

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| Write failed validation | No snapshot (only successful writes are snapshotted). |
| Identical content to last snapshot | Still snapshotted (timestamped) — keeps an honest timeline; cleanup can dedupe later if a policy requests it. |
