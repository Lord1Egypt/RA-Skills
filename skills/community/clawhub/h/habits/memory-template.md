# Working File Templates — Habits

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration keys and preference areas alike | `~/Clawic/data/habits/config.yaml` | Key by key, read-modify-write |
| Habit roster, retired habits, patterns, what works, capacity context, cadences, box index | `~/Clawic/data/habits/memory.md` | Rewritten in place; stays small |
| Completions, misses and freezes, day by day | `~/Clawic/data/habits/logs/<year>-<month>.md` | One file per month, one row per date |
| Weekly reviews, monthly rollups, quarterly audits | `~/Clawic/data/habits/reviews/<year>.md` | Append-only, cut by year |
| Things the user re-reads whole — routines, quit plans, restart protocols, commitment contracts, audit verdicts | `~/Clawic/data/habits/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A measured series the habit log cannot hold — pages, minutes, spend per week | `~/Clawic/data/habits/<plural-noun>.md` | One row per measurement; the log stays binary |
| Accountability partners, coaches, anyone named | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, one address book for every skill |
| Body numbers — weight, resting heart rate, blood pressure | `~/Clawic/data/health/` (**shared**) | A series per metric; never inside a habit log |
| Gym memberships, tracker subscriptions, paid stakes | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per recurring payment |
| **Anything durable this table does not name** | `~/Clawic/data/habits/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed. Every row below happens in the same turn as the event, not at some later tidy-up.

| It happened | Write |
|---|---|
| A day was completed, missed, frozen, or corrected | Today's cells in `logs/<year>-<month>.md` |
| A habit was defined, redefined, paused, or restarted | Its row in `## Habits`, all ten fields |
| A habit graduated, was dropped, or was superseded | Move the row to `## Retired`; never delete it |
| A best streak was beaten | The `Best` cell of the roster row, with the date it ended |
| A condition was observed twice on this person | Its row in `## Patterns` — stated out loud only at four samples (Rule 8) |
| A tactic, environment change, stake, or reward worked or backfired | `## What Works` |
| A review, rollup, or audit ran | The entry in `reviews/<year>.md`, plus `Last run` and `Next due` in `## Due` |
| A cadence was accepted or changed, or a pause got an end date | `## Due` |
| A routine, quit plan, restart protocol, contract, or audit verdict was agreed | `artifacts/<kebab-name>.md`, with its `## Boxes` line |
| A partner, coach, or group was named, changed, or dropped | The shared `contacts.md`; only the name stays in the roster row |
| A body number came up in passing | The shared `health/` box |
| A paid stake or membership started or was cancelled | The shared `finances/subscriptions.md` |
| The user described their capacity, schedule, or a hard constraint | `## Context` |
| The user stated a preference | Its key in `config.yaml` |
| A new month started | The new `logs/<year>-<month>.md` and its `## Boxes` line |

## Start flat, split only when it hurts

`memory.md` holds everything except logs, reviews, artifacts and the shared boxes — those four are born as their own files because a log grows without end and an artifact is read whole. Everything else starts as a section and splits only under this procedure:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — headings, hints and scaffolding do not count — then, in the same turn: create the new file in `~/Clawic/data/habits/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a routine or a quit plan is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Tracker exports, contracts and gym paperwork carry logins; store the pointer in place of the value, in this shape: `<kind>:<locator>`.

`env:TRACKER_TOKEN` · `keychain:habit-app` · `1password:Personal/Gym` · `bitwarden:Personal/Strava` · `file:~/.config/tracker/creds`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `api_key: <env:TRACKER_TOKEN>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: habit names and cue text, times of day, streaks, rates and quantities, the tracker app's name, the gym's name, a partner's name and which channel they prefer, the amount and currency of a stake, a quit target and its daily spend. **Secrets, strip them**: API tokens and export URLs carrying a key, app and gym account passwords, session cookies, 2FA recovery codes, card and bank details behind a forfeit or an escrow, and any share link that grants access on its own.

