# Language Tutor Pro — Setup Guide

Welcome! This guide walks you through setting up Language Tutor Pro step by step.
No technical experience needed — just follow along.

---

## What You Need

- OpenClaw installed and running on your machine
- A working internet connection (the agent needs it for conversations)
- 5 minutes to complete setup

---

## Step 1: Drop the Skill into Your Agent

Copy the entire `language-tutor-pro` folder into your agent's skills directory:

```
~/.openclaw/workspace/.agents/skills/language-tutor-pro/
```

If that folder doesn't exist yet, create it. The whole folder goes in — don't just copy individual files.

---

## Step 2: Run the Setup Script

Open your terminal and run:

```bash
bash ~/.openclaw/workspace/.agents/skills/language-tutor-pro/scripts/setup.sh
```

This creates the data folders where your learning progress will be stored.
You'll see a confirmation message when it's done.

---

## Step 3: Configure Your Settings

Open the file `config/settings.json` inside the skill folder. Edit these fields:

- **native_language**: Your first language (e.g., "English")
- **target_language**: The language you want to learn (Spanish, French, German, Italian, Portuguese, Japanese, Mandarin, Korean)
- **current_level**: Your best guess at your level:
  - `A1` — Complete beginner, know almost nothing
  - `A2` — Know some basics, simple phrases
  - `B1` — Can handle basic conversations
  - `B2` — Fairly comfortable, some gaps
  - `C1` — Advanced, mostly fluent
  - `C2` — Near-native
- **learning_goals**: What you want to achieve (e.g., "travel to Spain", "talk to my in-laws", "pass DELE exam")
- **session_duration_minutes**: How long you want each practice session (10, 15, 20, or 30)

Don't worry about getting the level exactly right — the tutor will calibrate during your first session.

---

## Step 4: Start Your First Session

Just talk to your agent! Say any of these:

- "Let's practice Spanish"
- "Teach me French"
- "I want to learn Japanese"
- "Language lesson"

The tutor will introduce itself and run a quick conversation to figure out your actual level. Then you're off — your first real session starts right there.

---

## Step 5 (Optional): Set Up the Dashboard

If you use the NormieClaw dashboard, the `dashboard-kit/` folder contains everything needed to see your progress visually — vocabulary growth, grammar mastery, session history, and more.

Follow the instructions in `dashboard-kit/DASHBOARD-SPEC.md` to connect it.

---

## What Happens Next

- **Every session is saved.** Your tutor remembers your mistakes, your vocabulary, and your progress.
- **Vocabulary reviews happen naturally.** Words you've learned come back in future conversations at spaced intervals.
- **Grammar gets reinforced.** If you keep making the same mistake, the tutor will create more practice around that rule.
- **Your level adapts.** As you improve, conversations get harder. If you're struggling, they get easier.

---

## Quick Commands

| Say This | What Happens |
|----------|-------------|
| "Practice [language]" | Free conversation session |
| "Vocab review" | Review words due for spaced repetition |
| "Teach me [topic]" | Guided grammar/vocab lesson |
| "Situation: ordering food" | Role-play scenario practice |
| "My progress" | See your stats |
| "Export progress" | Export data for dashboard |

---

## Troubleshooting

**"The tutor doesn't seem to remember my last session"**
Make sure the data directory exists at `data/` inside the skill folder. Run `scripts/setup.sh` again if needed.

**"The level feels too easy / too hard"**
Tell the tutor: "Change my level to B2" (or whatever feels right). It'll adjust immediately.

**"I want to learn a second language"**
Say: "Add language: German" — the tutor handles multiple languages with separate progress tracking for each.

**"I want to export my vocabulary"**
Run: `bash scripts/export-progress.sh` — this creates a summary file you can review or share.

---

That's it. No accounts to create, no subscriptions to manage. Just start talking.
