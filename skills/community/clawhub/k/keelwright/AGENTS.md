# AGENTS.md — keelwright

## What this skill does

keelwright is a coding agent skill that adds 28 machine-enforced safety checks to any
AI coding session. It is designed for non-programmers who use AI to write code.

## When to load this skill

- Before any vibe-coding or loop-coding session
- When running an autonomous or unattended agent
- When an agent swarm writes code a human will not review line by line
- Before committing a feature that touches auth, payments, or data

## Key behaviors

1. **Security gates R1–R12** run automatically on every iteration (SQL injection, hardcoded
   secrets, slopsquatting, business logic, auth). These cannot be disabled.

2. **Autonomy dial** controls what the AI can do alone:
   - Autopilot: unattended, escalates on blockers
   - Checkpoint: pauses at phase boundaries
   - Copilot: proposes, human approves

3. **Circuit-breaker** stops runaway loops: 50 iterations max, 5 no-progress cap,
   2-hour timeout, 3× same-error repeat.

4. **Plain-language reports**: every gate outcome is explained in words a non-coder
   understands. No jargon in user-facing messages.

5. **Risk glossary**: 28 named failure modes mapped to enforcement mechanisms.
   See `references/risk-glossary.md` for the full table (loaded on demand, not in SKILL.md).

## Do NOT

- Do not weaken or delete tests to make builds pass
- Do not bypass security gates even on Autopilot
- Do not invent scope without acceptance criteria
- Do not use `git add -A` when staging a project the agent is working in (stage by explicit path
  only, so bootstrap/qa artifacts are never committed by accident). NOTE: this rule is for
  agents USING the skill on a project — the skill's own repo maintenance may use `git add -A`
  deliberately.
- Do not trust self-reports from QA runs (verify on disk)
- **Do NOT hardcode any single agent runtime as if universal.** Keelwright ships on ClawHub,
  askill.sh, and skills.sh and is used on Hermes, OpenClaw, Cursor, Kilo, Codex, Cline, and more.
  NEVER reference the operator's private files (e.g. `a private operator repo's setup file` or any repo
  outside `ratingtesting/keelwright`). NEVER write `Hermes venv`, `<hermes-venv>`, or
  `hermes gateway restart` as if every user had them. Write fixes in runtime-neutral terms
  ("the agent's Python environment", "your agent runtime") so they work on any venv-based agent.
  Every file the skill references MUST live inside this repo. Universal + self-contained = mandatory.

## File structure

```
SKILL.md              — load this (the skill itself)
references/           — detailed patterns (load on demand)
  security-gates.md   — R1-R12 implementations
  circuit-breaker.md  — loop limits
  phases.md           — build loop phases
  writing-code.md     — coding discipline
qa-results/           — QA methodology README only (raw A/B run artifacts are gitignored local scratch)
scripts/              — validate_run.py, workspace_guard.py, check_update.py, web_heuristic_guard.py,
                       defense_health.py, attack_registry.py, verify_web_guard.py, export_skill.py, import_skill.py
templates/            — QA prompts
```
