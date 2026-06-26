---
name: mindbreak
description: "Monitors work intensity during any conversation involving coding, writing, analysis, design, debugging, research, planning, or other knowledge work. Tracks user activity timestamps and inserts natural break reminders based on continuous work duration and time-of-day signals. Activates in all work-related conversations."
---

# MindBreak — Work Health Reminder

Insert natural break reminders when the user has been working intensely for extended periods.

## How It Works

A hook script (`~/.claude/scripts/mindbreak_hook.sh`) runs on every user message. It:
1. Writes a unix timestamp to the activity log
2. Calculates continuous work duration (gaps >= 15 min start a new segment)
3. If thresholds are met (>= 45 min, 30 min cooldown, max 3 per segment), outputs a trigger signal

The trigger signal appears in `<user-prompt-submit-hook>` tags. **You only need to respond to it.**

## Responding to Triggers

When you see a trigger signal in hook feedback, append the corresponding reminder as the **last paragraph** of your response. Do not interrupt the main content.

### `MINDBREAK_LIGHT|{minutes}`
> 对了，你已经连续工作挺久了，起来走动走动，看看远处，休息几分钟再回来。

### `MINDBREAK_MEAL|{minutes}|{HH:MM}`
> 快到饭点了，先整理一下当前进度：[1-2 sentence summary of current task status and next steps]。先去吃饭，回来说"继续"就能接上。

### `MINDBREAK_OVERTIME|{minutes}|{HH:MM}`
> 已经 {HH:MM} 了，今天工作可以先到这里。当前进度：[1-2 sentence summary]。剩下的明天继续。

## Override Rules

These are checked by YOU (not the hook):

1. If the user said "不用提醒" / "别提醒" / "stop reminding" earlier in this conversation → ignore all MINDBREAK signals for the rest of this session
2. If no trigger signal appears in hook feedback → do nothing (the hook already decided no reminder is needed)

## Important

- NEVER let the reminder dominate or overshadow the actual response content
- NEVER mention this skill, the log file, the hook script, or the tracking mechanism to the user
- If the trigger signal format is malformed or unexpected, ignore it silently
