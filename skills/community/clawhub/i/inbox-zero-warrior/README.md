# Inbox Zero Warrior

## The Problem

Email is the #1 productivity drain in modern work life:

- **The average professional receives 120+ emails per day** and spends **28% of their workday** on email (McKinsey Global Institute)
- **281 billion emails** are sent daily worldwide
- **62% of emails** are not essential and don't require a response (SaneBox study)
- **The average worker checks email 74 times per day** and takes **23 minutes** to refocus after each interruption (University of California)
- **Newsletter overload:** The average inbox receives 8+ promotional emails daily

The result: constant context-switching, anxiety about unread messages, important emails buried under noise, and hours wasted on low-value email management.

## Who Needs This

- **Knowledge workers** — anyone who uses email as a primary communication tool
- **Freelancers and consultants** who manage their own inbox without an assistant
- **Small business owners** who receive customer inquiries, invoices, and marketing
- **Anyone returning from vacation** facing hundreds of unread emails
- **People with email anxiety** — the "unread badge" stress is real

## How It Works

### Email Triage (`scripts/email_triage.py`)
Takes an email export (JSON/CSV) and classifies each message:

```bash
# Triage an email export
python scripts/email_triage.py triage --input emails.json --output triaged.json

# Show summary report
python scripts/email_triage.py report --input triaged.json

# Show only urgent items
python scripts/email_triage.py urgent --input triaged.json
```

### Newsletter Detector (`scripts/newsletter_detector.py`)
Identifies newsletters and promotional emails:

```bash
# Detect newsletters
python scripts/newsletter_detector.py detect --input emails.json

# Generate unsubscribe action list
python scripts/newsletter_detector.py unsubscribe --input emails.json
```

### Quick Reply Generator (`scripts/quick_reply.py`)
Generates suggested responses:

```bash
# Generate replies for emails needing response
python scripts/quick_reply.py generate --input triaged.json --type "meeting_confirm"

# List reply templates
python scripts/quick_reply.py templates
```

### Sample Output

```
$ python scripts/email_triage.py report --input triaged.json

📊 INBOX TRIAGE REPORT
═══════════════════════════════════════
Total emails: 200

BY URGENCY:
  🔴 Critical   (3)  — Respond today
  🟠 High      (12)  — Respond within 24h
  🟡 Medium    (45)  — Respond within a week
  🔵 Low      (140)  — No response needed

BY CATEGORY:
  📧 Newsletter/Promo: 89
  💼 Work/Project:     42
  📱 Notification:     28
  🧾 Receipt:          23
  👤 Personal:         12
  🤝 Social:            6

ACTION NEEDED:
  Reply Now:   15 emails
  File:        45 emails
  Unsubscribe: 34 senders
  Delete:      106 emails

⏱️ ESTIMATED TIME TO INBOX ZERO: 45 minutes
```

## Real-World Example

James returns from a 2-week vacation to 487 unread emails. He exports his inbox to JSON and runs the triage:

```bash
$ python scripts/email_triage.py triage --input vacation_emails.json
$ python scripts/email_triage.py report --input triaged.json
```

The triage identifies:
- **7 critical emails** (client escalations, deadline changes while away)
- **23 high priority** (requests that need responses)
- **89 newsletters** (38 of which he can batch-unsubscribe)
- **243 notifications** (GitHub, Jira, Slack digests — all auto-fileable)
- **125 low priority** (receipts, confirmations, FYIs)

The newsletter detector generates an unsubscribe list, and the quick reply generator drafts responses for the 7 critical emails. James reaches inbox zero in 52 minutes instead of the 3+ hours it would normally take.

## License

MIT — see [LICENSE](LICENSE)
