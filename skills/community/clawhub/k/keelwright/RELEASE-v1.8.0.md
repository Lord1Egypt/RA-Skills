# keelwright v1.8.0 — Wave 2 audit fixes + adoption

Second wave of fixes from the 16-agent security audit + meta-audit (reality-checker role).
Builds on v1.7.2. All changes backward-compatible, non-blocking.

## What we improved (Wave 2)

### License & attribution
- **T8** — removed `references/qa-results-20260721.md` (stale CC BY 4.0 historical log; R10 memory-poisoning vector).
- **T9** — added `NOTICE-MIT` (copyright + SPDX provenance of every adapted source).
- **T10/T45** — SPDX-License-Identifier tags on all source credits (gweber/hermes-injection-guard, scastile/hermes-agent-defense, web-agent-security-gate).

### Web Guard / security
- **T11** — `detect_guard.py` no longer reports ACTIVE on deps-present alone. ACTIVE now requires a passing `verify_web_guard.py` smoke test. Fixes the false-ACTIVE trap (broken/MITM'd classifier looked "ACTIVE").
- **T13** — `attack_registry.redact_url` now strips userinfo (`user:pass@host` no longer logged).
- **T14** — `web_heuristic_guard.py` MEDIUM markers are advisory-only (no longer raise a blocking FLAGGED).
- **T15** — new `scripts/breaker.py`: enforceable circuit-breaker with file-backed counters (the 4 caps from SKILL.md are now machine-enforced, not just read by the agent).
- **T16** — new `scripts/check_model_pin.py` + `model-pin.json`: R9 model-version-drift check is now enforceable.

### Honest framing
- **T17** — SKILL.md description split: most modes have a machine-enforced detector + a discipline rule; a few (style, sycophancy) are discipline-only. No more "machine-enforced — not prompt suggestions" overclaim.
- **T19** — architecture.md: ZERO COST (not ZERO INSTALL).
- **T22** — self-healing → self-learning.
- **T33** — workspace_guard: MECHANICAL → TRIPWIRE.

### Runtime-agnostic
- **T23/T24** — export/import use env-overridable skill paths; verify_web_guard docstring runtime-neutral.
- **T35** — plugin author → ratingtesting.
- **T38** — attack_registry default → `./.keelwright`.
- **T41** — check_update warns on offline instead of silent pass.

### Doc sync
- **T27** — security-gates header R1-R12 (was R1-R11).
- **T29** — removed fake `keelwright load` CLI from README.
- **T31** — workspace isolation how-to added.
- **T32** — `MERGE-MATRIX.md` + `AUDIT-STRATEGY.md` now in the repo.
- **T37** — web-guard.md Hermes-specific paths honestly marked.

### Process / adoption
- **T44** — R10 guard: `references/historical/` never auto-loaded into agent context.
- **T46/T48** — `references/bootstrap/` audited (safe templates).
- **T47** — new `.github/workflows/security.yml`: pip-audit + license check on PR.
- **F29** — new bindings for **Cursor, Codex, Cline, OpenClaw** (runtime-agnostic mandate is now real, not just words).

## Files changed
scripts: breaker.py (new), check_model_pin.py (new), detect_guard.py, attack_registry.py, web_heuristic_guard.py, validate_run.py, check_update.py, verify_web_guard.py, export_skill.py, import_skill.py, workspace_guard.py, + copyright headers on all.
references: security-gates.md, attack-registry.md, web-guard.md, provenance.md, bindings/{cursor,codex,cline,openclaw}.md (new).
root: NOTICE-MIT (new), MERGE-MATRIX.md (new), AUDIT-STRATEGY.md (new), model-pin.json (new), .github/workflows/security.yml (new), LICENSE/llms.txt/architecture.html/web-guard.md/README.md/SKILL.md/architecture.md/plugin.yaml.

## Verification
- All scripts pass `py_compile`.
- redact_url strips userinfo (tested).
- MEDIUM markers = advisory (tested).
- License residual scan clean (except historical release-notes).
