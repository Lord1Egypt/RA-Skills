# Quiet hours, active hours, and DND

Three orthogonal suppression mechanisms. `--urgent` bypasses all three —
but NOT the task interval or dependency gates (see escalation.md and
multi-channel.md respectively for those).

## Mental model

A reminder fires whenever it's scheduled — including 3am — unless one
of these is set: per-reminder `--quiet-hours`, per-reminder
`--active-hours`, or DND. No implicit protection. There is no global
default quiet-hours window; declare it per reminder when you want it.

## Per-reminder quiet hours

```bash
poke --remind "Standup." --on-calendar "Mon..Fri *-*-* 09:00:00" \
  --quiet-hours "22:00-08:00" --channel CH --target TGT
```

- Per-reminder, declared at create time. Static.
- Suppresses delivery during the window. **Delays** to the end of quiet
  hours; doesn't drop.
- Wraps midnight correctly (`"22:00-08:00"` works).

## Active hours — inverse of quiet, per-reminder

```bash
poke --remind "Standup." --on-calendar "Mon..Fri *-*-* 09:00:00" \
  --active-hours "08:00-22:00" --channel CH --target TGT
```

- Per-reminder. Delivery only happens DURING this window.
- If a fire lands outside, delays until the active window opens.
- `--urgent` bypasses.

## DND — global, dynamic

Applies to ALL reminders globally. Unlike quiet hours (static,
per-reminder) DND is set ad-hoc and expires.

```bash
poke --dnd                   # show current DND status
poke --dnd-until "30m"       # enable for 30 minutes
poke --dnd-until "14:00"     # enable until 2pm
poke --dnd-until "2h"        # enable for 2 hours
poke --dnd-off               # disable
```

When DND is active, every non-urgent reminder delays until DND expires.

## `--urgent` bypass asymmetry

`--urgent` bypasses gates 1–6:

1. Snooze window
2. DND
3. Quiet hours (per-reminder)
4. Active hours
5. Flood guard (5 deliveries / 60s)
6. Busy-lane (other OpenClaw lanes recently active)

`--urgent` does NOT bypass:

7. Task interval (`--task-interval` minimum gap between fires)
8. Dependency resolution (`--depends-on`)

Use `--urgent` for things that absolutely must fire on time (medication,
critical alarms). Don't reach for it casually — it's the user's "ignore
my quiet hours" override.

## Testing clock-dependent behavior

Set `POKE_NOW_OVERRIDE` to an ISO timestamp to pin the engine's idea of
"now" at delivery time. The override flows through quiet-hours,
active-hours, and DND checks, so tests can exercise specific windows
deterministically regardless of the wall clock.

```bash
POKE_NOW_OVERRIDE="2026-05-28T03:00:00Z" poke --deliver tr-...
```

## Agent behaviour — the full conversation flow

When the user asks for a reminder that lands inside what looks like
quiet hours:

### Step 1 — if the fire time is inside the window the user described, ask

Don't silently schedule. Don't claim "won't fire until 8am" without
actually making it true. The ask:

> That's during your quiet hours (22:00–08:00). Want me to:
> (a) make it urgent so it fires on time,
> (b) schedule it with quiet hours so it actually waits until 08:00, or
> (c) move it to a different time?

### Step 2 — schedule with the right flag, depending on the answer

- **(a) urgent** → `poke ... --urgent` — fires at 3am, bypasses quiet hours.
- **(b) quiet-hours this one** → `poke ... --quiet-hours "22:00-08:00"` —
  scheduled at 3am, runtime defers delivery to 08:00.
- **(c) different time** → user picks; reschedule accordingly.

## One real anti-pattern worth naming

❌ **Reaching for `--urgent` as the default "yes, fire it" answer.**
Urgent bypasses DND too, which the user may have set for a reason. If
the user wants the reminder to fire at 3am despite a quiet-hours window
they declared, that usually means "this one shouldn't have quiet hours
in the first place" — just leave `--quiet-hours` off, not "override
every gate I've set."
