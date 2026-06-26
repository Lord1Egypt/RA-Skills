# Setup Guide

## Quick Start

### Step 1: Create the data directory

```bash
mkdir -p data/{medications,members,prescriptions,logs,media}
```

Or let the AI agent create it when you first add a medication.

### Step 2: Set up family member profiles

**Do this before anything else.** The AI agent will guide you through it:

1. Agent asks: "家里有几位成员？分别是谁？"
2. For each member, provide:
   - 姓名、角色（大人/小孩/老人）、出生日期
   - 体重（儿童必填，用药剂量按体重计算）
   - **过敏史**（最重要的安全问题）
3. The agent creates `data/members/{name}.md` for each person
4. Confirm the profiles are correct

You can always add more details later (chronic conditions, vaccination history, etc.).

### Step 3: Start adding medications

- **Best**: Send a photo of a prescription or medicine box
- **Good**: Describe the medication in text
- **Also works**: Voice description (if your platform supports speech-to-text)

### Step 4: Set up reminders (optional)

Tell the agent: "提醒我每天8点吃XX药" and it will configure your platform's reminder system.

### Step 5: Check expiry regularly

```bash
python3 scripts/check_expiry.py /path/to/data/medications/
```

Or just ask: "检查一下家里有没有过期药品"

## No Database Needed

This skill uses **markdown files** for storage. No PostgreSQL, no configuration, no dependencies.

## Platform Integration

### Reminder System

Use your platform's built-in cron/reminder system:

```bash
# OpenClaw cron example
openclaw cron add \
  --name "med-{drug}-{time}" \
  --schedule "0 8 * * *" \
  --message "💊 Take {drug}: {dose}"
```

## Tips

- **Photos work best** for prescriptions — the AI can extract more details
- **Confirm before saving** — the agent should always show you the extracted info first
- **Batch tracking** — add each batch separately if you have multiple purchases
- **Keep dates consistent** — always use YYYY-MM-DD format
- **Backup** — the entire `data/` directory is your database — back it up regularly
