# ⚙️ Lucid

  <img src="./assets/readme/hero.jpg" width="100%" alt="Lucid">

Nightly journal curator. Batch-processes OCAS skill journals via relevance

**Skill name:** `ocas-lucid`
**Version:** 3.0.0
**Type:** 
**Layer:** Execution
**Author:** Indigo Karasu

---

## 📖 Overview

Nightly journal curator. Batch-processes OCAS skill journals via relevance

---

## 🔧 Commands

- `lucid.status` to check last run, pending journals, filing stats
- `lucid.dream` -- run the full dream cycle immediately, ignoring the time gate
- `lucid.status` -- last run timestamp, journals pending, cumulative filing stats, streak count
- `lucid.init` -- create storage directories, initialize config and logs, register cron jobs
- `lucid.update` -- pull latest from GitHub source; preserves journals and data
- `mempalace_status`, `mempalace_search`, `mempalace_check_duplicate`, `mempalace_get_taxonomy` (read)
- `mempalace_add_drawer`, `mempalace_kg_add`, `mempalace_kg_invalidate` (write)
- `elephas.query` (optional, for pre-emission entity existence check)
- **`re_evaluations` can be `null` (not 0)** in older queue entries. Always use `e.get('re_evaluations') or 0` when comparing. Direct `>= 3` comparison against `null` returns `False` in Python and silently skips cleanup.

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [2.0.2] - 2026-04-26
- Changed
- [2.0.0] - 2026-04-13
- Changed
- Added
- Removed
- [1.0.0] - 2026-04-09
- Added

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.