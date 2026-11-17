---
name: noise-nuisance-log
description: "Use when you have a recurring noise problem — upstairs neighbors, barking dogs, construction, loud businesses, nightlife, HVAC equipment, band practice — and need to build a defensible record instead of venting; timestamps every incident with duration, type, and decibel estimate, shows time-of-day and weekday patterns, flags violations of typical night-quiet hours (22:00–07:00) and municipal limits, computes an annoyance/impact score, and generates a ready-to-send complaint letter to the landlord, HOA, or city noise office citing your documented pattern."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [noise, neighbors, landlord, hoa, dispute, evidence, complaint-letter]
---

# Noise Nuisance Log

## Overview

Recurring noise is one of the most common residential conflicts, and the side with the
*record* almost always wins. "It's loud every night" carries no weight with a landlord,
an HOA, or a city noise office; "14 incidents in 30 days, 11 after 22:00, median 47
minutes, mostly bass music, including weeknights before work days" gets a letter sent,
a lease clause cited, or an inspector dispatched. The gap between suffering and
resolution is almost never the noise itself — it's documentation discipline.

This skill is that discipline, distilled:

1. **10-second incident logging** — time, duration, type, estimated loudness, impact
   (woken up / couldn't work / kid disturbed), and a note.
2. **Pattern analysis** — time-of-day histogram, weekday split, night-hours rate,
   per-type totals, trend vs the previous period.
3. **Ordinance context** — typical municipal quiet hours (22:00–07:00) and common
   decibel limits by zone; every incident inside quiet hours is flagged. Adjust to your
   local code (the reference shows how to find it in 10 minutes).
4. **Impact score** — a 0–100 severity index from frequency, night share, duration, and
   sleep disruption, so "how bad is it really" has a defensible number.
5. **Complaint letter generator** — a factual, non-hostile letter to landlord/HOA/city
   citing your documented pattern, the relevant clause concepts (quiet enjoyment,
   nuisance), and a specific remedy request.

## When to Use

- Recurring neighbor noise (music, TV, footsteps, arguments, instruments)
- Barking dogs (yours-to-complain-about, or defending against a complaint about yours)
- Construction/renovation outside permitted hours
- Businesses/venues/HVAC affecting your home
- Preparing for a landlord conversation, HOA complaint, mediation, or a city noise
  office filing — anywhere a pattern beats an anecdote
- Don't use for: one-off events (call non-emergency police line if it's happening now),
  domestic-violence-sounding situations (that's emergency services), or workplace
  noise (different framework entirely).

## Commands

```bash
# Log an incident (start time defaults to now; duration in minutes)
python3 scripts/noise_log.py log --type music --duration 45 --loudness loud \
    --impact "woke us up" --note "bass, clearly audible in bedroom"
python3 scripts/noise_log.py log --type barking --start "2026-09-05 06:15" --duration 20 \
    --loudness moderate --impact "woke baby"
python3 scripts/noise_log.py log --type footsteps --duration 30 --loudness moderate

# Types: music, tv, talking, party, barking, construction, renovation, hvac,
#        traffic, venue, footsteps, other

# The patterns — this is what goes in the letter
python3 scripts/noise_log.py stats            # all-time summary
python3 scripts/noise_log.py stats --days 30
python3 scripts/noise_log.py stats --neighbor "upstairs 4B"   # if you log --neighbor

# Severity score with interpretation
python3 scripts/noise_log.py score

# Time-of-day and weekday distribution
python3 scripts/noise_log.py histogram

# Generate the complaint letter (landlord | hoa | city)
python3 scripts/noise_log.py letter --to landlord \
    --recipient "Jane Smith, Smith Property Mgmt" \
    --your-name "Alex Tenant" --address "Apt 4A, 12 Oak St"
python3 scripts/noise_log.py letter --to city --your-name "Alex Tenant" \
    --address "12 Oak St" --source "venue across the street"

# Manage
python3 scripts/noise_log.py list --limit 10
python3 scripts/noise_log.py export --csv noise-log.csv
```

Log lives at `~/.noise-log.json` (`--file` to override).

## What the Output Looks Like

```
Noise Log — 30 days ending 2026-09-08
  incidents: 14   (3.4/week)   total 9.2 hours
  night-hours (22:00–07:00): 11 of 14  (79%)  ⚠ 11 potential quiet-hours violations
  by type:   music 8 · party 3 · footsteps 2 · barking 1
  weekday vs weekend: 9 weekday · 5 weekend
  peak window: 22:00–01:00 (9 incidents)
  impact: sleep disruption reported in 10 incidents (71%)
  severity score: 68/100 — HIGH (frequent + mostly night + sleep impact)
```

## Common Pitfalls

1. **Logging only the worst nights.** The pattern is the evidence; a log with 3 entries
   in a month reads as "occasional," however brutal those nights were. Log everything
   you'd mention in conversation.
2. **Guessing decibels.** The tool asks for a band (faint/moderate/loud/very loud),
   not a number — because uncalibrated phone dB apps are often inadmissible-quality
   evidence, and a defensible band beats a pseudo-precise number. If you want real
   numbers, the reference explains what makes a measurement credible (calibrated meter,
   documented position) — and that your timestamped pattern usually matters more.
3. **Hostile letters.** The generator is deliberately factual and calm. Insults,
   threats, and speculation ("they're doing it on purpose") sink complaints; dates,
   durations, and impact get results.
4. **Wrong quiet hours.** 22:00–07:00 is the common default, but codes vary (some
   cities use 23:00; some have daytime limits too). Set your local hours with
   `--night-start`/`--night-end` after checking the municipal code — the reference
   shows where to look.
5. **Skipping contemporaneous notes.** Add a one-line `--note` (what it sounded like,
   what you did). "Called the front desk at 23:40, no answer" is a fact that later
   becomes leverage.
6. **Anonymous complaints as step one.** The letter generator includes your name
   because identified, documented complainants get processed; anonymous ones get filed.
   (If you fear retaliation, the reference covers escalation paths that protect you.)

## Verification Checklist

- [ ] Every incident logged same-day (contemporaneous = credible)
- [ ] `--night-start`/`--night-end` match your local ordinance
- [ ] `stats --days 30` shows the real pattern (aim for ≥2 weeks before escalating)
- [ ] Letter reviewed before sending: facts only, specific remedy requested
- [ ] Kept a copy of everything sent, with dates — the paper trail is the asset

## One-Shot Recipes

**Upstairs neighbor, week 3 of nightly music**
```bash
python3 scripts/noise_log.py log --type music --duration 45 --loudness loud --impact "woke us up"
# ...two weeks of this...
python3 scripts/noise_log.py stats --days 14
python3 scripts/noise_log.py letter --to landlord --recipient "Jane Smith, Acme Mgmt" \
    --your-name "Alex Tenant" --address "Apt 4A, 12 Oak St"
```

**Construction starting at 6:00 on Saturdays**
```bash
python3 scripts/noise_log.py log --type construction --start "2026-09-06 06:05" \
    --duration 150 --loudness "very loud" --note "jackhammer; permit says 08:00 start"
python3 scripts/noise_log.py letter --to city --your-name "Alex Tenant" \
    --address "12 Oak St" --source "site at 14 Oak St"
```
