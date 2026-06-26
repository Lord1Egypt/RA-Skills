# 💊 Medication Manager

> **Family medication management — zero database, pure markdown, works anywhere.**

Take a photo of a prescription or medicine box, and your AI agent will automatically record it, track expiry dates, set up reminders, and alert you about drug interactions. No database setup, no API keys, no configuration — just install and go.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📸 **Photo Entry** | Snap a photo of a prescription or medicine box — AI extracts all details |
| 📝 **Text Entry** | Describe medication in natural language |
| 👨‍👩‍👧‍👦 **Member Profiles** | Track medications per family member (adult/child/elder) |
| ⏰ **Reminders** | Configurable medication reminders via your preferred channel |
| 📅 **Expiry Alerts** | Automatic scanning and alerting for expiring medications |
| ⚠️ **Drug Interactions** | Built-in reference for common drug interaction checking |
| 👶 **Pediatric Dosing** | Weight-based dosage calculation reference |
| 💊 **Batch Tracking** | Track multiple batches per medication with quantity and location |
| 📊 **Intake Logs** | Daily medication intake tracking |
| 🔒 **Privacy First** | No cloud database, no API keys — everything stays in your files |

## 🚀 Quick Start

### Install

```bash
clawhub install medication-manager
```

### Setup (takes 2 minutes)

**1. Create data directories** (or let the AI agent do it automatically):

```bash
mkdir -p data/{medications,members,prescriptions,logs,media}
```

**2. Add family members:**

Just tell your AI agent: "Add a family member: 张三, adult, no allergies."

The agent will create `data/members/张三.md` with their profile.

**3. Configure notifications (optional but recommended):**

Tell your agent how you want to receive reminders:
- **OpenClaw users**: Automatic — uses your current channel
- **Webhook**: Provide your DingTalk/WeChat Work/Slack webhook URL
- **Email**: Provide your email address
- **Local**: Desktop notifications (macOS/Linux)

**4. Start adding medications:**

- **Best**: Send a photo of a prescription or medicine box
- **Good**: Type "I have 阿莫西林, 500mg, 2 boxes, expires 2027-06"
- The agent will extract details, confirm with you, and create the record

## 📖 How It Works

### Architecture

```
┌─────────────────────────────────────────────┐
│           Your AI Agent                     │
│  (OpenClaw / any LLM with vision)           │
│                                             │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐ │
│  │ Photo    │  │ Text      │  │ Voice    │ │
│  │ Entry    │  │ Entry     │  │ Entry    │ │
│  └────┬─────┘  └─────┬─────┘  └────┬─────┘ │
│       └──────┬───────┬──────┘       │       │
│              ▼       ▼              ▼       │
│     ┌────────────────────────────────┐     │
│     │  Medication Manager Skill      │     │
│     │                                │     │
│     │  • Extract & confirm details   │     │
│     │  • Create markdown records     │     │
│     │  • Check drug interactions     │     │
│     │  • Set up reminders            │     │
│     │  • Scan for expiry alerts      │     │
│     └────────────────┬───────────────┘     │
│                      │                     │
└──────────────────────┼─────────────────────┘
                       ▼
        ┌──────────────────────────┐
        │    File-based Storage    │
        │                          │
        │  data/                   │
        │  ├── medications/*.md    │
        │  ├── members/*.md        │
        │  ├── logs/*.md           │
        │  └── media/              │
        └──────────────────────────┘
```

### Data Format

Each medication is one markdown file:

```markdown
# 阿莫西林 (Amoxicillin)

## Basic Info
| Field | Value |
|-------|-------|
| Generic Name | 阿莫西林 |
| Brand Name | 阿莫仙 |
| Specification | 500mg × 24 |
| Manufacturer | 珠海联邦制药 |
| Drug Type | 处方药 |
| Category | 抗生素 |

## Batches
| Batch No | Expiry | Qty | Unit | Status |
|----------|--------|-----|------|--------|
| 240501 | 2027-06-01 | 2 | 盒 | active |
```

Simple, readable, editable by hand, easy for AI to parse.

## 📋 Usage Scenarios

### Scenario 1: Record a Prescription

```
You: [sends photo of prescription]
Agent: "I see a prescription from Dr. 王 for 阿莫西林 500mg.
        3 times daily for 7 days. Confirm these details?
        
        Shall I set up reminders for 8:00, 14:00, and 20:00?"
You: "Yes, all correct. Set reminders."
Agent: ✅ Recorded. Reminders set via your configured channel.
```

### Scenario 2: Check Expiring Medications

