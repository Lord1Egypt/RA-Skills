---
name: insurance-gap-auditor
description: Use when reviewing family insurance (home/renters, auto, health, life, travel) — walks household-specific scenarios (fire, flood, dog bite, e-bike, home office, basement sewer backup, teen driver) against your policies, flags standard EXCLUSIONS people discover only at claim time (flood vs wind, sewer backup rider, actual-cash-value roofs, jewelry sub-limits), computes true liability limits from net worth, and outputs a gap list with coverage amounts to ask an agent for.
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [insurance, home-insurance, renters, auto, liability, coverage-gaps, personal-finance]
---

# Insurance Gap Auditor

## Overview

Insurance is bought once, in a hurry, and never re-audited. Then the
claim denial teaches the buyer what the policy actually said: "flood"
isn't water from the sky, the roof payout was actual-cash-value on a
17-year-old roof, the jewelry sub-limit was $1,500 not the $12,000 it
cost, and the e-bike isn't a "bicycle" under the policy at all.

This skill runs the audit the agent should run annually:

1. **Scenario engine** — 15+ household risk scenarios (kitchen fire,
   sewer backup, sump overflow, dog bite, guest fall, trampoline,
   e-bike/scooter, home business equipment, teen driver, borrowed car,
   ring lost abroad…) each mapped to: which policy responds, what's
   TYPICALLY covered, what's TYPICALLY excluded or sub-limited.
2. **Exclusion checklist** — the standard gaps in US/UK/EU personal
   lines, with the rider/endorsement that closes each one and typical
   cost bands.
3. **Liability sizing** — umbrella limit computed from net worth +
   income exposure, so liability isn't a guess.
4. **Policy inventory** — record what you actually carry; the audit
   output is a gap list with **specific coverage amounts and rider
   names to request from your agent**.

**Educational tool**: policies vary by insurer, state, and country. The
output is questions and rider names, never a coverage opinion.

## When to Use

- Annual insurance review (or after: moving, renovating, new pet, teen
  driver, home business, big purchases, inheritance)
- "What am I missing?" — the exclusion checklist for home/renters/auto
- "How much liability/umbrella do I need?" — net-worth-based sizing
- Before buying a policy: scenario-test the quotes you're comparing
- After a denial: understand which exclusion bit and what closes it

**Don't use for:** choosing between specific insurers, reading a
specific contract's legal language (the tool encodes market-typical
patterns, not your document), commercial/business policies.

## Quick Start

```bash
# The scenario engine: what happens in each common loss
python3 scripts/insure_audit.py scenarios --filter fire
python3 scripts/insure_audit.py scenarios --group home

# Standard exclusion gaps + the riders that close them
python3 scripts/insure_audit.py exclusions --policy home
python3 scripts/insure_audit.py exclusions --policy auto

# Liability/umbrella sizing from finances
python3 scripts/insure_audit.py liability --net-worth 450000 --income 95000

# Record policies and run the full gap audit
python3 scripts/insure_audit.py policy add --name "Home" --type home \
    --dwelling 380000 --liability 300000 --deductible 2500
python3 scripts/insure_audit.py policy add --name "Auto" --type auto \
    --liability 100000 --deductible 500
python3 scripts/insure_audit.py audit --net-worth 450000
```

## What the Scenario Engine Knows

| Scenario | Responds | Typical gap discovered |
|---|---|---|
| Kitchen fire (own home) | Home dwelling/contents | ACV roof/contents depreciation if not replacement-cost |
| Fire spreads to neighbor | Liability | Limit adequacy vs net worth |
| Flood (external water) | **None — NFIP/private flood** | Standard home EXCLUDES flood |
| Sewer/drain backup | Home **only with rider** | $5–10k backup rider often absent |
| Sump pump failure | Home **only with rider** | Same water-backup endorsement |
| Jewelry/furs theft | Contents with sub-limit | $1–2k sub-limit vs real value → schedule items |
| Home office equipment | Contents, sub-limited | Business property rider if > $2.5k |
| Dog bite (guest) | Liability | Breed exclusions; some states strict liability |
| Trampoline/pool | Liability | Attractive-nuisance exclusions/requirements |
| E-bike/scooter (Class 2/3) | **Neither home nor auto** | Needs bike/moped policy or endorsement |
| Teen driver, family car | Auto | Permissive-use rules; rate/class update |
| Loaner/borrowed car | Owner's policy first | Non-owned coverage gaps |
| Wind/hail | Home (named-peril or all-risk) | 1–2 % hurricane/wind deductible surprise |
| Earthquake | **Rider only** | Standard policies exclude everywhere |
| Laptop lost abroad | Travel/contents | Travel policy or HO contents off-premises limit |

## The Standard Exclusion Gaps (summary)

**Home/renters:** flood, earthquake, sewer backup (rider ~$50–250/yr),
sump overflow, scheduled-valuables sub-limits, business property,
identity theft (rider), ordinance-or-law (rebuilding to new code),
extended replacement cost (inflation guard on dwelling).

**Auto:** liability-only states' uninsured/underinsured motorist (UM/
UIM) stacking, medical payments vs PIP, rental reimbursement, loan/lease
gap coverage, custom parts exclusions.

**Umbrella:** requires underlying limits maintained; excludes intentional
acts, business liability, and typically excludes e-bikes above class.

## Common Pitfalls

1. **"I have home insurance, so I'm covered for water."** Water damage
   is three different things (sudden pipe burst = covered; flood =
   never; backup = rider). Confusing them is the #1 denial.
2. **Insuring the house for market value.** Dwelling coverage must equal
   REBUILD cost (often more than market in high-land-cost areas).
3. **$100k liability on a $600k net worth.** Your liability limit is
   what stands between an accident and your assets. Size it to net
   worth + a few years of income; umbrella is cheap ($150–400/yr per $1M).
4. **Forgetting the umbrella's underlying requirements.** Umbrellas
   require auto liability at e.g. 250/500 — dropping underlying limits
   voids the umbrella at claim time.
5. **Scheduling jewelry AFTER the loss.** Sub-limits apply unless items
   are scheduled with appraisals beforehand.

## Verification Checklist

- [ ] scenarios print respond-policy, typical coverage, gap, and rider
- [ ] exclusions list rider names + typical cost bands per policy type
- [ ] liability sizing yields umbrella recommendation ≥ net worth
- [ ] audit cross-references entered policies against the gap checklist
- [ ] output always framed as questions for your agent, not legal advice

## Examples

```
$ python3 scripts/insure_audit.py scenarios --filter backup
[SEWER BACKUP] water pushes back through drains
  Responds: home policy ONLY IF water-backup endorsement present
  Typical gap: rider limit $5,000-10,000 vs finished-basement loss
  Ask agent: "Do I have water backup & sump overflow coverage? Limit?"

$ python3 scripts/insure_audit.py liability --net-worth 450000 --income 95000
Umbrella sizing: ~$700k-1M recommended...
```

Market-typical patterns for US personal lines (UK/EU notes where they
differ materially). Not legal or coverage advice — the output is the
question list that makes your agent specific.
