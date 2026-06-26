# Org Commit Monitor

## Setup
1. Place `monitor.py`, and `SKILL.md` in the skill folder.
2. get the list of member needed for this skill from the `monitor.py`
3. Set Environment Variables:
   - `GITHUB_TOKEN`: Your Personal Access Token.
   - `GITHUB_ORG`: Your Organization name.

## Automation
- **Cron**: `30 4 * * *` (Runs daily at 10:00 AM IST; adjust for UTC timezone offset)
- **Action**: Run `python3 monitor.py` and post output to #dev-updates.

## Commands
- `/team-status`: Runs the script immediately to show current standings.