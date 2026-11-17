# ⚙️ Genie

<img src="./assets/readme/hero.jpg" width="100%" alt="Genie">

**Skill name:** `ocas-genie`
**Version:** 1.8.2
**Type:** workflow
**Layer:** infrastructure
**Author:** Indigo Karasu

---

## Overview

Genie is a VPS disk-space monitor and safe-cleanup skill. It audits the
filesystem, identifies cleanup targets by risk tier, estimates the space each
target would reclaim, and executes only deletions that cannot reduce
functionality. Databases are analyzed read-only and never repaired or
VACUUMed automatically.

## Usage

All modes run from `scripts/genie.py`:

```bash
python3 scripts/genie.py --assess            # read-only report (default mode)
python3 scripts/genie.py --clean --dry-run   # preview what --clean would do
python3 scripts/genie.py --clean --tier 1    # execute Tier 1 (safe) cleanup
python3 scripts/genie.py --analyze           # Tier 3 read-only analysis
python3 scripts/genie.py --discover          # rescan filesystem, refresh the manifest
python3 scripts/genie.py --json              # machine-readable output
```

Tiers: **1** = safe (caches, stale tmp, aged logs and snapshots),
**2** = low risk (requires confirmation), **3** = analysis-only (never
auto-deleted).

## Safety rules

- A bare invocation is read-only (`--assess`); nothing is deleted without
  an explicit `--clean`.
- Age-based cleanup is designed to protect the newest snapshot/backup —
  verify survival after every `--clean` (see Known Issues in `SKILL.md`).
- Failed deletions are reported and left in place, never retried
  destructively.
- Every run appends a record to the skill journal
  (`commons/journals/ocas-genie/runs.jsonl`).

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition, procedure, and known issues |
| `scripts/genie.py` | The assessment and cleanup engine |
| `scripts/genie_rebuild_fts.py` | FTS index rebuild helper |
| `tests/` | Regression tests (clone-deletion safety gate) |
| `references/` | Operational notes, pitfalls, and worked examples |

## Documentation

Read `SKILL.md` for operational detail, tier definitions, and validation
rules. Read `references/` for detailed specifications and postmortems.

## License

MIT License — see `LICENSE`.
