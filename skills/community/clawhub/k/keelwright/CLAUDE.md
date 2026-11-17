# CLAUDE.md — keelwright

## Quick context

keelwright is a vibe/loop coding skill for non-programmers. It adds 28 machine-enforced
safety checks (OWASP, secrets, slopsquatting, reward hacking, doom loops, etc.) to any
AI coding session.

## Load order

1. `SKILL.md` — the full skill (phases, gates, autonomy dial, risk glossary)
2. `references/security-gates.md` — when implementing R1-R12 checks
3. `references/circuit-breaker.md` — when setting loop limits
4. `references/phases.md` — for build loop phase details

## Critical rules

- Security gates R1-R12 are **never** disabled, even on Autopilot
- Never delete or weaken tests (reward-hacking guard)
- Stage files by explicit path: `git add file1 file2` — never `git add -A` when working in a
  project the agent is modifying (bootstrap/qa artifacts must not be committed by accident).
  The skill's own repo maintenance may use `git add -A` deliberately.
- Plain language for all user-facing messages (no jargon)
- Verify on disk, never trust self-reports
- **Keep the skill runtime-agnostic.** Keelwright is published on ClawHub, askill.sh, and
  skills.sh and is used on Hermes, OpenClaw, Cursor, Kilo, Codex, Cline, and more — not only
  Hermes. NEVER reference the operator's private files (e.g. `a private operator repo's setup file` or
  any repo outside `ratingtesting/keelwright`). NEVER hardcode `Hermes venv`, `<hermes-venv>`,
  or `hermes gateway restart` as if universal. Write fix instructions in runtime-neutral terms
  ("the agent's Python environment", "your agent runtime") so they work for any venv-based agent.
  Every file the skill references MUST live inside this repo. Universal + self-contained = mandatory.

## Architecture (5 layers)

- L0: Human (goals + acceptance criteria → plain-language reports)
- L1: Control (autonomy dial, triage, phase 1-2, loop design)
- L2: Build loop (write → gates → verify → commit → repeat)
- L3: Supervision (circuit-breaker, stability, self-learning)
- L4: Production lifecycle (observe → analyze → fix → validate → learn)

## KDS (Keelwright Score)

Measures skill impact: KDS = ER × DR / 100 (0-100 scale).
Best: Laguna S 2.1 = 83. Weak models = 0 (can't execute tests).
