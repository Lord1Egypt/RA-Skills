# henry-skill-installer

Purpose: scaffold new skills inside <workspace>/skills safely.

Rules:
- Never delete files unless explicitly told.
- Only write within /Users/clawdbot/.openclaw/workspace/skills/
- Prefer /usr/bin/tee for writes and verify by /bin/cat afterwards.
- Never print tool JSON; call exec.

Workflow:
1) Ask for skill name + 1-paragraph spec.
2) Create folder workspace/skills/<name>/
3) Generate SKILL.md + minimal files.
4) Verify skill appears in `openclaw skills list`.
