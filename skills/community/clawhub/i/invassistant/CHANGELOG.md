
# Changelog — InvAssistant

Complete release history for the `invassistant` skill.

This file is **authoritative**. `SKILL.md` carries only a pointer to it, and the recent-releases table in `README.md` / `README_zh.md` is an abridged digest of this file.

Split out of `SKILL.md` at **v2.3.17**: the table itself had grown to **3181 B / 13.1%** of the file that is read on every invocation, where none of it is actionable. Same rule as note **D10** — keep the always-read file executable, move the chronology to a companion.

Merged from both previous tables, so nothing recorded anywhere was dropped: `SKILL.md` supplied 16 releases, the two READMEs 12 and 11 rows, of which 2 had never been recorded in `SKILL.md`. Where the files paraphrased the same release differently, the longer wording is kept and the shorter is only logged, not lost.

## Releases

| Version | Date | Summary |
|---------|------|---------|
| v2.3.19 | 2026-09-20 | LP1 fix: frontmatter `permissions` block added (Yahoo Finance quote endpoint used by `data_fetcher.py`, user-configured webhook URLs used by the optional `send_*.py` helpers, notification credential env-var names) + `network` capability token in `allowed-tools` — declaring in the frontmatter the outbound behaviors the body already disclosed; data-transmission notice corrected (the quote fetcher also transmits off-machine, previously mis-stated as send-helper-only) |
| v2.3.17 | 2026-09-17 | Restructure: §12 and §13 moved to `references/capital_plan_audit.md` and `references/derived_price_governance.md`, leaving the operating spine inline (the five-step loop, what a clean validator run does not tell you, the A1-A5 detection table). No rule text deleted — all of it relocated verbatim and cross-linked from §12/§13 and from the Reference Files table. Splitting so that the always-read file does not have to be skimmed, which is the same failure mode D10 addresses inside a registry |
| v2.3.16 | 2026-09-17 | Add D9 (an unsettled question needs its own ledger — one absorptive register, a per-entry blocking scope, adjudication deliberately outside pass/fail, mirrors that replicate values but not disputes) + D10 (keep the registry executable and move chronology to a companion file; guard the shape, not only the size; derive size targets from a measured floor) + the "a green validator is not an action permit" rule in D4 + mistakes P11/P12 |
| v2.3.15 | 2026-09-16 | Hardening per scanner findings: valuation gate + volume confirmation fail-closed in `redline_engine.py`; Framework Scope and Bundled Scripts section; allowed-tools completion; data-transmission notices; pinned requirements |
| v2.3.14 | 2026-09-11 | Add D8 (example configs carry no author positions — sample tickers must be generic and must never coincide with real holdings, because a shipped example that mirrors your book is a disclosure, not a demo) + P10; purged real tickers from `scripts/init_config.py` sample watchlist and from two inline code comments |
| v2.3.13 | 2026-09-11 | Add D7 (every balance carries an as-of and source; account corrections ship with a cash rollforward; arbitrate broker-vs-exchange by tier; never quote a rounded display) — prompted by a 6-week-stale cash field that produced a phantom discrepancy, while derived price levels already had eight mechanical checks |
| v2.3.12 | 2026-09-11 | Add D6 (capital-base resolution — caps resolve against the owning account; ratify historical practice, never sum mixed-basis account blocks) + definition-backfill principle. Frame D1-D5 list as §13 D1-D7 |
| v2.3.11 | 2026-09-11 | Add §13 Derived Price Level Governance (D1-D5) + P8/P9 — anchor-window declaration, single source of truth for levels, mirror discipline, and mechanical level validation |
| v2.3.10 | 2026-09-08 | Add not-individualized-advice disclaimer to risk_control_and_overrides.md (scanner finding) |
| v2.3.9 | 2026-09-07 | *(summary never recorded in any source file)* |
| v2.3.3 | 2026-08-07 | Sync SKILL.md version declaration with ClawHub package metadata |
| v2.3.2 | 2026-06-06 | Fix display name (remove Clean suffix) |
| v2.3.1 | 2026-06-06 | Major cleanup: English SKILL.md, clean frontmatter, bilingual README, no personal scripts |
| v2.1.2 | 2026-06-06 | Audit cleanup: bilingual README, remove legacy files |
| v2.1.1 | 2026-06-04 | Mode D: A-class candidate zone entry (no observation delay) |
| v2.1 | 2026-05-18 | A/B/C asset classification; 7 red lines; 4-factor QMS; trailing stop removed from A-class |
| v2.0 | 2026-05-18 | Full rebuild: decision pyramid, 5-factor QMS, 10 red lines (replaced by v2.1) |
| v1.5.x | 2026 Q1-Q2 | 3-condition engine, dual-mode entry, trailing stops, behavioral patches |
| v1.0 | 2026-01 | Initial: 3 red lines entry + multi-layer exit engine |

> `v1.5` and `v1.5.x` were two renderings of the same release line, one in each source file. They are merged into `v1.5.x` with the fuller wording rather than listed twice.

> `v2.3.1` and `v2.1.2` are both dated 2026-06-06 and both describe a cleanup release. They were recorded in different files under different numbers; they are kept separate here rather than silently merged, because nothing establishes which is the duplicate.

> Rows for `v2.3.4`–`v2.3.8` were never recorded in either source file. The gap is preserved rather than invented.
