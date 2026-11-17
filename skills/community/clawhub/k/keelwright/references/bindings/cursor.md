# keelwright binding — Cursor

Cursor is an agentic editor. To use keelwright's engine here, wire its rules so the loop
runs the same gates as on any other runtime.

## Setup (runtime-neutral)
- Place `keelwright` rules in your project's `.cursor/rules/` (or `.cursorrules`) by
  pointing at the skill's `SKILL.md` summary + the gate checklist from `references/security-gates.md`.
- The Web Guard auto-injection plugin is **Hermes-only**; on Cursor you enable the equivalent
  by adding a rule that runs `scripts/detect_guard.py` before any web tool call and surfaces
  DEGRADED/UNPROTECTED to the user.

## Commands (replace with your stack)
- test / lint / build / quality: use your project's own CLI. keelwright's gates are
  stack-agnostic — only the per-stack command names live in this file.

## Web Guard
- Before ANY web fetch, run: `python <keelwright>/scripts/detect_guard.py`
- If not ACTIVE, tell the user (plain language) before proceeding.
- Heuristic backstop: `python <keelwright>/scripts/web_heuristic_guard.py --text "..."`

keelwright itself is MIT-0. This binding is instructions only.