One more line that is not about credentials: a lapse note records the user's own trigger. Other people who appear in it are named, never described.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [logs/](#logs) · [reviews/](#reviews) · [artifacts/](#artifacts) · [shared contacts box](#shared-contacts-box) · [shared health box](#shared-health-box) · [shared finances box](#shared-finances-box) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/habits/` if it does not exist.

```yaml
max_active_habits: 3
week_start: monday
day_boundary: "04:00"
primary_metric: completion-rate
streak_freeze_budget: 1
checkin_style: batch
review_day: sunday
stakes_allowed: false
external_tracker: none

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  done_means: "gym = badge scanned, not a session logged"
platform:
  working_days: [mon, tue, wed, thu, fri]
output_register: neutral        # neutral | encouraging
scope:
  off_limits: [diet, screen time]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Habits Memory

## Boxes
- Daily log, current month → `logs/2026-07.md`; read before any rate, streak or "how am I doing"
- Daily log, previous month → `logs/2026-06.md`; read when the 28-day window crosses the 1st
- Reviews (11 entries) → `reviews/2026.md`; read before a weekly review or a quarterly audit
- Morning routine → `artifacts/routine-morning.md`; read when the morning routine is discussed, rebuilt, or has lapsed
- Quit plan, vaping → `artifacts/quit-vaping.md`; read before any conversation about vaping, and immediately after a lapse

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Weekly review | week, sunday | 2026-07-19 | 2026-07-26 |
| Monthly rollup | month, first session | 2026-07-01 | 2026-08-01 |
| Quarterly audit | quarter | 2026-04-05 | 2026-07-05 |
| Freeze budget reset | month | 2026-07-01 | 2026-08-01 |
| Spot check: graduated "floss" | 3 months | 2026-05-02 | 2026-08-02 |

## Habits
| Name | Type | Cue | Minimum | Frequency | Why | Started | Clean since | Best | Notes |
|------|------|-----|---------|-----------|-----|---------|-------------|------|-------|
| gym | do | after dropping the kids at school | change into kit and leave the house | 3×/week | "still carrying my own suitcase at 70" | 2026-03-02 | — | 9 weeks (ended 2026-06-14) | partner: Marta |
| read | do | after getting into bed | one page | daily | "I miss finishing books" | 2026-05-11 | — | 41 days (ended 2026-07-08) | 14-day floor halved once |
| vaping | avoid | — | substitution: 3-min walk | daily clean | "the cough" | 2026-06-20 | 2026-07-05 | 14 days (ended 2026-07-04) | 4.50 EUR/day saved |

## Retired
| Name | Outcome | Final rate | Best | Retired | What was tried |
|------|---------|------------|------|---------|----------------|
| floss | graduated | 97% | 112 days | 2026-05-02 | anchored after brushing; automatic by week 7 |
| journal | dropped | 31% | 6 days | 2026-04-18 | 3 cues tried (coffee, commute, bed); no time slot survived a work week |

## Patterns
| Pattern | Samples | First seen | Acting on it |
|---------|---------|------------|--------------|
| Misses cluster on Fridays | 6 Fridays | 2026-04 | Friday runs a 10-minute version; rate moved 58% → 84% |
| Rate falls the week after travel, not during | 3 trips | 2026-05 | Not yet — needs a fourth sample (Rule 8) |

## What Works
| Date | Tried | Outcome |
|------|-------|---------|
| 2026-03-09 | Kit laid out the night before | Worked; rate 61% → 88% over two weeks |
| 2026-04-02 | 20 EUR forfeit to a partner | Backfired — misses stopped being reported. Stakes off since |
| 2026-06-21 | Phone charging outside the bedroom | Worked for reading; unrelated habits unaffected |

## Context
Shift work, two nights a week. Day boundary set to 10:00 because of it. Newborn since 2026-06; capacity halved and maintenance mode agreed until September.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every cadence this skill accepts lands here: check-in time, review day, monthly rollup, quarterly audit, freeze reset, partner check-in, contract end date, pause resumption, graduated-habit spot check.
- **`## Habits`**: the six fields of Habit Anatomy plus `Started`, `Clean since`, `Best`, `Notes`. `Clean since` is `—` for `do` habits and the date of the last lapse for `avoid` ones. `Best` carries the date it ended, because it is the only number a rolling window cannot recover. **The current streak is never stored** — it is recomputed from the log every time (`tracking.md`). `Notes` holds the partner's name only, never their contact details.
- **`## Retired`**: `Outcome` is `graduated` · `dropped` · `superseded`. A row is moved here, never deleted: `What was tried` is what stops the same design being proposed again next quarter.
- **`## Patterns`**: `Samples` is a count of the observations, not a feeling. A pattern below four samples is recorded so the count can grow, and is not said out loud (Rule 8).
- **`## What Works`**: one row per intervention with its result, including the ones that backfired — those are the more valuable half, and they are what `stakes_allowed: false` is usually made of.
- These headings are exactly the ones the split files get, so a split stays a copy-paste.

