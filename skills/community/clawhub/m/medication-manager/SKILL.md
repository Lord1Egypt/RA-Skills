---
name: medication-manager
description: >
  Family medication management skill using file-based storage (no database required).
  Supports medication entry via photo/image (prescription, medicine box), text description,
  or voice input. Manages medication inventory, batch tracking, expiry alerts, and
  member health records. Works with any reminder platform (Feishu, Telegram, QQ, etc.).
  Use when: (1) user sends photos of prescriptions or medicine boxes, (2) user describes
  medications to record, (3) checking medication inventory or expiry, (4) reviewing
  medication history, (5) logging medication intake, (6) managing family health records.
---

# Medication Manager

Family medication management with **file-based storage**. No database required — works anywhere.

## Overview

| Feature | How |
|---------|-----|
| Medication catalog | Markdown files in `data/medications/` |
| Member profiles | Markdown files in `data/members/` |
| Batch tracking | Embedded in medication files |
| Expiry alerts | `scripts/check_expiry.py` or manual scan |
| Reminders | Your platform's cron/reminder system (configurable) |
| Notifications | OpenClaw cron, webhooks, email, local OS — you choose |
| Media archive | `data/media/` with date-based folders |

## Quick Start

### Step 1: Set Up Family Member Profiles

**This is always the first step.** Before recording any medications, create profiles for each family member.

See [references/member-profile.md](references/member-profile.md) for the complete template, role-specific fields, and data collection guide.

**Setup flow** (follow this every time):

1. **Ask about family members**: "家里有几位成员？分别是谁？（大人/小孩/老人）"
2. **For each member, collect minimum info**:
   - **姓名** — who is this person?
   - **角色** — 成人 / 儿童 / 老人
   - **出生日期** — for age calculation (儿童: calculate exact months)
   - **体重 (kg)** — ⚠️ 儿童必填，用药剂量按体重计算
   - **过敏史** — ⚠️ 最重要的安全问题 — "有没有什么药物过敏？"
3. **For children, additionally ask**:
   - 疫苗接种情况
   - 近期是否生病/用药
4. **For adults/elderly, additionally ask**:
   - 慢性病（高血压、糖尿病等）
   - 长期服用的药物
5. **Create `data/members/{name}.md`** for each member
6. **Confirm** the profiles with the user before proceeding

**Minimal profile** (user can fill in details later):
```markdown
# {姓名}

| Field | Value |
|-------|-------|
| Name | {姓名} |
| Role | 成人 / 儿童 / 老人 |
| Birth Date | YYYY-MM-DD |
| Weight | {kg} |
| Allergies | {list or "无已知过敏"} |
```

### Step 2: Configure Notifications

**Before setting reminders, configure how the user wants to be notified.**

This skill does **not** hardcode any notification channel. The user chooses their own method.

#### Option A: OpenClaw Built-in Cron (Recommended for OpenClaw users)

If running on OpenClaw, the cron system supports all configured channels automatically.

```bash
# Example: daily 8am reminder via current channel
openclaw cron add \
  --name "med-{member}-{drug}" \
  --schedule "0 8 * * *" \
  --agent-id your-agent \
  --message "⏰ 用药提醒\n\n💊 {药品名}\n剂量：{剂量}\n\n请按时服药！"
```

**Supported channels** (via `--target`):

| Channel | Target Format | Example |
|---------|--------------|---------|
| Feishu | `feishu:{open_id}` | `feishu:ou_xxxxx` |
| Telegram | `telegram:{chat_id}` | `telegram:-1001234567` |
| QQ Bot | `qqbot:c2c:{openid}` | `qqbot:c2c:xxxxx` |
| Discord | `discord:{channel_id}` | `discord:123456789` |
| Signal | `signal:{phone}` | `signal:+86138xxxx` |

> **Tip**: Omit `--target` to send to the current conversation (auto-detected).

#### Option B: Webhook (DingTalk, WeChat Work, Slack, etc.)

If the user has a webhook URL, send a POST request with the reminder message. See [references/notifications.md](references/notifications.md) for full templates.

**See [references/notifications.md](references/notifications.md) for:**
- All notification options with full examples
- Notification content templates
- Agent implementation guide
- Troubleshooting

**What the agent should do:**
1. Detect the user's current channel from conversation context
2. Ask: "你希望通过什么方式接收用药提醒？" and offer options
3. If OpenClaw → use cron with auto-detected target
4. If webhook → ask for the webhook URL
5. Store the notification config in the member profile
6. **Always test** — send one test notification to confirm it works

### Step 3: Set Up Data Directory

Create the storage structure:

```
data/
├── medications/        # One .md per medication
├── members/            # One .md per family member (created in Step 1)
├── prescriptions/      # Prescription records (optional)
├── logs/               # Medication intake logs (YYYY-MM-DD.md)
├── config/             # Optional: notification config
│   └── notifications.yaml
└── media/              # Photos of prescriptions/boxes
    └── YYYY-MM-DD/
```

### Step 4: Add Medications

When a user describes or sends a photo of a medication:

1. Analyze with vision model (if photo)
2. Extract: generic name, brand name, spec, manufacturer, batch no, expiry, dosage
3. Confirm details with user
4. Create a markdown file: `data/medications/{generic_name}.md`
5. Set up reminders if requested (using configured notification method)

## Medication File Template

