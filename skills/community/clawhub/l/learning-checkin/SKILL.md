---
name: learning-checkin
description: Daily learning habit builder with check-ins and smart reminders
metadata: { "copaw": { "emoji": "📚" } }
---

# Learning Check-in Skill

Help users build a daily learning habit through simple check-ins and intelligent reminders.

## Overview

This skill enables users to track their daily learning with:
- Simple daily check-in (just say "I'm done" or "check-in complete")
- Automatic streak tracking
- Optional smart reminders

## Data Storage

All data is stored locally in a `data` subfolder next to the skill:

```
<skill_directory>/data/
├── rule.md           - User's customizable rules
├── records.json      - Check-in history
├── version.txt       - Current skill version
├── cron_status.json  - Reminder configuration status
└── reminder_log.json - Reminder sending log
```

The data folder is automatically created on first use.

## Commands

### 1. Initialize (First Time)

```bash
python <skill_path>/learning_checkin.py init
```

**Returns:**
- `welcome_message` - Welcome text for the user
- `environment` - Only contains `user_language` (for message display)
- `reminder_strategy` - Suggested reminder times
- `cron_status` - Current reminder configuration status

**Agent action:** 
1. Run the init command
2. Show welcome message and explain the check-in process
3. Ask user if they want daily reminders
4. Ask user to start their first check-in

### 2. Check-in

```bash
python <skill_path>/learning_checkin.py checkin
```

**Returns:**
- `success` - Whether check-in was recorded
- `streak` - Current streak count
- `message` - Celebration message (in English, translate to user's language)

### 3. Status

```bash
python <skill_path>/learning_checkin.py status
```

**Returns:**
- `checked_in_today` - Whether user has checked in today
- `streak` - Current streak count
- `total_checkins` - Total days checked in
- `message` - Status message (in English)

### 4. Get User Language

```bash
python <skill_path>/learning_checkin.py env
```

**Returns:**
- `user_language` - Detected language (zh/en)

**Why needed:** Only to display messages in the user's preferred language.

### 5. Get Reminder Message

```bash
python <skill_path>/learning_checkin.py message <time>
```

Where `<time>` is one of: `09:00`, `17:00`, `20:00`

**Returns:**
- `message` - Reminder text (in English, translate to user's language)

### 6. Check Reminder Status

```bash
python <skill_path>/learning_checkin.py reminder <time>
```

**Returns:**
- `should_send` - Whether reminder should be sent
- `checked_in` - Whether user has already checked in today

### 7. Update Cron Status

```bash
python <skill_path>/learning_checkin.py update-cron <times>
```

**When to use:** After setting up reminders (optional).

### 8. Get Cron Status

```bash
python <skill_path>/learning_checkin.py cron-status
```

**Returns:**
- `configured` - Whether reminders are set up
- `times` - Configured reminder times

## Default Behavior

### Check-in Rule
- User checks in once per day
- Simply tell the Agent "I'm done" or "check-in complete"

### Reminder Strategy (Suggested)
If user wants reminders, Agent can use any scheduling method:
- **Evening (20:00)** is recommended as default
- Or user's preferred time

The skill will check if user already checked in before sending reminders.

### Streak System
- Consecutive days = streak
- Miss a day = streak resets

## Customization

Users can edit the `rule.md` file (in the data folder) to customize reminder messages.

## Version

See GitHub releases: https://github.com/daizongyu/learning-checkin/releases

## Agent Guidelines

### First Interaction (Welcome)
The Agent should:
1. Be warm and encouraging
2. Explain the simple check-in process
3. Ask if user wants daily reminders (optional feature)
4. Ask: "Ready to start your first check-in?"

### Check-in Interaction
- Translate messages to user's language
- Celebrate the check-in
- Show streak count

### Reminder Implementation (Optional)
If user wants reminders:
- Agent decides how to implement (cron, native scheduler, etc.)
- The skill provides `reminder` and `message` commands
- Check if user already checked in before sending

## Technical Notes

- **Data collection**: Only `user_language` is collected for message display
- All messages are in **English** - Agent translates to user's language
- All file paths use UTF-8 encoding
- Compatible with Windows, Linux, macOS
- Data stored in `data` subfolder next to the skill
- **No external network requests** from the skill
- **No automatic scheduling** - Agent decides implementation
- No external dependencies (Python standard library only)

## Version

Current version: 3.1.0

GitHub: https://github.com/daizongyu/learning-checkin