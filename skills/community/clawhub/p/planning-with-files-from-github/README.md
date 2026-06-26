# planning-with-files — OpenClaw Skill

Manus-style persistent markdown planning for OpenClaw. Port of [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files).

## Install

### Option A: Personal skill (all agents)
```bash
mkdir -p ~/.openclaw/skills
cp -r planning-with-files ~/.openclaw/skills/
chmod +x ~/.openclaw/skills/planning-with-files/scripts/*.sh
```

### Option B: Workspace skill (one project)
```bash
mkdir -p <your-workspace>/skills
cp -r planning-with-files <your-workspace>/skills/
chmod +x <your-workspace>/skills/planning-with-files/scripts/*.sh
```

### Option C: Via clawhub (if published)
```bash
clawhub install planning-with-files
```

## Verify

In OpenClaw chat:
```
/skills
```
You should see `planning-with-files 📋` in the list.

## Use

```
/planning-with-files  →  start a planning session
```

Or the agent will auto-activate for complex multi-step tasks.

## Required Permissions

The scripts use `exec` tool. Make sure your config allows it:

```json
{
  "tools": {
    "allow": ["group:runtime", "group:fs"]
  }
}
```

## File Structure

```
planning-with-files/
├── SKILL.md              ← main skill (OpenClaw reads this)
├── scripts/
│   ├── init-session.sh   ← creates 3 planning files
│   └── check-complete.sh ← verifies all phases done
├── templates/
│   ├── task_plan.md      ← goal + phases tracker
│   ├── findings.md       ← research + decisions
│   └── progress.md       ← session log
└── references/
    └── workflow.md       ← detailed workflow docs
```

## Differences from Claude Code Version

- No hooks (PreToolUse/PostToolUse/Stop) — behaviors encoded in SKILL.md instructions instead
- Uses `exec` tool for scripts instead of Claude Code plugin hooks
- Uses `{baseDir}` for script path resolution
- Works with any OpenClaw agent (not just Claude)
