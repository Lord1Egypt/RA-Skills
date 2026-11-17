# Noise Nuisance Log

**In a noise dispute, the side with the record wins. This builds the record.**

Recurring noise is among the most common residential conflicts — and "it's loud every
night" carries no weight with a landlord, HOA, or city noise office. "14 incidents in
30 days, 79% after 22:00, median 47 minutes, sleep disruption in 71%" gets a letter
sent and a lease clause cited. The gap between suffering and resolution is
documentation discipline; this tool is that discipline.

## What it does

- ⏱️ **10-second incident logging** — time, duration, type (12 kinds), loudness band,
  impact, note, and optionally the responsible neighbor/unit
- 🌙 **Quiet-hours flagging** — every incident inside night hours (default 22:00–07:00,
  adjustable to your local ordinance) is marked as a potential violation
- 📊 **Pattern analysis** — incidents/week, night-share, type ranking, weekday split,
  peak time window, sleep-disruption rate
- 🔢 **Severity score** — a defensible 0–100 index (frequency, night share, duration,
  sleep impact) so "how bad is it" has a number
- 📈 **Histograms** — time-of-day and weekday distributions
- ✉️ **Complaint letter generator** — landlord, HOA, or city variants; factual, calm,
  pattern-cited, with a specific remedy request
- 📴 Local JSON storage, pure stdlib, CSV export for mediators/attorneys

## Quick start

```bash
python3 scripts/noise_log.py log --type music --duration 45 --loudness loud \
    --impact "woke us up" --note "bass through ceiling" --neighbor "upstairs 4B"
# ...two weeks of this...
python3 scripts/noise_log.py stats --days 14
python3 scripts/noise_log.py score --days 14
python3 scripts/noise_log.py letter --to landlord \
    --recipient "Jane Smith, Acme Mgmt" --your-name "Alex Tenant" \
    --address "Apt 4A, 12 Oak St"
```

## Who needs this

- Tenants and condo owners dealing with noisy neighbors
- Anyone facing barking dogs, after-hours construction, or intrusive HVAC/venues
- People preparing for mediation, HOA hearings, or municipal complaints
- Landlords documenting a nuisance before an eviction conversation
- Anyone defending *against* a noise complaint (same log, exculpatory notes)

## Example output

```
Noise Log — 30 days ending 2026-09-08
  incidents: 7   (1.6/week)   total 6.8 hours
  night-hours (22:00–07:00): 7 of 7  (100%)  ⚠ 7 potential quiet-hours violations
  by type:   music 4 · party 2 · footsteps 1
  peak window: 21:00–24:00 (6 incidents)
  impact: sleep disruption reported in 6 incidents (86%)
severity score: 67/100 — HIGH (mostly night, long episodes, sleep impact)
```

Ordinance lookup, evidence credibility, and the escalation ladder:
[`references/ordinances-and-evidence.md`](references/ordinances-and-evidence.md)

## License

MIT
