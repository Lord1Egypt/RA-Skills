---
name: open-deepseek
description: "Opens Brave browser and navigates to DeepSeek website. Use when user says 'open deepseek' or 'go to deepseek'."
---

# Open DeepSeek Skill

This skill opens the Brave browser and goes to DeepSeek's website.

## Trigger
- "open deepseek"
- "go to deepseek"
- "launch deepseek"
- "/deepseek"

## Instructions
1. When user asks to open DeepSeek, run the script `scripts/open_deepseek.py`
2. The script will:
   - Open Brave browser
   - Navigate to https://chat.deepseek.com
   - Keep browser window ready for typing
3. Tell user: "DeepSeek is open in Brave! Type your prompt there."

## Safety
- Only runs when user explicitly asks
- Does not modify browser settings
- Only opens one tab