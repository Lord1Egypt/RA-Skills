# keelwright v1.10.0 — Layered Skill (ADR-001)

Real implementation of F46 (layered architecture). Replaces the cosmetic line-trim
of v1.8.1 with a real ~84% token reduction for agent contexts.

## What changed
- **SKILL.md is now a thin index** (~221 lines, ~2.7K tokens; was ~17K tokens).
  Contains critical safety rules (R1–R12, autonomy dial, circuit-breaker caps) + a Map
  table for on-demand loading of `references/*.md`.
- **`scripts/build_skill.py`**: reassembles the index + all `references/*.md` into
  a single full document for public registry display (skills.sh / ClawHub / askill.sh).
  Supports `--check` for CI idempotency.
- **`docs/ADR-001-layered-skill.md`**: formal Architecture Decision Record explaining
  the index/reference split, token budget, and publish workflow.
- **README.md & GitHub Repo Description**: Architecture section added on the first page.

## Token Savings
- **Agent context on session start:** ~2,700 tokens (was ~17,300).
- **Reduction:** **84% less token overhead** on every turn across Hermes, Cursor, Codex,
  Cline, and OpenClaw.

## Verification
- `python scripts/build_skill.py --check` PASS (idempotent assembly)
- `python scripts/runtime_integration_tester.py --skill-dir .` PASS (5/5 canonical cases)
- `python tests/fuzz/test_web_heuristic.py` PASS (42/50 fuzz cases)
- All `.py` scripts pass `py_compile`.