## logs/

One file per month at `~/Clawic/data/habits/logs/<year>-<month>.md`. One row per date, one column per **active** habit, retired ones dropped at rollover. Symbols are defined once, in `tracking.md`: `y` done · `n` scheduled and missed · `-` not scheduled · `f` freeze · blank unknown.

```markdown
# Habits — 2026-07

| Date | gym | read | vaping | Note |
|------|-----|------|--------|------|
| 01 Wed | y (32 min) | y (14 pages) | y | |
| 02 Thu | - | y | y | |
| 03 Fri | n | y | y | gym: Friday again |
| 04 Sat | - | y | n | vaping lapse: bar, after the second drink |
| 05 Sun | f | y | y | f: flight, declared 03 Jul |
```

- A quantity rides in parentheses inside the habit's own cell (`y (32 min)`), so the grid stays binary and the rate math stays valid. `Note` holds reasons: a freeze's declared cause, a lapse's trigger, a correction.
- Blank is not `n`. Blank is absence of evidence and shrinks the window; `n` is evidence of a miss and lowers the rate.
- Never add a column for a habit with no roster row — a column without a frequency has no denominator.
- Retention: keep 24 months. Deleting an old file and deleting its `## Boxes` line are one act.

## reviews/

One file per year at `~/Clawic/data/habits/reviews/<year>.md`, append-only. Every cadence in `review.md` writes here; three months of these entries are what make a quarterly audit possible without recomputing anything.

```markdown
# Reviews — 2026

## 2026-07-19 — weekly
gym 9/11 (82%, working) · read 24/28 (86%, working) · vaping 14 clean days since the 04 Jul lapse
Shape: gym misses both on Fridays — sixth sample, acting on it.
Change: Friday gym drops to a 10-minute version. One change only.
Slot: none free; next addition possible 2026-07-25.

## 2026-07-01 — monthly rollup
June closed: gym 10/13, read 26/30, vaping 10/11 clean since the 20 Jun quit date. Better than May on gym and read.
Best streak updated: gym 9 weeks, ended 2026-06-14. Freeze budget reset.
```

## artifacts/

One file per thing, at `~/Clawic/data/habits/artifacts/<kebab-name>.md`, created the first time it exists. Canonical names here: `routine-<name>.md` · `quit-<thing>.md` · `restart-<habit>.md` · `contract-<habit>.md` · `audit-<year>-q<n>.md`. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Morning routine
*Read when the morning routine is discussed, rebuilt, or has lapsed. Written 2026-05-11.*

Anchor: feet on the floor.
1. Water, 1 glass — 30s
2. Kit on — 2 min
3. Walk, 10 min minimum
Total 13 min. Bad-day version: links 1 and 2 only.
Removed 2026-06-02: journaling as link 4 — it broke the chain twice, both times on work days.
```

```markdown
# Quit plan — vaping
*Read before any conversation about vaping, and immediately after a lapse. 2026-06-20.*

