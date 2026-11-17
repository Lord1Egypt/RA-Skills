---
name: gift-occasion-planner
description: "Use when birthdays, anniversaries, and holidays keep sneaking up on you every single year — maintains a registry of people and their gift occasions (birthday, anniversary, Mother's/Father's Day, etc.) with per-person gift profile (interests, sizes, favorites, taboo list, past gifts), generates a rolling 60-day lookahead of upcoming occasions, recommends what to give based on profile + past-gift history (never repeat, always evolve), budgets per person/occasion with running yearly totals, produces an actionable buying plan per occasion (what, budget, where, wrap, card), and exports ICS reminders at 21/7/1 days out so the era of gas-station flowers on the drive home ends."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [gifts, occasions, reminders, family, budgeting, calendar]
---

# Gift Occasion Planner

## Overview

Gift failure is a memory failure. Every year: the birthday that arrives the day after you remembered it, the anniversary dinner booked nowhere, Mother's Day creeping up between playoff games. The result is the gas-station-flower bailout — expensive, obviously last-minute, and quietly corrosive to relationships.

This skill runs a **gift intelligence system**:

1. **Registry** — people × occasions with dates. Per-person profile: interests, sizes, favorite colors/teams/authors, taboo list ("no clothes", "no sweets"), budget.
2. **60-day radar** — rolling lookahead; every occasion appears 60, 21, 7, 1 days ahead (ICS export puts these in your real calendar).
3. **Recommendation engine** — suggests gifts from profile ∩ history: never repeats, escalates or rotates category by year (year 1 book → year 2 experience → year 3 something from the wish list), respects taboos and budget.
4. **History** — every given gift logged; the engine and the annual "what did I give last year?" panic both read it.
5. **Budget view** — per-person and yearly totals, so December's damage is visible in March.

## When to Use

