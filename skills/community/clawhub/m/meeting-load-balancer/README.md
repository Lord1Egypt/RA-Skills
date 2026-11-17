# Meeting Load Balancer

**Turn an exported calendar into an evidence-based meeting audit: where the hours go,
what they actually cost, and what to kill — with simulated before/after numbers.**

Knowledge workers lose 10–20+ hours a week to meetings, and almost nobody measures it.
Calendars fill by accretion: every recurring meeting was individually justifiable and
collectively catastrophic. The hidden damage is fragmentation — a day with four
scattered hours of meetings has zero deep-work blocks left. This tool measures both
the hours and the fragmentation, prices every recurring series in person-hours, and
simulates the effect of killing/shortening/de-densifying before anyone has to argue
about it.

## What it does

- 📥 **ICS import** — Google/Outlook/Apple exports; recurring events expanded (weekly,
  daily, intervals, counts, untils, exclusions), cancelled events dropped
- ⏱️ **Volume metrics** — h/week, weekday split, double-booked minutes, per-series
  and per-attendee totals
- 🧩 **Fragmentation metrics** — ≥90-min focus blocks per week, longest daily block,
  fragmentation hours; batch advice for the worst day
- 💰 **True-cost ranking** — every series priced as person-hours/week
  (duration × attendees × frequency)
- 💊 **Prescriptions** — explicit rules flag meetings to KILL/ASYNC (status-shaped),
  SHORTEN (60→45), DE-DENSITY (weekly→biweekly), or BATCH
- 🔮 **Simulation** — apply the prescriptions virtually: recovered meeting hours and
  recovered focus time, computed before the meeting about meetings
- 👥 **Team mode** — combine several people's exports, find who silently absorbs the
  group's meeting load
- 📴 100% local, pure stdlib, works on a synthetic demo with no calendar at all

## Quick start

```bash
python3 scripts/meeting_load.py demo                        # see it work instantly
python3 scripts/meeting_load.py stats --ics calendar.ics --weeks 4
python3 scripts/meeting_load.py focus --ics calendar.ics --weeks 4 --advice
python3 scripts/meeting_load.py rank --ics calendar.ics --weeks 4
python3 scripts/meeting_load.py simulate --ics calendar.ics --weeks 4
```

Calendar export instructions: [`references/ics-export.md`](references/ics-export.md)

## Who needs this

- ICs whose week disappeared and want proof before saying no
- Managers/leads running meeting audits and team retros
- Anyone proposing a new recurring meeting (check the load first — including theirs)
- Consultants/facilitators doing effectiveness reviews
- Anyone defending focus time with data instead of vibes

## Example output

```
Focus analysis (working 09:00–17:00, block ≥90 min):
  focus blocks: 2.5/week   fragmentation: 3.5 h/week

PRESCRIPTIONS:
KILL/ASYNC  Weekly Status Sync    status-shaped name — replace with written update
SHORTEN     Design Review         60→45min — default to shorter

SIMULATION: meeting hours 1.6 → 1.1 h/week; focus time 10.5 → 11.0 h/week
```

## License

MIT
