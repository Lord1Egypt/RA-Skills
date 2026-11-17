---
name: grow
description: Use when the user wants the full Groundcrew growth loop on a site — survey, fix, verify, report — as one command, or one named phase of it (`--phase survey|fix|verify|report`).
---
# Grow

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion. Report output follows `references/reporting.md`.

Grow orchestrates other Groundcrew skills; it adds no data source of its own. Invoked without `--phase` it runs the loop in order and stops at every gate. `--phase` runs exactly one phase and stops.

## The loop

1. **survey** — establish current state: `site-audit` for defects, `ai-visibility` for answer-engine reach, `keyword-scout` for the keyword picture at the current tier. Output one prioritized finding list (critical first), each finding tagged with the skill that owns it and whether a safe automated fix exists.
2. **fix** — hand code-fixable findings to `fix-my-site`, one branch per root cause. Anything irreversible or outward-facing (content changes, redirects, robots policy, disavow-like actions) is proposed, never applied — the loop stops and waits for the owner. Skipped findings are recorded as skipped with the reason.
3. **verify** — prove what changed. Open mode: re-crawl the touched pages and diff against the survey observations. Connected: `POST /api/v1/sites/{slug}/trigger_audit` (write scope, explicit user intent; on `403` say when the next scheduled audit runs, on `429` wait — never stack retries), poll `GET /api/v1/sites/{slug}/jobs/{job_id}`, then read `GET /api/v1/sites/{slug}/issues?status=fixed` for closures. A fix nothing re-observed stays "applied, unverified".
4. **report** — package the cycle with the owning report skill (`weekly-report` for the period, `audit-report` for findings depth). Verdict rules come from `references/reporting.md`; a cycle whose fixes are unverified cannot say SHIP.

## Gates

Between phases the loop presents what it found, what it intends next, and stops when the next phase would write anywhere outside a local branch. One full pass is one cycle; the loop never self-restarts — the user starts the next cycle.

## When not to use

- One question about one surface → the owning skill directly (`site-audit`, `keyword-scout`, `ai-visibility`, `competitor-watch`).
- Only a document, no action → the report skills.
- Content production or publishing → `content-strategy` / `content-desk`; the loop does not write or publish content.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
