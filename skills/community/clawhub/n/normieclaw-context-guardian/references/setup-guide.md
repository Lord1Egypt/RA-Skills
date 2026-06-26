# Context Guardian — Setup Guide

This skill works out of the box, but you'll get the most out of it with a simple workspace setup.

## What You Need

A `memory/` folder in your workspace where your AI saves daily notes. That's it.

## Quick Setup (30 seconds)

Open your terminal (or ask your AI to do it) and run:

```bash
mkdir -p memory/archive
```

This creates:
- `memory/` — where daily notes go (e.g., `memory/2026-03-16.md`)
- `memory/archive/` — where old completed items get moved during cleanup

## How It Works

Your AI will automatically:
- **Save notes** to `memory/YYYY-MM-DD.md` as you work together
- **Read yesterday's and today's notes** at the start of each session so it knows what you've been up to
- **Move old stuff** to `memory/archive/` during weekly cleanups

You don't need to manage these files yourself. Your AI handles it. But you can always open them and read/edit if you want — they're just plain text files.

## Optional: Long-Term Memory File

If you want your AI to remember important things across weeks and months, create a file called `MEMORY.md` in your workspace root:

```bash
touch MEMORY.md
```

Your AI will use this for:
- Long-term preferences ("I prefer morning meetings")
- Active project status
- Important decisions that stay relevant over time

During weekly cleanups, your AI will suggest promoting important items from daily notes into this file, and removing things that are no longer relevant.

## Optional: AGENTS.md

If you have an `AGENTS.md` file in your workspace, you can add a line telling your AI to follow Context Guardian practices:

```markdown
## Session Hygiene
Follow the context-guardian skill for session management, note-taking, and memory maintenance.
```

This makes sure every session starts with good habits.

## What "Starting Fresh" Means

When your AI suggests "starting a fresh session," it means:
1. Your AI saves everything you've discussed to a notes file
2. You start a new conversation (new chat/session)
3. Your AI reads the saved notes and picks up right where you left off

Nothing gets lost. Your AI just works better when it's not carrying a huge conversation history.

Think of it like clearing your desk — same work, same project, just a clean surface to work on.

## Troubleshooting

**"My AI isn't saving notes"**
Make sure the `memory/` directory exists in your workspace. Run `mkdir -p memory/archive` to create it.

**"My AI is too naggy about starting fresh"**
The skill is designed to suggest, not demand. If it feels too frequent, just tell your AI: "I'm fine, let's keep going." It will back off.

**"I lost something from a previous session"**
Check `memory/` for daily notes files. They're named by date (e.g., `memory/2026-03-16.md`). Everything your AI saved will be there.

**"The weekly cleanup deleted something I needed"**
Check `memory/archive/`. Archived items are moved there, not deleted. They're organized by month (e.g., `memory/archive/2026-03.md`).

## That's It

No configuration files. No API keys. No complicated setup. Just a folder and good habits.

Your AI handles the rest.
