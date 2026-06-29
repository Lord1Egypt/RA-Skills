# ndis-incident-reporting-specialist

**Skill for:** OpenClaw · Hermes Agent · Claude
**Region:** 🇦🇺 Australia only
**Version:** 1.0.0

---

## What it does

Turns an AI agent into an NDIS reportable incident specialist for Australian registered and unregistered providers. Takes a raw, informal account of what happened and determines whether it's reportable to the NDIS Quality and Safeguards Commission, identifies the correct category, states the exact notification timeframe, and drafts an audit-ready incident report — grounded in the NDIS Act 2013 (ss 73Z–73ZA) and current NDIS Commission incident reporting guidance.

Pairs naturally with [`ndis-progress-note-claiming`](https://github.com/arbazex/ndis-progress-note-claiming) — together they cover routine documentation (progress notes/claiming) and incident documentation, the two heaviest admin burdens for NDIS support workers.

---

## Coverage

| Capability                                                                          | Included |
| ----------------------------------------------------------------------------------- | -------- |
| Reportable vs internal-only incident triage                                         | ✅       |
| All 6 reportable incident categories                                                | ✅       |
| 24-hour vs 5-business-day timeframe logic                                           | ✅       |
| Initial notification draft                                                          | ✅       |
| Full 5-business-day follow-up report draft                                          | ✅       |
| Audit red flag identification (vague language, missing timestamps, opinion-as-fact) | ✅       |
| Record retention guidance (7 years)                                                 | ✅       |

---

## How to install

**OpenClaw / ClawHub:**

```
clawhub skill install ndis-reportable-incident-reporting
```

**Manual (Claude / Hermes):**
Copy the contents of `SKILL.md` into your agent's system prompt or skill slot.

---

## Important limitations

- **Not legal advice.** Drafts should be confirmed with a compliance lead or the NDIS Quality and Safeguards Commission (1800 035 544 / ndiscommission.gov.au) for ambiguous or high-severity cases.
- **No external API calls.** Pure reasoning + instructions only. No env vars, no bins, no network required.
- **Behaviour Support Plans are out of scope.**

---

## License

MIT
