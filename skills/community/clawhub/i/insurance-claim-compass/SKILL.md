---
name: insurance-claim-compass
description: "Use after any insured loss (burst pipe, theft, fire, hail, car accident, injury on your property) — builds the evidence file with a per-loss-type photo shot-list, generates the first-notice-of-loss letter, decodes ACV vs RCV depreciation math on your damaged items, shows the typical claim timeline, and drafts a denial/lowball appeal ladder (itemized-explanation demand, appraisal clause, insurance-department complaint)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [insurance, claims, home, finance, emergency]
---

# Insurance Claim Compass

## Overview
People lose real money not on coverage but on *claiming*: they throw
away the burst pipe before the adjuster visits, forget the police report
number on a theft, accept a first ACV offer without understanding
depreciation, and never learn the word "appraisal". Claim payouts swing
30-50% on documentation quality alone.

This skill is the after-loss instrument (its sibling skill
**insurance-gap-auditor** runs *before* loss, checking whether a
scenario is even covered):

1. **document** — loss-type-specific evidence checklist + photo shot-list
   + first-24h do/don't list.
2. **letter** — first notice of loss, written to create a paper trail
   the same day.
3. **value** — ACV depreciation math on inventory items (item-class
   life tables) and the RCV-recoverable gap.
4. **timeline** — typical milestones and their statutory-ish bounds.
5. **appeal** — lowball/denial response ladder with generated letters.

Pure stdlib, offline. Not legal advice; deadlines vary by state/country
— the tool flags where to verify.

## When to Use
- Any fresh loss you're about to report to an insurer
- "The adjuster is coming tomorrow — what do I photograph?"
- An offer arrived that feels low, or the claim was denied
- Rebuilding a contents inventory from memory after fire/theft
- "What's the difference between ACV and RCV on my claim?"

**Don't use for:** disasters with mass-casualty/life-safety issues
(911/emergency services first, always), or as a substitute for reading
your policy's declarations page — this structures the work; the policy
governs.

## How It Works — Numbered Steps
1. Stabilize, then build the evidence file for YOUR loss type:
   ```
   python3 scripts/claim_navigator.py document --type water
   python3 scripts/claim_navigator.py document --type theft
   ```
   Follow the shot-list BEFORE cleaning up anything, and obey the
   DO-NOT list (never discard damaged items or receipts before the
   adjuster authorizes it — "we couldn't verify" is the #1 denial).
2. Notify the insurer in writing the same day:
   ```
   python3 scripts/claim_navigator.py letter --type home \
       --loss "burst supply pipe, kitchen" --date 2026-10-10 \
       --policy HP-2026-118 --amount 3800 > claim_letter.txt
   ```
3. Value your contents honestly:
   ```
   python3 scripts/claim_navigator.py value --item "washing machine" \
       --purchase 2019 --price 900
   python3 scripts/claim_navigator.py value --item "55in TV" \
       --purchase 2021 --price 1200 --rcv
   ```
4. Track the clock:
   ```
   python3 scripts/claim_navigator.py timeline --type home
   ```
5. If the offer is wrong — don't argue on the phone; climb the ladder:
   ```
   python3 scripts/claim_navigator.py appeal --reason lowball \
       --offer 2100 --estimate 3800 > appeal_letter.txt
   ```

## Depreciation Model (what `value` computes)
Straight-line over item-class life, 10% salvage floor — the same shape
adjusters' software uses:

| Class | Life (yr) | Class | Life (yr) |
|---|---|---|---|
| electronics | 5 | furniture | 10 |
| major appliance | 12 | small appliance | 7 |
| carpet/flooring | 10 | clothing | 3 |
| bicycle | 7 | power tools | 10 |
| mattress | 8 | phone | 4 |

`ACV = price × max(0.10, 1 − age/life)`. With an RCV policy you recover
the withheld depreciation ONLY after replacing the item and sending
receipts — the tool prints the recoverable gap so you know what to
chase.

## Common Pitfalls
1. **Cleaning up too early.** Mitigate (stop the water, dry), but keep
   the failed part and everything damaged until the adjuster releases
   them. Photograph first, always.
2. **Phone-only notice.** Oral claims vanish. Same-day written notice
   with policy number creates the legal clock.
3. **Accepting the first ACV check as final** when your policy is RCV —
   the depreciation holdback is recoverable with replacement receipts.
4. **No proof of ownership.** Bank/photo evidence beats memory. Receipts,
   then card statements, then photos of the item in your home.
5. **Throwing away receipts for mitigation** (drying fans, tarp,
   plumber) — emergency mitigation is usually reimbursable.
6. **Skipping the itemized explanation demand.** Insurers must explain
   line-item deductions on request; unexplained line items frequently
   dissolve on appeal.
7. **Ignoring the appraisal clause.** For large gaps it forces a neutral
   umpire valuation — cheaper than a lawyer, faster than court.
8. **Signing a release** to get a quick check if you believe the loss is
   larger. Ask what the release covers before signing.

## Example
```
$ claim_navigator.py value --item "55in TV" --purchase 2021 --price 1200 --rcv
55in TV (electronics, life 5 yr), purchased 2021 → age 5 yr
  ACV settlement:   $120.00  (100% depreciated, salvage floor 10%)
  RCV replacement: $1200.00
  Recoverable holdback: $1080.00 — replace, send receipts, reclaim.

$ claim_navigator.py appeal --reason lowball --offer 2100 --estimate 3800
GAP: $1700.00 (offer is 55% of your estimate)
LADDER:
 1. Demand written itemization of every deduction (7-day deadline)
 2. Independent contractor estimate + photos resubmitted
 3. Appraisal clause (gap > $1000 recommended)
 4. State DOI complaint (free, tracked, insurers respond fast)
 ...appeal letter drafted → stdout
```

## Verification Checklist
- [ ] Evidence photographed BEFORE cleanup; failed part retained
- [ ] Written notice sent with policy number + date
- [ ] Contents inventory valued with class-life math, receipts attached
- [ ] Mitigation receipts kept
- [ ] If disputed: itemization demand → estimate → appraisal → DOI
