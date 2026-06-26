# Job Watch – Initial Setup (Skill‑Owned Memory)

## First Run Instructions

When the skill runs for the first time, it will look for these three files inside its own folder:

~/.openclaw/workspace/skills/job-watch/memory/
├── platforms.md
├── profile.md
└── scoring.md

If any are missing, the skill will ask you to provide the missing information.

### 1. Platforms (`platforms.md`)
List each platform on a new line with a dash:
```markdown
- dreamjob.ma
- Glassdoor
```

### 2. Profile (`profile.md`)
Use the format shown in the example above (desired roles, skills, experience, location, salary).

### 3. Scoring (`scoring.md`)
Define weights and matching rules as shown in the example.

## Testing the Skill

Send a message to OpenClaw:
```
run job watch now
```

## Scheduling (Cron)

You can schedule the skill using OpenClaw’s cron.