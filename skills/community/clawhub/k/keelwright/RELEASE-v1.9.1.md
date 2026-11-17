# keelwright v1.9.1 — runtime-agnostic fix (remove Hermes venv hardcode)

Hotfix reported by the owner: the "universal" skill still referenced `Hermes venv` /
hardcoded Hermes paths as if universal — contradicting the runtime-agnostic mandate
that v1.7.1 started and v1.8.0 bindings completed.

## What changed
- `scripts/import_skill.py`: `HERMES_SKILLS` → `KEELWRIGHT_SKILLS`; `find_hermes_skills_dir()`
  → `find_skills_dir()` now scans Hermes / OpenClaw / Cursor / Codex / Cline + neutral
  `~/.keelwright`; **default install path is now `~/.keelwright/skills`** (not `AppData/Local/hermes`).
- `scripts/export_skill.py`: default skill path → `~/.keelwright/skills/keelwright`.
- `references/bindings/python.md`: "hermes venv" → "agent runtime venv".

## Verification
- `py_compile` OK on both scripts.
- `find_skills_dir()` returns the neutral `~/.keelwright/skills` default when no runtime
  path exists on disk (no longer assumes Hermes).
- No `HERMES_SKILLS` / `find_hermes_skills_dir` symbols remain in code.

This is the final cleanup so keelwright is genuinely runtime-neutral across Hermes,
OpenClaw, Cursor, Codex, Cline, and any venv-based agent.
