# Project Manager Pro — Setup Prompt

> Run this conversation on first install to configure the tool for the user.

---

## Step 1: Welcome & Active Projects

```
🎯 Project Manager Pro — Let's get you set up (2 min).

First — any active projects or big goals? Examples:
  • "Launch a website by April"
  • "Move apartments in June"
  • "Study for certification exam"

Tell me what's on your plate and I'll create them. Add more anytime.
```

**Action:** Create project entries for each one the user mentions. Ask for target dates if not provided.

## Step 3: Priority Framework

```
How do you want me to prioritize your tasks?

1️⃣ Eisenhower Matrix (recommended) — Urgent/Important grid. I auto-classify based on deadlines and context.
2️⃣ ICE Scoring — Rate Impact, Confidence, Ease (1-10 each). Best for business-heavy task lists.
3️⃣ Value/Effort — High/Low value vs effort quadrants. Good for decision-heavy workflows.
4️⃣ Simple P1-P4 — You assign priority manually. No auto-classification.

Pick a number, or just say "default" for Eisenhower.
```

**Action:** Set `priority_framework` in settings.json.

## Step 4: Check-In Schedule

```
I can check in with you to keep things on track:

☀️ Morning brief — Your priorities for the day
🌙 Evening review — What got done, what's carrying over  
📊 Weekly summary — Progress report + next week preview

What times work? Defaults:
  • Morning: 8:00 AM
  • Evening: 7:00 PM
  • Weekly: Sunday 10:00 AM

You can change these anytime. Want all three, or just some?
```

**Action:** Set `check_ins` schedule in settings.json. Respect the user's timezone from their agent config.

## Step 5: Quiet Hours

```
When should I NOT bug you?

Default quiet hours: 10:00 PM – 7:00 AM
No check-ins, no task alerts during this window.

Works for you, or want to adjust?
```

**Action:** Set `quiet_hours` in settings.json.

## Step 6: Cross-Tool Integration

```
If you're using other NormieClaw tools, I can auto-create tasks from them:

  💰 Expense Tracker → bill reminders, subscription renewals
  🍽 Meal Planner → grocery shopping, meal prep tasks
  💪 Fitness Tracker → workout tasks, supplement reorders
  📝 Content Calendar → content creation deadlines

Want me to pick up tasks from your other tools automatically?
(You can always turn specific integrations on/off later.)
```

**Action:** Set `cross_tool_integrations` in settings.json with enabled/disabled per tool.

## Step 7: Confirmation

Summarize all configured settings, then: "Start by telling me something you need to do, or say 'show my tasks' anytime."

**Action:** Write settings.json, create pm-pro data directory via setup.sh.

## Agent Notes

- Run setup.sh before the conversation begins
- If the user skips questions, use defaults — don't stall
- If the user mentions tasks during setup, create them immediately
- One-time conversation. After completion, operate via SKILL.md
