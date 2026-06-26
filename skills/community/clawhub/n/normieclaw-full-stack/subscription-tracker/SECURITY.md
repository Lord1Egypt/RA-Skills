# Security — Subscription Tracker

## How Your Data Is Handled

Subscription Tracker processes bank and credit card statements to identify recurring charges. This document explains what happens with that data.

### What the Tool Accesses

- **Statement files you provide** — CSV or PDF files you upload to your agent. These contain transaction history including dates, merchant names, and amounts.
- **A local JSON database** — Your subscription data is stored in `~/.normieclaw/subscription-tracker/subscriptions.json` on the machine running your OpenClaw agent.
- **Statement archives** — Uploaded statements may be stored in `~/.normieclaw/subscription-tracker/statements/` for future comparison scans.

### What the Tool Does NOT Do

- **No bank account linking** — We never connect to your bank. No Plaid, no Finicity, no screen scraping. You provide statement files manually.
- **No credential storage** — We never ask for or store your bank login, password, or MFA codes.
- **No bill negotiation** — We don't contact service providers on your behalf.
- **No automated cancellation** — We provide instructions; you perform the cancellation.
- **No credit monitoring** — We don't access credit reports or scores.

### Data Sensitivity

Bank and credit card statements contain sensitive financial information:
- Transaction amounts and dates
- Merchant names (which reveal spending habits)
- Partial account numbers (last 4 digits)
- Potentially identifying purchase patterns

**Treat your subscription database and stored statements with the same care you'd give the original bank statements.** These files contain real financial data.

### Where Data Lives

All data is stored on the machine running your OpenClaw agent:

```
~/.normieclaw/subscription-tracker/
├── subscriptions.json    # Your subscription database
├── statements/           # Uploaded statement files
├── exports/              # Generated reports
└── logs/                 # Scan logs
```

### Your Responsibilities

- **Secure your machine** — The subscription data is only as secure as the device it's on.
- **Control statement access** — Only upload statements through your agent. Don't share statement files through unsecured channels.
- **Review exports** — If you export data (CSV, Budget Buddy format), those files also contain financial information. Handle accordingly.
- **Clean up when done** — If you stop using the tool, delete the `~/.normieclaw/subscription-tracker/` directory to remove all stored data.

### Deletion

To remove all Subscription Tracker data:

```bash
rm -rf ~/.normieclaw/subscription-tracker/
```

This removes your subscription database, all stored statements, exports, and logs.

### AI Agent Processing

Your OpenClaw agent reads and processes your statement data to identify subscriptions. This means:
- Statement contents are sent to the AI model as part of the conversation context
- The AI model processes transaction data to identify patterns and recurring charges
- Model providers have their own data handling policies — consult your model provider's terms

### Third-Party Services

Subscription Tracker itself does not send your data to any third-party service. However:
- Your AI model provider processes the data as part of agent interactions
- If you use the Budget Buddy Pro export feature, that data is shared with the Budget Buddy Pro tool on your same agent
- No data is sent to NormieClaw, analytics services, or any external API

### Updates

This document covers Subscription Tracker v1.0.0. Security practices may be updated in future versions. Check for the latest version at [normieclaw.ai](https://normieclaw.ai).
