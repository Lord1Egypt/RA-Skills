# keelwright binding — Kilocode

Kilocode is an agentic runtime. Wire keelwright's gates through its equivalent of
project rules / AGENTS.md so the loop runs the same checks as on any other runtime.

## Setup (runtime-neutral)
- Point Kilocode's rules at keelwright's gate checklist (`references/security-gates.md`)
  and loop phases (`references/phases.md`).
- Web Guard auto-injection is Hermes-only; on Kilocode add a pre-tool rule that runs
  `scripts/detect_guard.py` and surfaces the verdict.

## Commands (replace with your stack)
- test / lint / build / quality: your project's CLI. keelwright's gates are stack-agnostic.

## Web Guard
- Before ANY web fetch: `python <skill_dir>/scripts/detect_guard.py`
- If not ACTIVE, tell the user before proceeding.
- Heuristic backstop: `python <skill_dir>/scripts/web_heuristic_guard.py --text "..."`

keelwright is MIT-0. This binding is instructions only.