Mode: abstinence. Quit date: 2026-06-20. Escalation trigger: three lapses in one week → clinician.
Triggers, ranked: 1 after coffee · 2 bar after the second drink · 3 phone calls at work.
Substitutions: 1 → walk the block. 2 → sparkling water in the same hand.
Friction: none kept at home or in the car. Knows: Marta, brother.
Lapses: 2026-07-04 (bar, trigger 2). Trigger list updated, not restarted.
```

Update an artifact in place — a second quit plan for the same target loses the first attempt's trigger list, which is the most valuable thing in the file.

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that names people — the user may have none of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Marta Ruiz | marta@example.com | gym partner | whatsapp | Trains Tue/Thu; accountability since 2026-03 | 2026-07-19 | — |
```

- **Identity is `Key`**: lowercase email, else the handle, else `<kebab-name>` with a stable disambiguator. It is always written into the row, never left implicit — `Preferred channel` is a channel type, not an address, and cannot serve as a key.
- **Read the file before adding.** If the key is already there, update that row in place. Never append a second row for the same person, and never rewrite a row this skill did not create.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Scale cut**: one row per person while there are ≤15. Past that, or as soon as one person does not fit in a row, one file per person at `~/Clawic/data/contacts/<name>.md` with `contacts.md` as the index carrying the `File` pointer. If the folder already looks like that on arrival, follow it.
- **Removal is part of the box.** When an arrangement ends, delete the row this skill added and note the date in `memory.md`.
- In the habits roster, keep **only the person's name**. Duplicating the contact here is how two skills end up contradicting each other.

## Shared health box

Lives at `~/Clawic/data/health/` and holds the user's own body numbers, never a third party's. A habit log records whether the behavior happened; the number goes here.

```markdown
# Health profile

## Conditions
Asthma, exercise-induced. Inhaler before training.

## Metrics
- Weight (22 entries) → `weight.md`; read before any body-composition question
| Metric | Value | Date |
|--------|-------|------|
| Resting heart rate | 58 bpm | 2026-07-14 |
```

- **Identity is metric + date.** Stable facts (conditions, allergies, medication) live in `profile.md`; a metric measured in series moves to `~/Clawic/data/health/<metric>.md` once it passes ~15 entries, and `profile.md` keeps its index line.
- **The unit lives inside the value** (`74.2 kg`, `58 bpm`), because the next skill to read this file may not share the user's locale.
- Foreign columns win, same as above. Never rewrite a header this skill did not write.
- Never copy a body number into a habit log or a roster row. A weight series inside a habit grid breaks the rate math and hides the number where nothing else will find it.

## Shared finances box

Lives at `~/Clawic/data/finances/subscriptions.md`. Anything with a recurring charge attached to a habit — a gym, a tracker app, a class pass, a paid accountability service — is a subscription, not a habit note.

```markdown
# Subscriptions

| Name | Amount | Cycle | Started | Notes |
|------|--------|-------|---------|-------|
| Climbing gym | 49 EUR | monthly | 2026-03-02 | habits: gym |
```

- **Identity is `Name`.** Read before adding; update in place if it is there.
- **The currency lives inside the value** (`49 EUR`, not `€49`), because rows here come from several skills and someone will add the column up.
- **Cancelling deletes the row** and notes the date in `memory.md`. This table is not split — it stays small precisely because removal is part of it.
- Foreign columns win. Never rewrite the header.
- A one-off forfeit is not a subscription: it belongs in the commitment contract artifact, with the payment reference as a pointer, never a card number.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`roster.md` — `## Habits` and `## Retired`, moved together. They split as a pair because the quarterly audit reads both, and `## Retired` is the half that grows.

`patterns.md` — `## Patterns`, once a person has been tracked long enough for the table to pass ~15 rows.

`what-works.md` — `## What Works`. This is usually the last to split and the most valuable when it does: it is the record of every intervention already tried on this person, and it is what makes the third habit easier to design than the first.
