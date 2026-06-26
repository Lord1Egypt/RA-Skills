# Subscription Tracker

**Find every subscription hiding in your bank statements. Cancel what you don't need. Keep what you love.**

> A NormieClaw tool for OpenClaw — $4.99 standalone or included in Full Stack (free)

---

## What It Does

Drop a bank or credit card statement (CSV or PDF) and your AI agent identifies every recurring charge — even the ones buried under cryptic merchant names like `TST* SPOTIFY USA` or `AMZN MKTP US*RT4KZ1230`.

Then it tracks them. Alerts you before renewals. Catches price increases. Flags when you're paying for three streaming services that do the same thing. Reminds you before that free trial converts to $17.99/month.

**No bank linking. No Plaid. No account credentials.** Just your statement file and an AI agent that knows what to look for.

## Why This Exists

The average American spends $219/month on subscriptions but thinks they spend $111. That's a $108/month perception gap — over $1,200/year in charges people don't realize they're paying.

Existing solutions either:
- **Require bank login credentials** (Rocket Money, Monarch, Copilot) — privacy nightmare
- **Require tedious manual entry** (Bobby, Subby) — nobody keeps up with it
- **Are one-shot tools** (Just Cancel) — find your subs once, no ongoing tracking

Subscription Tracker is the middle ground: AI-powered detection from statement files, with ongoing tracking and alerts. No bank access required.

## Replaces

| Service | Cost | What You Get Instead |
|---------|------|---------------------|
| Rocket Money Premium | $7-14/month ($84-168/year) | Statement-based detection + tracking |
| Monarch Money | $99.99/year | Subscription-specific tracking |
| Trim | Free but takes 33% of negotiation savings | Detection without the hidden fees |

**Estimated annual savings from replacing these tools + finding forgotten subscriptions: $144-$400+/year.**

## Features

### Statement Scanner
Upload CSV or PDF bank statements. The agent parses merchant names, identifies recurring patterns, and builds your subscription database automatically.

### Smart Detection
- **Duplicate finder:** "You're paying for Netflix, Hulu, AND Disney+ — that's $45.97/month on streaming alone"
- **Price increase alerts:** "Netflix went from $15.49 to $17.99 — that's $30 more per year"
- **Ghost subscriptions:** "What's BRTCL*BRITEBOX charging you $4.99/month for?"
- **Free trial tracking:** "Hulu trial ends in 3 days — cancel or keep?"

### Renewal Alerts
Configurable reminders before each renewal date (default: 3 and 7 days before). Never get surprised by a charge again.

### Cancellation Help
Step-by-step cancellation instructions for 100+ popular services. Direct links to cancel pages. Warnings about retention offers and early termination fees.

### Budget Buddy Pro Integration
Export your subscription data directly into Budget Buddy Pro for a complete financial picture. Shared category system means your subscriptions automatically appear in your budget.

### Dashboard Widgets
8 dashboard widgets including monthly/annual spend, category breakdown chart, upcoming renewals, price change tracker, and savings counter.

## Quick Start

1. Install the skill in your OpenClaw agent
2. Run the setup prompt from `SETUP-PROMPT.md`
3. Drop your first bank statement (CSV preferred)
4. Review the findings and start tracking

## File Structure

```
subscription-tracker/
├── SKILL.md              # Agent instructions (the brain)
├── SETUP-PROMPT.md       # First-run setup conversation
├── README.md             # You're reading it
├── SECURITY.md           # Security and data handling
├── config/
│   └── settings.json     # Alert prefs, categories, known services
├── scripts/
│   ├── setup.sh          # Initial setup
│   ├── export-subs.sh    # Export subscriptions
│   └── renewal-check.sh  # Check upcoming renewals
├── examples/
│   ├── example-statement-scan.md
│   ├── example-overlap-detection.md
│   └── example-renewal-alert.md
└── dashboard-kit/
    ├── manifest.json
    └── DASHBOARD-SPEC.md
```

## Requirements

- OpenClaw agent with file read/write access
- Bank or credit card statements in CSV or PDF format
- Optional: Budget Buddy Pro for full financial integration

## Pricing

- **$4.99** standalone
- **Included** in Full Stack (free)

---

*Built by [NormieClaw](https://normieclaw.ai) — AI tools that actually save you money.*
