# keelwright binding — Hermes

Hermes is the runtime that ships this skill natively. The gate checklist and loop
phases load automatically via the `keelwright` skill manifest. This binding only
documents the Web Guard surface and the skill-tree path discovery.

## Setup (runtime-neutral)
- Skill root discovery: `KEELWRIGHT_SKILLS` env var, or the runtime's default skills dir.
- Web Guard: Hermes uses the auto-injection plugin (`keelwright.web-guard`) when enabled;
  the underlying probe is still `scripts/detect_guard.py`. If the plugin is disabled,
  run `scripts/detect_guard.py` before web trips and surface the verdict.

## Commands (replace with your stack)
- test / lint / build / quality: your project's CLI. keelwright's gates are stack-agnostic.

## Web Guard
- Before ANY web fetch: `python <skill_dir>/scripts/detect_guard.py`
- If not ACTIVE, tell the user before proceeding.
- Heuristic backstop: `python <skill_dir>/scripts/web_heuristic_guard.py --text "..."`

keelwright is MIT-0. This binding is instructions only.
