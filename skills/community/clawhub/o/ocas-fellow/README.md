# ⚙️ Fellow

  <img src="./assets/readme/hero.jpg" width="100%" alt="Fellow">

Empirical experimentation engine. Invoked by Mentor to evaluate, compare, and promote improvements to OCAS skills, prompts, heuristics, and workflows using benchmark-driven experiments. Returns best variant result with lineage. Not user-invocable — called only by Mentor.

**Skill name:** `ocas-fellow`
**Version:** 2.6.5
**Type:** 
**Layer:** Execution
**Author:** <agent-name>

---

## 📖 Overview

Empirical experimentation engine. Invoked by Mentor to evaluate, compare, and promote improvements to OCAS skills, prompts, heuristics, and workflows using benchmark-driven experiments. Returns best variant result with lineage. Not user-invocable — called only by Mentor.

---

## 🔧 Commands

- `fellow.experiment.run` — execute an experiment cycle from Mentor invocation payload
- `fellow.experiment.status` — current experiment state if in progress
- `fellow.journal` — write journal for the current run; called at end of every run
- `fellow.update` — pull latest from GitHub source; preserves journals and data

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

- [2.6.5] - 2026-04-26
- Changed
- [2026-04-04] Spec Compliance Update
- Changes
- Validation
- [2.6.1] - 2026-04-08
- Storage Architecture Update
- [2.6.0] - 2026-04-08

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