- **Chronic last-minute gifters** — the core audience; the 60-day radar IS the product.
- **Large families / blended families** — 15+ occasions/year is un-manageable by memory alone.
- **Anniversaries matter to your partner** — the highest-stakes recurring date there is.
- **Budget control** — see the whole year's gift spend upfront and cap it.
- **After any gift lands well** — log it; profiles compound (year 3 recommendations beat year 1's).
- Don't use for: holiday shopping lists for yourself (different problem), corporate gifting programs (different scale/tax rules).

## How It Works

1. **Add people** — `add-person "Mom" --birthday 1958-03-14 --interests "gardening,opera" --taboo "no gadgets"`.
2. **Add occasions** — birthdays auto-created; anniversaries, Mother's/Father's Day, graduations added explicitly. Recurring occasions compute next date automatically.
3. **Radar** — `radar` shows the next 60 days: who, what occasion, days left, budget, recommendation, and status (IDEA / BOUGHT / WRAPPED / GIVEN).
4. **Recommendations** — `recommend <person>` proposes 3-5 options from profile ∩ past-gift history with rationale; you confirm into the plan.
5. **Plan & execute** — `plan <occasion-id>` prints the actionable card: gift, budget, where to buy, wrap idea, card note suggestion, deadline chain (buy-by, wrap-by, mail-by dates).
6. **Log** — `given <occasion-id> --gift "..."` records history and moves on.

## Commands

```bash
# People
python3 scripts/gift_planner.py add-person "Mom" --birthday 1958-03-14 \
    --interests "gardening,opera,birdwatching" --taboo "no gadgets,no sweets" --budget 75
python3 scripts/gift_planner.py add-person "Dad" --birthday 1955-11-02 \
    --interests "woodworking,jazz vinyl" --budget 60

# Occasions (birthdays auto; others explicit)
python3 scripts/gift_planner.py add-occasion "Mom" --kind anniversary --month-day 04-22 --label "Wedding anniversary"
python3 scripts/gift_planner.py add-occasion "Dad" --kind fathers-day

# The radar: next 60 days
python3 scripts/gift_planner.py radar

# What to give?
python3 scripts/gift_planner.py recommend "Mom"

# Lock in a plan
python3 scripts/gift_planner.py plan mom-birthday-2026 --idea "Pruning set + garden kneeler"

# Status machine: IDEA → BOUGHT → WRAPPED → GIVEN
python3 scripts/gift_planner.py status mom-birthday-2026 --set bought

# Log what was given (feeds history so recommendations never repeat)
python3 scripts/gift_planner.py given mom-birthday-2026 --gift "Felco pruning set" --cost 68

# Budget overview
python3 scripts/gift_planner.py budget

# Calendar export: 60/21/7/1-day reminders per occasion
python3 scripts/gift_planner.py ics gifts.ics
```

## Example Session

```
$ python3 scripts/gift_planner.py radar

GIFT RADAR — next 60 days (as of 2026-09-20)

DUE IN 21 DAYS ────────────────────────────────
  Mom — BIRTHDAY (Oct 11)
    Budget: $75   Status: IDEA (nothing planned yet!)
    Interests: gardening, opera, birdwatching
    Recent gifts: bird feeder (2025), opera DVDs (2024)
    Recommendation: rotate category → tool/equipment this year:
      · Felco #2 pruners + holster (garden tool upgrade) ~$65
      · Garden kneeler-stool ~$45
      · Botanical garden season pass ~$70

DUE IN 47 DAYS ────────────────────────────────
  Dad — FATHER'S DAY... no, wait: ANNIVERSARY (Nov 2 is birthday)
  ...

$ python3 scripts/gift_planner.py plan mom-birthday-2026 --idea "Felco pruners + holster"

PLAN: Mom's birthday 2026-10-11 (21 days out)
  Gift: Felco #2 pruners + holster      Budget: $75 (est. $65)
  Where: local garden store or online 2-day ship
  Buy by: 2026-10-04 (buffer for shipping)
  Wrap by: 2026-10-10
  Card angle: "for the rose bed that beat the neighbors again"
  Status: IDEA → run `status --set bought` when purchased
```

## Recommendation Logic

1. **Never repeat** — exact and near-dupe matches against history (token overlap ≥ 60%).
2. **Category rotation** — interests cycle: if last year was gardening-gear, this year suggest opera or birdwatching; same-category twice in a row only if the profile is single-interest.
3. **Taboo filter** — hard exclusion.
4. **Budget fit** — suggestions land within ±20% of per-person budget.
5. **Wish-list escalation** — items marked "mentioned wanting" in notes rank first.

The engine proposes; the human decides. Suggestions carry rationale strings so choices never look arbitrary in the plan card.

## Workflow for an Agent

1. **Onboard**: ask for 3-5 important people + dates; `add-person` each. Birthdays auto-create occasions.
2. **Set budgets** — even rough ones; the yearly budget view depends on them.
3. **Export ICS immediately** — 60/21/7-day reminders in the user's real calendar make the system work even when they forget the system exists.
4. **At T-21**: `radar` → `recommend` → present 3 options with rationale; user picks; `plan` it.
5. **At T-7**: check status; if still IDEA, escalate the reminder and suggest fastest shippable options.
6. **After**: `given` — history keeps future recommendations fresh and non-repeating.

## Common Pitfalls

1. **Populating occasions once and never again** — one-time events (graduation) need annual review; recurring ones don't. `radar` shows "no occasions in window" — that's the cue to check next year's one-offs.
2. **Ignoring taboo lists** — a suggestion the person explicitly banned is worse than a generic gift; the engine filters, but manual plans bypass it.
3. **Setting budgets too tight to be useful** — ±20% flex is built in; a $30 budget producing zero viable suggestions means the budget, not the engine, is wrong.
4. **Logging gifts from memory years back** — pre-history is fine to seed, but mark years clearly; the never-repeat logic treats memory-seeded entries as gospel.
5. **Reminder-only usage** — reminders without profiles produce panic purchases anyway; the profile IS what converts lead time into good gifts.
6. **Mother's/Father's Day dates** — they move (2nd Sunday in May / 3rd Sunday in June US, different elsewhere); the library computes them, don't hardcode.

## Verification Checklist

- [ ] All important people + occasions registered (birthdays at minimum)
- [ ] Profiles carry interests + taboos + budget per person
- [ ] ICS exported with 60/21/7/1-day reminders and imported into real calendar
- [ ] Radar reviewed at least monthly; nothing within 21 days still in IDEA
- [ ] Every given gift logged (`given`) so history compounds
- [ ] Yearly budget total reviewed and accepted
