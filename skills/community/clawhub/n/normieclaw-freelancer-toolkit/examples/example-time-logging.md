# Example: Conversational Time Logging Session

A real session showing how Freelancer Toolkit handles different time logging styles.

---

## Simple Time Entry

**You:** I worked 3 hours on the Acme redesign today

**Agent:**
```
✅ Logged: 3.00 hrs — Acme Corp → Website Redesign
   "Website redesign work"
   Date: March 10, 2026 | Billable | Rate: $85/hr ($255.00)
```

---

## Detailed Entry with Description

**You:** Just finished 2.5 hours on BrightPath, built out the API integration for the user dashboard

**Agent:**
```
✅ Logged: 2.50 hrs — BrightPath → Mobile App
   "Built out the API integration for the user dashboard"
   Date: March 10, 2026 | Billable | Rate: $95/hr ($237.50)
```

---

## Past Date Entry

**You:** Yesterday I did 45 minutes of admin — catching up on emails and organizing project files

**Agent:**
```
✅ Logged: 0.75 hrs — (No client) → General
   "Catching up on emails and organizing project files"
   Date: March 9, 2026 | Non-billable | Category: admin
```

---

## Ambiguous Client

**You:** Spent 4 hours on the Nova project, typography system

**Agent:**
```
I found 2 clients matching "Nova":
  1. Nova Labs (Brand Guide — active)
  2. Nova Design Co (Logo Package — active)

Which one?
```

**You:** Nova Labs

**Agent:**
```
✅ Logged: 4.00 hrs — Nova Labs → Brand Guide
   "Typography system"
   Date: March 10, 2026 | Billable | Rate: $75/hr ($300.00)

⚠️ Heads up: Nova Labs Brand Guide is at 92% of budget
   (18.5 of 20 estimated hours used). Consider flagging with the client.
```

---

## New Client On-the-fly

**You:** I worked 2 hours for Pinnacle Studios on their pitch deck

**Agent:**
```
I don't have a client called "Pinnacle Studios." Want me to create them?

I'll need:
  • Hourly rate (or use your default of $75/hr)
  • Contact email (optional)
  • Payment terms (optional, default: net 30)
```

**You:** $110/hr, net 15, email is mark@pinnaclestudios.com

**Agent:**
```
👤 Created client: Pinnacle Studios
   Rate: $110/hr | Terms: Net 15
   Contact: mark@pinnaclestudios.com

📁 Created project: Pitch Deck (hourly billing @ $110/hr)

✅ Logged: 2.00 hrs — Pinnacle Studios → Pitch Deck
   "Pitch deck work"
   Date: March 10, 2026 | Billable | Rate: $110/hr ($220.00)
```

---

## Start/Stop Timer

**You:** Start tracking Acme redesign

**Agent:**
```
⏱ Timer started: Acme Corp → Website Redesign
   Started at: 2:00 PM
   I'll keep tracking until you say stop.
```

**You (2 hours later):** Stop tracking

**Agent:**
```
⏱ Timer stopped: 2.25 hrs — Acme Corp → Website Redesign
   Started: 2:00 PM | Stopped: 4:15 PM
   
   Add a description? (or I'll save as "Timer session")
```

**You:** Client feedback call and revisions to hero section

**Agent:**
```
✅ Logged: 2.25 hrs — Acme Corp → Website Redesign
   "Client feedback call and revisions to hero section"
   Date: March 10, 2026 | Billable | Rate: $85/hr (free1.25)
```

---

## Editing a Previous Entry

**You:** Actually, that Acme entry should be 2.5 hours, not 2.25

**Agent:**
```
✏️ Updated: Acme Corp → Website Redesign (March 10)
   Changed: 2.25 hrs → 2.50 hrs
   New amount: $212.50 (was free1.25)
```

---

## End-of-Day Summary

**You:** What did I log today?

**Agent:**
```
📋 Today: March 10, 2026

• Acme Corp → Website Redesign — 3.00 hrs ($255.00)
• Acme Corp → Website Redesign — 2.50 hrs ($212.50)
• BrightPath → Mobile App — 2.50 hrs ($237.50)
• Nova Labs → Brand Guide — 4.00 hrs ($300.00)
• Pinnacle Studios → Pitch Deck — 2.00 hrs ($220.00)
• Admin (non-billable) — 0.75 hrs

Total: 14.75 hrs
Billable: 14.00 hrs ($1,225.00)
Non-billable: 0.75 hrs

That's a big day. 🔥
```
