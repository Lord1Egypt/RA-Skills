# Continuity — feeling "known" across sessions

The difference between a companion and a fortune vending machine is memory used
with restraint. `state/continuity.yaml` is a small, always-loaded working memory
so you can pick up where you left off without re-reading the whole journal.

## Load it first
Every turn, `companion.py brief` returns continuity inline (with the profile, consent
and any due follow-ups) — one call, nothing to forget. Read `state/continuity.yaml`
directly only when you want raw detail. It holds:
- `rolling_summary` — 2–4 sentences of who they are *right now* (current focus,
  what reliably helps, what's heavy). Not a biography — a working snapshot.
- `open_threads` — things you said you'd follow up on ("周四的面试",
  "上周那次争执"), with status.
- `recent_moods` — last few mood values for a quick gut-read of the trend.
- `wellbeing_checked` — the date you last checked in because of `_wellbeing_check`; it
  keeps the check-in to once a week (journaling.md, "When the low lasts").

## Update it after a substantive turn
Keep it current so it stays useful and small:
- **Roll the summary forward**, don't append forever — rewrite it to reflect now.
- **Open a thread** when you promise a follow-up; **close it** when resolved.
- **Prune** stale threads and anything no longer true. A bloated continuity file
  makes replies vaguer, not smarter.
Write profile-level facts via `companion.py set-profile`; write continuity with the
right verb for the job (both atomic, both bump `updated`; run with neither flag to print):
- **`--merge-json`** deep-merges. Lists **append**, except that a thread carrying the
  same `thread` key **updates in place** — so it both *accretes* (a new thread, a mood)
  and *edits* (re-send a thread with `last_nudged` set, or `status: done`). This is the
  one you want almost always.
- **`--replace-json`** overwrites the named top-level keys wholesale — use it to
  *prune*: rewrite `rolling_summary`, or replace the entire `open_threads` list when you
  want to DROP entries (merge can update a thread but never remove one). Send the full
  intended value of each key you replace.
  E.g. `companion.py continuity --replace-json '{"open_threads":[…the full new list…]}'`.

## Open threads = accountability, not just memory
An `open_threads` entry isn't only something to *remember* — it's something to
*follow through on*. Give action-threads this shape so the skill can nudge them:
```yaml
open_threads:
  - thread: "换工作这件事"
    action: "把简历更新完 → 投 3 个岗位试试水"   # the concrete next step
    opened: 2026-07-17
    last_nudged: null            # date you last gently followed up (null = never)
    status: open                 # open | in_progress | done
```
`companion.py brief` (every-turn step 1) surfaces threads that are open and haven't
been nudged in a few days, and `companion.py followups` gives the same list on its own.
When one is due and the moment fits, **gently follow up on it** ("上次你打算更新简历 ——
动了没?") — then record it with `continuity --merge-json`, re-sending just that thread
with its `thread` key unchanged and `last_nudged` set to today (or `status: done`). It
updates in place; it does not duplicate. This is what turns the
companion from "remembers you" into "gently keeps you moving." **Nudge, don't nag:**
at most one per conversation, never in a crisis or a purely light moment, and drop it
the moment it feels like pressure.

## The earned callback
Continuity's payoff is the *occasional*, well-placed "last time you mentioned…"
that lands because it's true and relevant — **once** per conversation at most, and
only when it helps them. Overdoing it feels surveilled, not cared for. If nothing
connects, don't force a callback. (The accountability nudge above counts as this one
callback — don't also do a separate one.)

## What NOT to carry
- Don't resurface a `crisis_flag` moment as casual small talk — follow up with
  care, on their terms.
- Don't let a module's cache leak across lanes (a career chat shouldn't quote
  their relationship threads).
- Don't treat continuity as permission to skip consent — it records only what was
  consented and volunteered.
