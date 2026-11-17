# Event Duration Defaults

Used by: `sands.create`

When the user does not specify an explicit duration, apply smart defaults based on event
title keywords. User-specified durations always take precedence ("30 minute lunch" → 30 min).

---

## Keyword-to-Duration Mapping

| Keywords (case-insensitive) | Default Duration |
|---|---|
| meeting, sync, standup, 1:1, one-on-one, check-in | 30 min |
| call, phone call | 30 min |
| coffee, tea | 30 min |
| lunch, dinner, brunch | 60 min |
| interview | 60 min |
| doctor, dentist, appointment, checkup | 60 min |
| gym, workout, run, swim | 60 min |
| haircut, barber, salon | 60 min |
| workshop, class, course, lesson | 90 min |
| focus time, deep work | 120 min |
| concert, show, game, performance, recital | 180 min |

## Special Cases

| Keywords | Behavior |
|---|---|
| flight, train, bus (transport) | Do not default — ask the user or extract from details |
| all day, vacation, holiday, PTO | Create as all-day event (no duration needed) |
| reminder | Do not default — ask the user (reminders are not Sands' responsibility, but if the user insists, use 15 min) |

## Fallback

If no keyword matches: default to **60 minutes**.

---

## Override Rules

1. Explicit user duration always wins: "30 minute lunch" → 30 min, not 60
2. Time range always wins: "lunch 12:00-12:45" → 45 min
3. If keyword matches multiple rows, use the first match from the table above
4. If the user says "quick" or "short", halve the default (minimum 15 min)
5. If the user says "long" or "extended", double the default (maximum 240 min)