```
You: "Check which medications are expiring soon."
Agent: "🔍 Scanned 15 medications:
        
        ⚠️ 3 items need attention:
        - 布洛芬 [003] — expires in 7 days (1 box)
        - 氨溴索 [001] — expires in 30 days (1 box)
        - 健胃消食片 [001] — expires in 45 days (1 box)"
```

### Scenario 3: Drug Interaction Check

```
You: "Doctor prescribed 克拉霉素 and I'm taking 阿托伐他汀."
Agent: "⚠️ Drug Interaction Alert!
        
        克拉霉素 + 阿托伐他汀 → Rhabdomyolysis risk
        Recommendation: Pause statin during antibiotic course
        or switch to a non-interacting antibiotic.
        Please consult your doctor."
```

### Scenario 4: Pediatric Dosage

```
You: "My child is 3 years old, 15kg, has a fever."
Agent: "Based on weight (15kg):
        
        🌡️ Fever medication:
        - 布洛芬: 75-150mg per dose (every 6-8h)
        - 对乙酰氨基酚: 150-225mg per dose (every 4-6h)
        
        Please confirm which medication you have available."
```

## 🔧 Configuration

### Notifications

The skill adapts to your platform automatically:

| Platform | Setup |
|----------|-------|
| **OpenClaw** | Auto-detected, no config needed |
| **DingTalk** | Provide webhook URL |
| **WeChat Work** | Provide webhook URL |
| **Slack** | Provide webhook URL |

### Expiry Checking

```bash
# Manual check
python3 scripts/check_expiry.py data/medications/

# Or just ask your AI agent
# "Check for expired medications"
```

### Reminder Management

```bash
# List all reminders
openclaw cron list

# Remove a reminder
openclaw cron remove med-{member}-{drug}

# Pause/resume
openclaw cron disable med-{member}-{drug}
openclaw cron enable med-{member}-{drug}
```

## 📁 Directory Structure

```
data/
├── medications/        # One .md per medication
│   ├── 阿莫西林.md
│   ├── 布洛芬.md
│   └── ...
├── members/            # One .md per family member
│   ├── 张三.md
│   └── ...
├── prescriptions/      # Prescription records
├── logs/               # Daily intake logs (YYYY-MM-DD.md)
└── media/              # Photos (organized by date)
    └── 2026-04-13/
        └── prescription_001.jpg
```

## 🛡️ Privacy & Security

- **No database** — all data stored as local markdown files
- **No API keys** — no authentication tokens hardcoded
- **No cloud dependency** — works entirely on your machine
- **Your data stays yours** — no telemetry, no sync, no sharing
- **Backup friendly** — just copy the `data/` directory

## 📚 Reference Data Included

| Reference | Content |
|-----------|---------|
| **Drug Interactions** | Common drug interactions with severity levels and actions |
| **Pediatric Dosage** | Weight-based dosing for 20+ common medications |
| **Member Profiles** | Template for family member health records |
| **Storage Layout** | File organization and naming conventions |

## 🔮 Coming Soon

- [ ] Medication shopping list generation
- [ ] Monthly usage reports
- [ ] Insurance reimbursement tracking
- [ ] Import from spreadsheets
- [ ] Multi-language support

## 📝 License

Free to use, modify, and share.

## 💡 Tips

1. **Photos work best** — the AI extracts much more from a clear photo than from text
2. **Confirm before saving** — the agent should always show you what it extracted
3. **Track batches separately** — each purchase gets its own entry with unique expiry
4. **Update regularly** — mark medications as used/depleted to keep inventory accurate
5. **Back up your data** — the `data/` folder is your entire database
6. **Start small** — just add current medications, don't try to enter everything at once

## ❓ FAQ

**Q: Do I need a database?**
A: No! Everything is stored as simple markdown files. No setup, no config.

**Q: Can I use this without OpenClaw?**
A: Yes, the skill is platform-agnostic. Any AI agent that can read/write files can use it. The notification section provides adapters for different platforms.

**Q: How do I back up my data?**
A: Just copy the `data/` directory anywhere — it's all plain text.

**Q: Can multiple family members use it?**
A: Yes! Create a profile for each member and the agent tracks medications per person.

**Q: Is the drug interaction list comprehensive?**
A: It covers common interactions found in typical family medication cabinets. For rare drugs or complex interactions, always consult a pharmacist or doctor.

**Q: Can I import existing medication data?**
A: Yes, convert your data to the markdown template format and place files in `data/medications/`. See `references/setup.md` for details.
