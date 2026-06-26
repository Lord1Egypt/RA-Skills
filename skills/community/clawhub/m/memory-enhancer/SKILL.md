# Memory Enhancer Skill

## Purpose
Extract structured facts from daily logs and maintain long-term memory using a sub-agent.

## How it works
1. Finds yesterday's daily memory file: `memory/YYYY-MM-DD.md`
2. Spawns a sub-agent with the day's log content
3. Sub-agent uses OpenRouter to analyze and extract:
   - Preferences (communication style, topics of interest)
   - New contacts (names, roles, context)
   - Habits/routines
   - Projects (active, completed, progress)
4. Sub-agent updates JSON files in `memory/stats/`
5. Sub-agent appends a concise summary to `MEMORY.md`
6. Main skill logs the outcome

## Configuration
- Runs daily via cron (default: 02:00 AM)
- Model: Uses OpenRouter (default: `openrouter/openrouter/free`)
- Temperature: 0.3 (for consistent extraction)

## Files modified
- `memory/stats/preferences.json`
- `memory/stats/contacts.json`
- `memory/stats/habits.json`
- `memory/stats/projects.json`
- `MEMORY.md` (curated summary)

## Invocation
This skill is intended to run automatically via cron job.
Manual test: `skill/memory-enhancer` (will process most recent memory file if yesterday's missing)