```markdown
# {Generic Name} ({Brand Name})

## Basic Info
| Field | Value |
|-------|-------|
| Generic Name | {name} |
| Brand Name | {name} |
| Specification | {spec} |
| Manufacturer | {manufacturer} |
| Approval No | {批准文号} |
| Drug Type | 处方药 / OTC / 外用药 |
| Category | 抗生素 / 感冒药 / 退烧药 / etc. |
| Indications | {适应症} |
| Contraindications | {禁忌} |
| Storage | {储存条件} |

## Batches
| Batch No | Mfg Date | Expiry | Qty | Unit | Location | Status |
|----------|----------|--------|-----|------|----------|--------|
| {batch} | {date} | {date} | {n} | 盒/支/瓶 | {location} | active |

## Usage Notes
- Adult dose: {dosage}
- Child dose: {dosage by weight}
- Food: before/after meals
- Special notes: {warnings}

## History
| Date | Member | Action | Notes |
|------|--------|--------|-------|
| YYYY-MM-DD | {name} | added/prescribed | {source} |
```

## Notification Settings

## Core Workflows

### Photo Entry (prescription / medicine box)

```
User sends image → Analyze with vision model → Extract medication info
→ Confirm with user → Create/update medication .md file → Set reminders if requested
```

**Steps:**
1. Use your platform's image analysis tool to read the photo
2. Extract: generic name, brand name, spec, manufacturer, batch no, expiry, dosage
3. Confirm details with user (especially for prescriptions)
4. Save photo to `data/media/YYYY-MM-DD/`
5. Create or update the medication markdown file
6. Ask if reminders are needed → use configured notification method

### Text Entry

```
User describes medication → Parse → Confirm → Create .md file
```

Use structured extraction from user's text description. Always confirm before creating.

### Set Reminder

```
Get member + medication + schedule → Check notification config
→ Create platform-specific reminder → Record in member file → Test it
```

1. Read member file for notification settings
2. If no notification config exists → **ask the user to configure first** (see Step 2)
3. Query medication file for drug info
4. Determine reminder schedule based on dosage instructions
5. Create reminder using the configured method:
   - **OpenClaw cron**: `openclaw cron add --name "..." --schedule "..." --message "..."`
   - **Webhook**: POST JSON to the webhook URL
6. **Test** — send one notification immediately to confirm delivery
7. Record the reminder details in the member's notification settings
8. Confirm with the user: "提醒已设置，{时间}会收到通知"

### Expiry Check

```bash
python3 /path/to/medication-manager/scripts/check_expiry.py /path/to/data/medications/
```

Or manually scan medication files for expiry dates. Alert levels:

| Level | Threshold | Action |
|-------|-----------|--------|
| 🔴 Expired | Past date | Notify immediately, mark as expired |
| ⚠️ 7 days | Within 7 days | Daily reminder to use or dispose |
| 🟡 30 days | Within 30 days | Weekly reminder |
| 🔶 90 days | Within 90 days | Monthly review |

### Query Inventory

Scan all files in `data/medications/` for:
- Active batches with quantity > 0
- Sort by expiry date (soonest first)
- Filter by category if requested

### Log Medication Intake

When a family member takes a medication:

1. Append entry to `data/logs/YYYY-MM-DD.md`:
   ```markdown
   | Time | Member | Medication | Dose | Status | Notes |
   |------|--------|-----------|------|--------|-------|
   | 08:15 | 张三 | 氨氯地平 | 5mg | ✅ taken | 饭后 |
   ```
2. Update batch quantity in the medication file (decrement)
3. Flag if dose was missed or skipped

## Reference Data

| Reference | Path | Purpose |
|-----------|------|---------|
| Member profiles | [references/member-profile.md](references/member-profile.md) | Template & collection guide |
| Notifications | [references/notifications.md](references/notifications.md) | All notification options & templates |
| Storage layout | [references/storage-layout.md](references/storage-layout.md) | File organization & naming |
| Drug interactions | [references/drug-interactions.md](references/drug-interactions.md) | Check when multiple drugs prescribed |
| Pediatric dosage | [references/pediatric-dosage.md](references/pediatric-dosage.md) | Calculate child doses by weight |
| Setup guide | [references/setup.md](references/setup.md) | Installation & first use |

## Important Rules

- **Always confirm** medication details before saving
- **Configure notifications first** — reminders are useless if they can't reach the user
- **Test notifications** — always send a test notification after setup
- **Children dosing**: always verify weight and age, ask about allergies
- **Expiry alerts**: proactively notify when drugs expire or near expiry
- **Antibiotics**: flag prescription antibiotics, remind about completing full course
- **Drug interactions**: check reference when multiple drugs prescribed together
- **Special drugs**: flag controlled substances (精二药品, etc.)
- **Privacy**: do not share personal health information

## Platform Adapters

This skill is **platform-agnostic**. The notification layer adapts to whatever the user has:

| Platform | Method | Setup |
|----------|--------|-------|
| OpenClaw (any channel) | Built-in cron | Auto-detected, no config needed |
| Feishu | `message` tool or cron | Set `--target "feishu:{open_id}"` |
| Telegram | Bot API or cron | Set `--target "telegram:{chat_id}"` |
| QQ Bot | qqbot_remind / qqbot_cron | Set target via cron |
| Webhook | POST JSON | Provide webhook URL |

Full details: [references/notifications.md](references/notifications.md)

## Data Migration

If you have existing medication data (e.g., from a spreadsheet or another system):
1. Convert each medication to the markdown template above
2. Place files in `data/medications/`
3. Run the expiry check script to validate dates
