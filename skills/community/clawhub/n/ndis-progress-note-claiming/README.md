# ndis-progress-note-claiming

**Skill for:** OpenClaw · Hermes Agent · Claude  
**Region:** 🇦🇺 Australia only  
**Version:** 1.0.0

---

## What it does

Turns an AI agent into an NDIS documentation and claiming specialist for Australian registered and unregistered providers. The agent collects context, then drafts audit-safe progress notes, identifies correct support catalogue line item codes, and troubleshoots claiming errors — all grounded in the NDIS Pricing Arrangements and Price Limits 2025–26 (V1.1, effective 24 November 2025) and NDIS Practice Standards.

---

## Coverage

| Capability                                                            | Included |
| --------------------------------------------------------------------- | -------- |
| Shift note drafting (Standard, SOAP, DAP formats)                     | ✅       |
| Objective language rules and goal referencing                         | ✅       |
| Audit red flag identification (copy-paste, vague entries)             | ✅       |
| All 15 NDIS support categories explained                              | ✅       |
| High-frequency line item code reference table                         | ✅       |
| Time-of-day code variants (weekday/Sat/Sun/PH)                        | ✅       |
| Group vs individual claiming rules                                    | ✅       |
| Provider travel rules (including 50% therapy travel from 1 July 2025) | ✅       |
| Non-face-to-face claiming eligibility                                 | ✅       |
| Short-notice cancellation rules                                       | ✅       |
| Service Agreement requirements                                        | ✅       |
| Claiming error troubleshooting                                        | ✅       |
| Audit documentation checklist                                         | ✅       |

---

## How to install

**OpenClaw / ClawHub:**

```
clawhub skill install ndis-progress-note-claiming
```

**Manual (Claude / Hermes):**  
Copy the contents of `SKILL.md` into your agent's system prompt or skill slot.

---

## Important limitations

- **Not clinical or legal advice.** Every response includes a disclaimer directing users to the NDIS Quality and Safeguards Commission (1800 035 544 / ndiscommission.gov.au) for complex compliance matters.
- **Verify codes and prices.** Line item codes and price limits change each financial year. The skill instructs the agent to direct users to the official NDIS Support Catalogue at ndis.gov.au/providers/pricing-arrangements before claiming.
- **Behaviour Support Plans are out of scope.** BSPs require a registered Behaviour Support Practitioner.
- **No external API calls.** Pure reasoning + instructions only. No env vars, no bins, no network required.

---

## Key references

- NDIS Pricing Arrangements and Price Limits 2025–26 V1.1: [ndis.gov.au/providers/pricing-arrangements](https://www.ndis.gov.au/providers/pricing-arrangements)
- NDIS Support Catalogue: [ndis.gov.au/media/support-catalogue](https://www.ndis.gov.au/providers/pricing-arrangements)
- NDIS Quality and Safeguards Commission: [ndiscommission.gov.au](https://www.ndiscommission.gov.au)
- Claiming troubleshooting: [ndis.gov.au/providers/working-provider/getting-paid/claims-and-payments-troubleshooting](https://www.ndis.gov.au/providers/working-provider/getting-paid/claims-and-payments-troubleshooting)

---

## License

MIT
