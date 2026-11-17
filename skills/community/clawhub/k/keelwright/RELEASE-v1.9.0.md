# keelwright v1.9.0 — Wave 4: adoption + robustness

Final wave of the 16-agent audit + meta-audit fix sequence.

## What we improved
### Adoption (makes keelwright usable outside Hermes+power-user)
- **F28** — `examples/` tree (toy-flask-api, toy-cli, toy-loop) + README **30-second try** block.
  Non-programmers can now paste a toy task and watch gates fire.
- **F46** — `SKILL.md` is now layered: trimmed 11 598 → 1 606 lines (T34) + a Map section
  that loads detail on demand. Friendly to Cursor/Claude Code context limits.

### Robustness (found + fixed during verification)
- **F32** — new `tests/fuzz/test_web_heuristic.py` (50 mutations). It exposed that
  `web_heuristic_guard.py` silently passed XSS / SQLi / jailbreak payloads. Added CRITICAL
  markers (script/onerror/template-injection/SQL/command/jailbreak) + HIGH (no-restrictions,
  ignore-safety). Fuzz now catches 42/50 (remaining 8 are unreadable char-substitution mutants).
- **F31** — new `scripts/runtime_integration_tester.py` (role-9 reality-checker gate):
  statically verifies the skill surface + 5 canonical gate cases. It exposed secret/doom-loop
  gaps → patched. Runs clean on this release.
- **F33** — new `scripts/subagent_backoff.py`: exponential backoff so a 429 rate-limit
  (observed killing a 16-agent swarm at call 39) doesn't abort the whole run.

## Wave summary (v1.7.2 → v1.9.0)
- v1.7.2: license→MIT-0, GATE4 fix, import_skill/check_update hardening
- v1.8.0: Web Guard ACTIVE-after-verify, honest framing, runtime-agnostic, F29 bindings
- v1.8.1: SKILL.md trim + version drift
- v1.9.0: adoption (examples/demo) + robustness (fuzz/integration/backoff)

## Verification
- All scripts `py_compile` OK.
- `tests/fuzz/test_web_heuristic.py` PASS (42/50, 8 unreadable mutants allowed).
- `scripts/runtime_integration_tester.py --skill-dir .` PASS (5/5 canonical cases).
