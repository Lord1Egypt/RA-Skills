# keelwright binding — OpenClaw

OpenClaw is a multi-agent runtime (ClawHub ecosystem). keelwright ships there too; wire the
engine via a hook.

## Setup (runtime-neutral)
- Add a hook that, on each agent turn, loads keelwright's gate checklist
  (`references/security-gates.md`) and loop phases (`references/phases.md`).
- Web Guard: OpenClaw can use `web-agent-security-gate` (MIT-0, ClawHub) OR run
  `scripts/detect_guard.py` directly. Surface DEGRADED/UNPROTECTED to the operator.

## Commands (replace with your stack)
- test / lint / build / quality: your project's CLI.

## Web Guard
- Before ANY web fetch: `python <keelwright>/scripts/detect_guard.py`
- If not ACTIVE, tell the user before proceeding.
- Heuristic backstop: `python <keelwright>/scripts/web_heuristic_guard.py --text "..."`

keelwright is MIT-0. This binding is instructions only.
