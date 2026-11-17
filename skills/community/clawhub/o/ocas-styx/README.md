# ⚙️ Styx

  <img src="./assets/readme/hero.jpg" width="100%" alt="Styx">

Transaction data store with merchant enrichment. Provides a clean, queryable

**Skill name:** `ocas-styx`
**Version:** 1.4.0
**Type:** 
**Layer:** data-science
**Author:** <agent-name>

---

## 📖 Overview

Transaction data store with merchant enrichment. Provides a clean, queryable

---

## 🔧 Commands

- `<hermes-home>/data/transactions.db` — raw Plaid transaction data (1,187 transactions, last: 2026-06-24)
- `<hermes-home>/data/styx.db` — enriched merchant data (1,193 transaction_merchants links, 493 merchants)
- `m.category IN ('restaurant', 'cafe', 'bar', 'food')` for dining
- `m.category IN ('grocery', 'supermarket', 'food_store')` for food shopping
- **`query.py --health-check` does not exist** — Use inline Python to verify DB integrity instead.
- **`google_auth_mcp` import path is profile-dependent** — When running under the `indigo` Hermes profile, `Path.home()` returns `<hermes-home>/profiles/indigo/home` instead of `/root`. Scripts that do `sys.path.insert(0, str(Path.home() / '.hermes' / 'scripts'))` or `sys.path.insert(0, str(AGENT_ROOT / 'scripts'))` will fail to find `google_auth_mcp.py`. **Fix:** Hardcode `sys.path.insert(0, str(Path('<hermes-home>/scripts')))` in any script that imports `google_auth_mcp`. **Affected scripts (all fixed as of 2026-06-04):** dispatch: `triage.py`, `check_unread.py`, `gmail_search.py`, `gmail_scan.py`; taste: `email_scan.py`, `run_historical_scans.py`; scripts: `email_check.py`, `dream_journal_pipeline.py`.
- **`llm_resolve.py` does NOT work in cron/background context** — The script calls `hermes ask --no-stream` via subprocess, which returns no output when there is no interactive session.
- `styx_universal_enrich.py` is at `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/` (NOT `<hermes-home>/commons/data/ocas-styx/`)
- `taste_full_enrich.py` may report "Failed: N" for items that need LLM resolution. This is a known cron limitation (`llm_resolve.py` calls `hermes ask` which returns no output without an interactive session). Items will be retried on the next non-cron enrichment run.

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


## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.