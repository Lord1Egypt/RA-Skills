---
name: medication-travel-companion
description: "Use when traveling with prescription medications (especially controlled substances, insulin/GLP-1 cold chain, or daily-schedule meds across time zones). Screens a med list against TSA/airport security rules, destination bans, cold-chain storage physics, and supply math; builds timezone-shift dose schedules and a doctor letter."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, health, medications, tsa, insulin, timezone, planning]
---

# Medication Travel Companion

## Overview

Traveling with prescription medications is a minefield of small rules that each carry a big consequence: an Adderall prescription that is legal at home is a **prison-sentence offense in Japan or the UAE**; insulin frozen in a checked hold is destroyed; a controlled substance in an unmarked pill organizer without documentation can be confiscated at any border. This skill turns a med list + trip parameters into a per-medication screening report, a timezone-shift dosing plan, a cold-chain packing protocol, and a doctor's-letter request — before the traveler is standing at security.

The tool is **rule-based and offline**: it screens against a built-in knowledge base of controlled-substance classes, destination restrictions, cold-chain drugs and their stability windows, and TSA-style carry-on rules. It never guesses doses; it flags, plans, and documents.

## When to Use

- The user is flying (domestic or international) with any prescription medication
- Meds include **controlled substances** (stimulants, benzodiazepines, opioids, testosterone) — destination legality must be checked
- Meds include **insulin, GLP-1 agonists (Ozempic/Mounjaro), biologics** — cold chain, never in checked baggage
- Trip crosses **time zones** and the med schedule matters (once/twice daily, basal insulin, blood thinners)
- Trip is **longer than the pills on hand** — early-refill / vacation-override math needed
- Don't use for: choosing medications, adjusting prescribed doses (except safe timezone-shift timing), or emergency medical advice — route those to a pharmacist/doctor.

## Quick Start

```bash
# 1. Screen a med list for a 14-day trip to Japan
python3 scripts/medtravel.py screen \
  --meds "Adderall 20mg 2x daily; Lantus insulin 100u/mL; metformin 1000mg 2x daily" \
  --days 14 --destination japan --pills-on-hand 10

# 2. Shift a twice-daily med across a 7-hour time jump
python3 scripts/medtravel.py schedule --med "metformin 2x daily" --from-tz 2 --to-tz -5

# 3. Generate the doctor's letter request (all required elements listed)
python3 scripts/medtravel.py letter --meds "Adderall 20mg; Lantus insulin" --days 14

# 4. Packing checklist incl. cold-chain protocol
python3 scripts/medtravel.py packing --cold-chain --controlled --days 14
```

## What the Screener Checks (per medication)

| Check | Trigger | Verdict action |
|---|---|---|
| Controlled schedule (US CSA II–V) | name keyword match | Original container + doctor letter + count matches Rx |
| Destination ban/restriction | country KB (Japan/UAE/KSA/Qatar strict on stimulants; Singapore, Greece limit codeine) | **STOP — verify with embassy** before flying |
| Cold chain | insulin, GLP-1, biologics | Carry-on only, 2–8°C unopened, in-use window printed, Frio/cool pouch |
| Liquid form >100 mL | mL/ suspension / injectable | Declare at screening (medically necessary = exempt from 3-1-1) |
| Supply math | days × daily dose vs pills on hand | Early refill flag, vacation-override talking points |
| Insulin in-use clock | opened vial/pen | 28-day room-temp window countdown vs trip length |
| Checked-bag risk | any critical med | Rule: ALL critical meds + 2 extra days split between two carry-ons |

## Timezone Schedule Logic

- **Once daily, wide window** (statins, levothyroxine aside — see pitfalls): take at the equivalent local time on arrival if the gap is 18–30 h; otherwise shift ±1 h per day.
- **Twice daily**: keep ≥8 h between doses; on travel day stretch/squeeze one interval into 8–14 h, then resume local rhythm.
- **Basal insulin**: trips ≤3 days — stay on home-clock time; longer — shift 2–3 h per day toward destination time. Never stack a double dose.
- **Birth control / narrow-window drugs**: fixed interval (≤24 h) — take on home clock the whole trip if zone shift ≤4 h; else use the ±1 h/day ladder.

## Common Pitfalls

1. **Pill organizers instead of original containers for controlled substances.** Legal domestically in practice, but border officers can confiscate unidentified pills. Carry originals + a letter.
2. **Insulin in checked luggage.** Holds drop below freezing and destroy insulin; it must fly in the cabin in a Frio pouch or with gel packs (declared).
3. **Assuming a US prescription is universally legal.** Stimulants are narcotics-class in Japan; codeine is restricted in Greece/Singapore/UAE. Always run the destination check.
4. **Doubling a dose after a long-haul flight.** For nearly every daily drug the safe move is a slightly early/late single dose — never two at once.
5. **Refill math on 30-day controlled scripts.** Insurance vacation overrides exist but the prescriber must file ahead — do this 2 weeks out, not at the airport.

## Verification Checklist

- [ ] Every med got a per-line verdict (no "unknown" left uninvestigated)
- [ ] Destination restrictions checked for controlled substances — embassy confirmation if STOP verdict
- [ ] Cold-chain items: carry-on plan + in-use expiry window printed
- [ ] Timezone plan has no interval shorter than the drug's minimum spacing
- [ ] Doctor letter lists: patient name, drug names + doses, condition, prescriber contact, on letterhead
- [ ] Supply math done; early refill requested if deficit > 0

## Example Session

```
$ python3 scripts/medtravel.py screen --meds "Adderall 20mg 2x; Lantus 100u/mL" \
    --days 14 --destination japan --pills-on-hand 10

MEDICATION TRAVEL SCREEN — 14 days → JAPAN
════════════════════════════════════════════════════
[1] Adderall 20mg, 2x daily
    ⚠ CONTROLLED — Schedule II (stimulant, amphetamine)
    ✖ DESTINATION GATE: Japan treats amphetamine-class stimulants as
      prohibited narcotics. Import without advance permission (about 2-month
      application via MHLW) is a criminal offense.
      → STOP: confirm with the Japanese embassy BEFORE booking. Ask about
        Yakkan Shoumei (import certificate). Do not carry it "just in case".
    ✔ Supply: need 28, have 10 → early refill REQUIRED (+18 pills)
[2] Lantus insulin 100u/mL
    ❄ COLD CHAIN — carry-on ONLY, never checked. Unopened: 2–8°C.
       Opened pen in use: 28 days at room temp (≤30°C).
    🧳 Packing: Frio pouch or gel pack (declare); spare pen in companion bag.
[3] Destination verdict: 1 BLOCKER, 1 COLD-CHAIN, 0 info requests.
```
