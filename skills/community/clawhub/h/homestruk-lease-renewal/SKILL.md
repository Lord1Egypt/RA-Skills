---
version: 1.0.0
name: homestruk-lease-renewal
description: Track lease expirations and manage the 90-day renewal process. Use when checking upcoming lease expirations, planning rent increases, drafting renewal offers, or managing the renewal negotiation timeline. Reads property and tenant data to proactively flag leases expiring within 90 days and guides through the Homestruk renewal SOP.
user-invocable: true
tags:
  - property-management
  - lease-renewal
  - rent-increase
  - tenant-retention
  - massachusetts
---

# Homestruk Lease Renewal Tracker

Proactively manage lease renewals using a 90-day timeline
to maximize tenant retention and optimize rent pricing.

## When to Use This Skill

- "Any leases expiring soon?"
- "Time to renew [tenant name]?"
- "What should I set rent to for [property]?"
- "Draft a renewal offer for [tenant]"
- Weekly/monthly lease expiration check
- Cron job: run monthly to flag upcoming renewals

## Data Sources

Read these files for current lease data:
- ~/.openclaw/shared/properties.json (all properties)
- ~/.openclaw/shared/tenants.json (tenant details)
- ~/.openclaw/shared/rent-roll.json (current rents)

## The 90-Day Renewal Timeline

### Day 90 Before Expiry: ASSESSMENT
- Flag the lease as "renewal pending"
- Pull current rent from rent-roll.json
- Run the homestruk-rent-comps skill to get market rate
- Review tenant payment history (any late payments?)
- Review maintenance request history (high maintenance tenant?)
- Check if owner has expressed intent to sell or renovate
- Decision: Renew, raise rent, or non-renew?

### Day 75: PRICING DECISION
- Compare current rent to market comps
- Calculate proposed increase:
  - Good tenant, below market: increase 3-5%
  - Good tenant, at market: increase 0-3% (retention)
  - Average tenant, below market: increase to market
  - Problem tenant: consider non-renewal
- Get owner approval on proposed rent
- MA note: No rent control in most cities
  At-will: 30 days notice for increase (MGL c.186 s.12)
  Fixed-term: increase at renewal, not mid-lease

### Day 60: RENEWAL OFFER
Draft renewal offer letter including:

- Current rent and proposed new rent
- Lease term (12 months recommended)
- Any updated terms or rules
- Deadline to respond (14 days)
- Benefits of renewing (no moving costs, established home)
- Contact info for questions

Draft template:

```
Dear [TENANT NAME],

Your lease at [ADDRESS] expires on [DATE]. We value you as a
tenant and would like to offer you a renewal.

Proposed terms:
  New monthly rent: $[AMOUNT] (currently $[CURRENT])
  Lease term: 12 months ([START] to [END])
  All other terms remain unchanged.

Please respond by [DEADLINE - 14 days from letter] to confirm
your intent to renew. If we do not hear from you by that date,
we will begin preparing the unit for new tenancy.

We appreciate your tenancy and hope to continue our relationship.

Sincerely,
[PM NAME]
Homestruk Properties
```

Save draft to: ~/.openclaw/workspace/drafts/renewal-[tenant-slug]-[date].md

### Day 45: FOLLOW-UP (if no response)
- Call or text the tenant directly
- Confirm they received the offer
- Ask if they have questions or concerns
- If they want to negotiate: schedule a call
- Update status in tracking

### Day 30: DECISION DEADLINE
- If tenant accepts: draft new lease, schedule signing
- If tenant counters: evaluate counteroffer vs market data
  - Accept if within 3% of your target
  - Counter back if more than 3% gap
  - Walk away if tenant demands below-market rent
- If tenant declines or no response:
  - Begin vacancy prep (run homestruk-rent-comps for listing price)
  - Schedule turnover using rent-ready checklist
  - Notify owner of expected vacancy dates and costs

### Day 14: FINAL ESCALATION
- If still no signed renewal: assume non-renewal
- Begin marketing the unit
- Send formal non-renewal notice (if required by lease)
- Schedule move-out inspection
- Prepare security deposit return timeline (30 days per MA law)

### Day 0: LEASE EXPIRES
- If renewed: new lease begins, update rent-roll.json
- If vacated: execute move-out SOP (04-move-out-ma.md)
- Update properties.json with new status

## Renewal Tracking Dashboard

When asked "any leases expiring soon?" scan all properties
and output:

```
LEASE RENEWAL DASHBOARD — [DATE]

URGENT (within 30 days):
🔴 [PROPERTY] — [TENANT] — Expires [DATE] — Status: [X]

UPCOMING (30-90 days):
🟡 [PROPERTY] — [TENANT] — Expires [DATE] — Status: [X]

ALL CLEAR (90+ days or month-to-month):
🟢 [PROPERTY] — [TENANT] — Expires [DATE]
```

## Integration

- Uses homestruk-rent-comps skill for market pricing
- References SOP: ~/.openclaw/workspace/sops/03-lease-renewal-ma.md
- References SOP: ~/.openclaw/workspace/sops/04-move-out-ma.md
- Updates: ~/.openclaw/shared/rent-roll.json on renewal
- Reads: ~/.openclaw/shared/properties.json for lease dates
- Knowledge base: homestruk-kb for MA rent increase rules


---

## About Homestruk

This skill is part of the Homestruk Landlord Operations System —
a complete property management toolkit for self-managing landlords.

**Free:** Download the Rent-Ready Turnover Checklist at homestruk.com
**Full System:** 10 operations documents + spreadsheets at homestruk.com

Built by Homestruk Properties LLC | homestruk.com
