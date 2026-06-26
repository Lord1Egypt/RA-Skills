# Escalation, heartbeats, and followups

"Keep poking until I reply" — the family of features that turn a single
fire into a self-sustaining cycle.

## Escalation — rotating tones, custom intervals

```bash
poke --remind "垃圾拿出去了吗？" --on-calendar "Sun *-*-* 19:00:00" \
  --tone "warm,playful,stern,chaotic" \
  --escalation-intervals "60,30,15,10,5,5" \
  --max-pokes 6 --channel CH --target TGT
```

- `--tone "a,b,c"` rotates tones across escalation levels (1st poke uses
  tone a, 2nd uses b, etc.). Single tone is constant.
- `--escalation-intervals "60,30,15,10,5,5"` — gap (in minutes) between
  pokes within one cycle. List walks; if escalation exceeds the list,
  the last value repeats.
- `--max-pokes N` — total pokes per cycle (counting the base fire as #1).
  `-1` means unlimited (default for calendar reminders).

A reply at any escalation level ends the cycle. Recurring schedules
advance to the next base occurrence; one-offs terminate.

## Followup — fire something else if no reply

```bash
poke --remind "Did you take the chicken out?" --once 1h --channel CH --target TGT \
  --if-unconfirmed-remind "You still haven't answered about the chicken." \
  --if-unconfirmed-after 30m
```

- `--if-unconfirmed-remind TXT` — followup is a fresh reminder string.
- `--if-unconfirmed-task TXT` — followup is an agent prompt (`--agent`
  required).
- `--if-unconfirmed-command CMD` — followup is a shell command *(executes under your full user privileges at fire time; only use scripts you wrote or explicitly trust)*.

Exactly one of those three. Then exactly one of these triggers:

- `--if-unconfirmed-after DUR` — time-based (e.g. `30m`)
- `--if-unconfirmed-after-pokes N` — count-based

`--if-unconfirmed-after` works with both `--once` and `--on-calendar`
(the latter is what makes the heartbeat pattern self-sustaining).

The followup fires *once* per cycle, gated by `followup_fired`, and
appends `followup_fired` to history for audit.

## Heartbeat — recurring + followup + escalation

```bash
poke --remind "Are you alive?" --on-calendar "*-*-* 09:00,12:00,17:00" \
  --if-unconfirmed-after 30m --if-unconfirmed-remind "You missed a check-in!" \
  --escalation-intervals "30,15,5" --max-pokes 4 \
  --channel CH --target TGT
```

How it self-sustains:

1. Fires on calendar schedule (9:00, 12:00, 17:00).
2. User confirms → cycle resets; next fire follows calendar.
3. No response within 30m → followup fires ("You missed a check-in!").
4. Still no response → escalation kicks in (30 min, then 15, then 5).
5. Cycle ends on any reply (confirm / cancel / snooze / followup) or
   when `--max-pokes` runs out.

This is the canonical replacement for OpenClaw heartbeat polling — see
`sub-skills/migration.md` for the porting helper.

## Task interval — rate limit on `--task`

```bash
poke --task "Check email." --on-calendar "*-*-* *:0/5" \
  --task-interval "30m" --channel CH --target TGT
```

- Reminder is scheduled to wake every 5 minutes, but only actually
  fires if at least 30 minutes have elapsed since the last `--task`
  run.
- Useful for "wake often enough to catch a window, but don't actually
  do the work every wakeup."
- `--urgent` does NOT bypass task interval (only the soft suppression
  gates 1–6).

## Followup mutual-exclusivity

These pairs error at create time if both are set:

- `--if-unconfirmed-remind` / `-task` / `-command` — pick exactly one.
- `--if-unconfirmed-after` / `-after-pokes` — pick exactly one.

## What `cycle_poke_count` tracks (mental model)

Each fire within a single cycle increments `cycle_poke_count`. The cycle
resets on:

- any user reply (confirm / cancel / snooze / followup),
- recurring base advance to the next occurrence,
- followup firing on a recurring reminder.

Snooze *decrements* the count by one (so "snooze + continue" doesn't
double-count toward `--max-pokes`).
