# Open DeepSeek Skill

## What it does
Opens Brave browser and goes to DeepSeek website automatically

## How to install
1. Put this folder in your OpenClaw skills directory
2. Run: `openclaw skills install ./open-deepseek`
3. Say: "open deepseek"

## Requirements
- Brave browser must be installed
- Python 3 (for .py script) or Bash (for .sh script)

## Files
- `SKILL.md` - Rulebook for AI
- `scripts/open_deepseek.py` - Python script
- `scripts/open_deepseek.sh` - Bash script (alternative)

## Troubleshooting
- If Brave not found, install it from https://brave.com
- If script doesn't run, make sure it's executable: `chmod +x scripts/*.sh`