# keelwright binding — Cline

Cline is a VS Code agentic extension. Configure its rules folder to run keelwright's gates.

## Setup (runtime-neutral)
- Add keelwright's gate checklist (`references/security-gates.md`) and loop phases
  (`references/phases.md`) to your Cline rules (e.g. `.clinerules` or project rules).
- Web Guard auto-injection is Hermes-only; on Cline add a pre-tool rule that runs
  `scripts/detect_guard.py` and surfaces the verdict.

## Commands (replace with your stack)
- test / lint / build / quality: your project's CLI.

## Web Guard
- Before ANY web fetch: `python <keelwright>/scripts/detect_guard.py`
- If not ACTIVE, tell the user before proceeding.
- Heuristic backstop: `python <keelwright>/scripts/web_heuristic_guard.py --text "..."`

keelwright is MIT-0. This binding is instructions only.
