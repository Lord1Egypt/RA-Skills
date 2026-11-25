---
name: passport-expiry-radar
description: "Use when a trip is being planned, a passport/ID/license/visa expiry is mentioned, or someone asks 'is my passport still valid for X'. Tracks whole-family travel document validity, applies destination entry rules (6-month / Schengen 3-month-beyond-exit), and back-plans renewal deadlines from real processing times so nobody is denied boarding."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, passport, documents, expiration, visa, family]
---

# Passport Expiry Radar

## The problem it solves
Airlines deny boarding every day to people whose passports are *technically unexpired* but violate the destination's validity rule (many countries require 6 months of validity beyond arrival; Schengen requires validity to extend 3 months beyond planned exit). Families discover one member's expired passport a week before departure. Driver's licenses, visas, residence permits and Global Entry memberships all expire on different clocks with different lead times.

This skill keeps a family-wide registry of document expiries and answers two questions:
1. **"Can I travel to X on date Y with these documents?"** — verdict per document, per traveler.
2. **"When must I start renewing what?"** — renewal-by dates back-planned from published processing times.

## When to trigger
- User mentions an upcoming international trip → run `check` against the registry.
- User asks "how long does my passport need to be valid for Thailand/France/…?"
- User says a passport/license/visa is "expiring soon" or asks when to renew.
- Periodic audit ("what expires in the next 12 months across the family?").

## Steps
1. Load or create the registry (`~/.passport_radar.json` or a path the user gives). Each entry: traveler, doc type, issuing country, number suffix (never store full numbers unless the user insists), issue date, expiry date, blank pages (optional).
2. `status` → list every doc with days-to-expiry and a band:
   - **EXPIRED** (< 0 days) — renew immediately, travel blocked.
   - **RENEW NOW** (< 90 days) — routine processing windows no longer comfortable.
   - **PLAN** (90–180 days) — renew at leisure, avoid peak season.
   - **OK** (> 180 days).
3. `check --dest XX --arrival DATE --exit DATE` → for each passport apply the destination rule from `references/destination-rules.md`:
   - validity-beyond-arrival rule (6 months etc.), validity-beyond-exit rule (Schengen 3 months), just-valid rule (Mexico/Canada/UK …)
   - blank-page requirement, machine-readability notes
   - verdict: **CLEARED / RENEW-FIRST / BLOCKED** with the exact date the passport must be valid to.
4. Back-plan renewals: renewal-by = travel date − buffer (7 days) − destination validity requirement; report which processing tier (routine / expedited / urgent agency appointment) makes it.
5. Print a family dashboard: per traveler, per doc, worst-case blocker named.

## Rules the engine encodes (summary)
- Schengen: passport valid **3 months beyond intended exit**, issued within 10 years (some carriers enforce this even where border officers don't).
- ~60 countries incl. China, Thailand, Egypt, Turkey, Indonesia, UAE: **6 months validity beyond arrival**.
- USA, Mexico, Canada, UK, Japan: valid for the duration of stay (Canada/US land: enhanced DL acceptable).
- Renewal processing bands (US example): routine 4–8 weeks, expedited 2–3 weeks, urgent agency appointment ≤14 days before travel. Non-US: see references.
- Kid passports (US under-16) valid only 5 years — the classic family trip-killer.

## Pitfalls
- **Never assume the weakest rule.** The airline, not the immigration officer, is usually who blocks you — carriers enforce the letter of the rule.
- Name changes after marriage: passport in old name + ticket in new name = check-in problems; flag mismatches in the registry.
- Some countries count validity "beyond arrival", others "beyond exit" — the engine distinguishes; do not eyeball it.
- Two blank facing pages (South Africa), machine-readable zone, no water damage — include as secondary checks, not just dates.
- Kid passports expire far sooner than parents expect — always surface children's docs first.

## Example
```
$ python3 scripts/passport_radar.py check --dest TH --arrival 2027-02-10 --exit 2027-02-24
THAILAND: passport must be valid ≥ 6 months beyond arrival → until 2027-08-10
  Mom    P***4821 exp 2029-03-01   CLEARED (valid past 2027-08-10)
  Dad    P***9917 exp 2027-04-02   RENEW-FIRST: expires 130 days before the required 2027-08-10
  Kid(U12)P***3320 exp 2026-12-15  BLOCKED: expires before arrival → urgent renewal + consent letters
Renewal verdict for Dad: routine OK if renewed by 2026-11-28; after that, expedited ($60) until 2027-01-05.
```

## Files
- `scripts/passport_radar.py` — registry + status + trip check + renewal back-planner (stdlib only).
- `references/destination-rules.md` — validity rules for ~30 common destinations, how to verify.
- `references/renewal-times.md` — processing-time bands for US/UK/EU/CAN/AUS passports and ID docs.
- `README.md` — real-world problem framing.
