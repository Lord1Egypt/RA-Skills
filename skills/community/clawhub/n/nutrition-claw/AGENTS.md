# Agent Instructions

## Keeping the skill in sync

After every change to `SKILL.md`, run:

```bash
./scripts/sync-skill.sh
```

This copies `SKILL.md` to `~/.openclaw/workspace/skills/nutrition/SKILL.md` so the openclaw agent always sees the latest version. **Do not skip this step — an outdated skill file will cause the agent to give wrong guidance.**
