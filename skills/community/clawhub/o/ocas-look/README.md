# ⚙️ Look

  <img src="./assets/readme/hero.jpg" width="100%" alt="Look">

Converts user-provided images into validated, decision-ready action drafts. Routes images by inferred intent across domains: events from flyers, macros from meal photos, places to save, products to price, receipts to log, documents to file, civic issues to report. Supports reverse image search via Yandex and Google. NOT for generic OCR, computer vision research, or surveillance.

**Skill name:** `ocas-look`
**Version:** 2.5.2
**Type:** 
**Layer:** ocas-look
**Author:** <agent-name>

---

## 📖 Overview

Converts user-provided images into validated, decision-ready action drafts. Routes images by inferred intent across domains: events from flyers, macros from meal photos, places to save, products to price, receipts to log, documents to file, civic issues to report. Supports reverse image search via Yandex and Google. NOT for generic OCR, computer vision research, or surveillance.

---

## 🔧 Commands

- `look.ingest.image` — ingest image(s) with optional EXIF and device pre-parse
- `look.propose.actions` — generate ActionDrafts with DecisionRecords
- `look.execute.action` — execute a confirmed draft (requires explicit approval)
- `look.rollback.action` — attempt rollback for reversible actions
- `look.status` — last ingest, pending drafts, items awaiting confirmation
- `look.config.set` — update configuration
- `look.journal` — write journal for the current run; called at end of every run
- `look.update` — pull latest from GitHub source; preserves journals and data
- `lookup.reverse_search` — perform Google reverse image search on an image URL or local file. Returns matching pages, titles, and similar image URLs.

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

- [2.4.5] - 2026-04-26
- Changed
- [2026-04-04] Spec Compliance Update
- Changes
- Validation
- [2.4.1] - 2026-04-08
- Storage Architecture Update
- [2.4.0] - 2026-04-08

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
