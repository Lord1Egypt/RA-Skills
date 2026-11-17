# Stage 3.4 — Cleanup

> Phase 3 (Govern). Prune historical snapshots per retention policy or explicit request. The only stage that deletes.

## Purpose

Keep `history/` from growing unbounded, while never touching the current data surface.

## Inputs

- `{family}-ws/data/history/` snapshots.
- Retention policies (per-package, declared in SOURCE_MAP) and/or an explicit `--before {timestamp}`.

## Logic

`DAT__ cleanup --before {epoch-ms}`:
1. Enumerate `history/{epoch-ms}_{file}` snapshots.
2. Delete those whose `{epoch-ms}` prefix is strictly less than the given timestamp.
3. Report: count deleted, count retained, bytes freed.

Policy-driven cleanup (no explicit timestamp):
1. For each package with a declared retention policy, apply it (keep last N snapshots, or keep snapshots newer than T).
2. Packages without a policy default to **forever** (never auto-pruned).

## Output

A pruned `history/` + a cleanup report. Current data files and `REGISTRY.json` are never touched.

## Safety

- Cleanup operates ONLY within `history/`. It never deletes a current data file, a schema, the registry, the manifest, or `dfe-state.md`.
- Deletion is reported, not silent. A dry-run variant lists what *would* be deleted before acting when the set is large.

## Future

A per-family config package for retention-policy changes is a recorded idea (not in v1.0).
