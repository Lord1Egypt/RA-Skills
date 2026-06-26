# Quick Start Guide

> Get your Personal Agent running in 15 minutes.

## Prerequisites

- Claude Desktop with Cowork mode, or Claude Code CLI
- A folder on your computer for your knowledge base
- (Optional) Obsidian for graph visualization

## Step 1: Get the Files (2 min)

**Option A**: Clone from GitHub
```bash
git clone https://github.com/YOUR_USERNAME/memory-work.git my-vault
```

**Option B**: Download ZIP from GitHub releases

## Step 2: Connect to Claude (1 min)

1. Open Claude Desktop → Cowork mode
2. Select the downloaded folder as your workspace
3. Claude automatically reads CLAUDE.md

## Step 3: Initialize (5 min)

Say **"Start"** or **"开始工作"** to trigger initialization.

Claude will:
1. Ask your preferred language (English / 中文)
2. Set up files automatically
3. Have a casual chat to learn about you
4. Create your first weekly workspace

**Tips**:
- Be natural — talk about what you're actually working on
- Don't worry about structure — Claude organizes your thoughts
- You can always update your profile later

## Step 4: Your First Week (5 min)

Tell Claude what you're working on. Just talk naturally:

> "This week I need to finish the quarterly report, prep for Thursday's client meeting, and review the new hire's code."

Claude will break this into tasks, search your library, ask clarifying questions, and offer to generate a calendar file.

## Step 5: Daily Use

- Talk to Claude about work progress
- Share new thoughts and ideas
- Ask for help with specific tasks
- Claude remembers context from earlier in the week

## Step 6: Weekend Review

Say **"Let's do a review"** or **"复盘"** at week's end.

Claude will show memory operations, ask for feedback, calibrate strategy, archive completed work, and set up next week.

## What Happens Under the Hood

When you start a conversation, Claude automatically:
1. Checks current date/time
2. Reads your weekly file
3. Checks memory log for recent calibrations
4. Loads personality preferences from SOUL.md
5. Matches relevant memories from MEMORY.md

You don't manage any of this manually.

## Customization

### Adding Zones
Create folders (e.g., `03 ProjectA/`) with zone agent files.

### Adding Skills
Create skill folders in `06 Skills/` with SKILL.md files.

### Adjusting Personality
Edit SOUL.md to change communication style, humor, proactiveness.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Claude doesn't read files | Ensure folder is selected as workspace |
| Memory seems off | Run "memory review" to recalibrate |
| Too many interruptions | Dual-mode: execution (quiet) + review (batch) |
| Files messy | Use weekend archive to organize |

## Next Steps

- Read [methodology.md](methodology.md) for the full philosophy
- Explore zone agent files for area-specific rules
- Start accumulating skills in `06 Skills/`
- After 2-3 weeks, your AI will noticeably "know" you better

---
*Memory Work · Quick Start · v2.0*
