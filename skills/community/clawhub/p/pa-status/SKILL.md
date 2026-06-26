---
name: pa-status
description: "PA network health dashboard. Use when: checking if all PAs in the network are active, checking billing status, verifying calendar connections, or generating a network status report. Reads from data/pa-directory.json."
---

# PA Status Skill

## Minimum Model
Any model. Status checks are data-driven and rule-based.

---

## When to Run

- **Daily at 09:00:** Full network report to admin.
- **Immediately on billing error:** Send a partial report for the affected PA.
- **On demand:** If admin asks "what's the status?" → generate the report now.

---

## Status Checks

For each PA in `data/pa-directory.json`, check:

| Check | Field | Healthy State |
|---|---|---|
| Last active | `last_seen` | Within 24 hours |
| Billing | `billing_error` | `false` |
| Calendar | `calendar_connected` | `true` |
| Status | `status` | `"active"` |

---

## Automated Report Script

```python
#!/usr/bin/env python3
import json
import datetime

# Load PA directory
try:
    with open('data/pa-directory.json') as f:
        d = json.load(f)
except FileNotFoundError:
    print("ERROR: data/pa-directory.json not found")
    exit(1)

today = datetime.date.today().isoformat()
online = []
issues = []
offline = []

for pa in d.get('pas', []):
    name = pa['name']
    owner = pa['owner']
    status = pa.get('status', 'unknown')
    model = pa.get('model', 'unknown')

    # Format calendar and billing indicators
    calendar = "✅" if pa.get('calendar_connected') else "❌"
    billing_ok = not pa.get('billing_error', False)
    billing = "✅" if billing_ok else "⚠️ billing error"

    # Classify each PA into online / issues / offline
    if status == 'active' and billing_ok:
        online.append(f"• {name} ({owner}) — {model}, cal {calendar}")
    elif status == 'inactive':
        offline.append(f"• {name} ({owner})")
    else:
        issues.append(f"• {name} ({owner}) — {billing}")

# Print the report
total = len(d.get('pas', []))
print(f"📊 PA Network Status — {today}\n")
print(f"✅ ONLINE ({len(online)}/{total})")
for line in online:
    print(line)

if issues:
    print("\n⚠️ ISSUES")
    for line in issues:
        print(line)

if offline:
    print("\n❌ OFFLINE")
    for line in offline:
        print(line)

if not issues and not offline:
    print("\nAll PAs are healthy 🎉")
```

---

## Directory Schema (With Status Fields)

Add these fields to each PA entry in `pa-directory.json`:

```json
{
  "name": "Aria",
  "phone": "+1XXXXXXXXXX",
  "owner": "Owner Name",
  "owner_email": "owner@company.com",
  "status": "active",
  "model": "your-llm-model",
  "last_seen": "2026-04-01T10:00:00Z",
  "calendar_connected": true,
  "billing_error": false,
  "billing_error_since": null
}
```

Replace `"your-llm-model"` with the actual model ID (e.g. `"claude-haiku-20240307"`, `"gpt-4o-mini"`, `"gemini-1.5-flash"`).

---

## Quick Ping (WhatsApp Reachability)

Use this for real-time check (after the script above):

```
For each PA in the issues list:
  Send: "ping 🏓"
  Wait up to 5 minutes
  If response received: mark ONLINE
  If no response: mark NO_RESPONSE → check whatsapp-diagnostics and billing-monitor skills
```

**Rule:** Only ping PAs that are flagged. Do not ping healthy PAs — it creates noise.

---

## Scheduling

| Frequency | Action |
|---|---|
| Daily at 09:00 | Full network report to admin |
| On billing error | Immediate partial report |
| On demand | When admin asks "what's the status?" |

---

## Cost Tips

- **Very cheap:** Reading a JSON file and formatting a report uses minimal tokens.
- **Small model OK:** Any model can generate this report.
- **Avoid:** Do not ping all PAs at once — send one at a time to avoid rate limits.
- **Batch:** Run the full report once daily instead of checking each PA separately.
