# Working File Templates — Meetings

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/meetings/config.yaml` | Key by key, read-modify-write |
| Standing series, open action items, meeting norms, pain points, due dates, box index | `~/Clawic/data/meetings/memory.md` | Rewritten in place; stays small |
| What happened in a meeting — attendees, decisions, actions, open questions | `~/Clawic/data/meetings/records/<year>-<mm>.md` (or `record_location`) | Append-only, one block per meeting, cut by month |
| Decisions, with who decided, by which method, and what was rejected | `~/Clawic/data/meetings/decisions.md` | One row per decision; grep-able forever |
| Open action items and what you are waiting on | `## Follow-Ups` in `memory.md`; `~/Clawic/data/meetings/follow-ups.md` once it outgrows the section | One row per item; closed items move to that month's record |
| Standing meetings: cadence, purpose, owner, expiry date | `## Series` in `memory.md`; `~/Clawic/data/meetings/series.md` from ~15 series | One row per series |
| People who attend meetings — role, channel, context, last contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill writing into one address book |
| Work the user tracks as a project — the decision summary and the milestone | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, referenced from the record by name |
| Things you produced that get re-read — an agenda that worked, a series charter, a recurring prep brief, formal minutes, a workshop plan, a facilitation script, a retro format | `~/Clawic/data/meetings/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Raw transcripts, only when the user asks to keep the raw text | `~/Clawic/data/meetings/transcripts/<date>-<kebab-topic>.md` | One file per transcript; the record is written from it and stands alone |
| **Anything durable this table does not name** | `~/Clawic/data/meetings/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind, and anything marked off the record | Nowhere under `~/Clawic/data/` | Pointer only, or nothing at all — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, a company, a booking? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — an agenda template, a charter, a set of minutes, a workshop plan? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A meeting took place, or the user described one that did | A block in `records/<year>-<mm>.md` |
| A decision was made | A row in `decisions.md`, and the same decision inside the meeting's record block |
| A decision belongs to a tracked project | One-line summary in `~/Clawic/data/projects/<project>.md`, full entry stays in `decisions.md` |
| An action item was agreed | A row in `## Follow-Ups` with owner, date and definition of done |
| An action item closed, slipped, or was escalated | The same row — closed items move into that month's record, slipped ones get the new date and the reason |
| A standing meeting was created, re-scoped, rescheduled, or killed | `## Series`, with its expiry date (SKILL.md Rule 7) |
| An attendee appeared for the first time, or their role, channel or context changed | Their row in `contacts.md` (shared) |
| Something was learned about how a person or a room behaves in meetings — who decides, who blocks, who needs the pre-read | The person's `Context` in `contacts.md`; if it no longer fits the row, their own contact file |
| A norm or constraint about how this org meets came out — no-meeting day, timezone spread, a room that always overruns, a client who never reads pre-reads | `## Meeting Norms` |
| A meeting failed in a way worth not repeating | `## Pain Points`; a second occurrence earns a facilitation script or charter in `artifacts/` |
| An agenda, charter, prep brief, set of minutes, workshop plan or retro format is worth reusing | `artifacts/` |
| The user asked to keep a raw transcript | `transcripts/`, and the structured record in the same turn |
| A sweep, kill review, load audit or cadence check was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except records, decisions, artifacts, transcripts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/meetings/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Records, decisions, artifacts and transcripts are the exception: each is born in its own file whatever its size, because it is read whole and only when its subject comes up. `records/` cuts by month; if a single month passes ~60 meeting blocks, cut it into `records/<year>-<mm>-a.md` and `-b.md` by fortnight and leave nothing behind. `decisions.md` stays one grep-able file until ~150 rows, then splits into `decisions/<year>.md` with `decisions.md` kept as the index (`Date | Decision | → file`).

## If an older layout is already there

Earlier versions of this skill created `upcoming/`, `past/`, `recurring/`, `people/` and `follow-ups.md`. Fold them in the first time you write, then delete the empty folders:

| Found | Goes to |
|---|---|
| `past/**` and any dated meeting note | `records/<year>-<mm>.md`, one block per meeting, keeping the original date |
| `upcoming/*` for a one-off meeting | Nothing — a prep brief for a meeting that has happened is dead weight |
| `upcoming/*` for a recurring meeting | `artifacts/prep-<series>.md`, updated in place each occurrence |
| `recurring/*` | A row in `## Series`; its running notes become record blocks |
| `people/*` | The person's row in `~/Clawic/data/contacts/contacts.md`, or their own contact file if it does not fit |
| `follow-ups.md` at the workspace root | `## Follow-Ups` in `memory.md`, open items only |

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted invite, transcript or calendar export is a dense source: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`keychain:board-zoom-passcode` · `1password:Work/Zoom/board` · `bitwarden:Team/Standup` · `env:CALENDAR_ICS_URL` · `file:~/.config/meetings/ics-url` · `vault:secret/team/dial-in`

In a text, the pointer goes where the value was: `Dial-in PIN: <keychain:board-dial-in>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: names, roles, titles, company names, meeting titles and series names, dates, times and timezones, room names, agenda items, decisions and their reasoning, action items, project names, public join URLs with no embedded passcode, the *existence* of a recording.

**Secrets, strip them**: join links with an embedded passcode or token, dial-in PINs, meeting passwords, webinar registration tokens, secret ICS or calendar-sharing URLs, API keys or passwords read out in the room, personal phone numbers the user did not choose to store.

**Off the record is a third category, and it outranks both.** Compensation figures, performance ratings, health details, legal advice, unannounced personnel changes, and anything the user flags as off the record are not written to disk at all — not redacted, not summarized with the number removed unless the user asks. Write the decision that resulted ("comp review completed for the team") and nothing else. If a record already holds such content, delete the line and say so in one line.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [records/](#records) · [decisions.md](#decisionsmd) · [artifacts/](#artifacts) · [transcripts/](#transcripts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/meetings/` if it does not exist.

```yaml
default_role: chair
meeting_length_default: 25-50
decision_method: daci
cost_per_attendee_hour: 90 EUR
record_location: ~/Clawic/data/meetings/records/
record_style: decisions-first
recap_policy: when-decisions
recording_consent: announce
follow_up_sweep_day: Friday
series_review_days: 90

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  invite_title: "<output> — <series or project>"
  action_syntax: "owner — verb + object — date"
platform:
  timezone: Europe/Madrid
  working_hours: "09:00-18:00"
  no_meeting_block: "Wednesday mornings"
confidentiality:
  never_stored: [comp review, board exec session]
cadence:
  load_audit: monthly
  skip_level: quarterly
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Meetings Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Meeting records (2026-07, 14 meetings) → `records/2026-07.md`; read before any meeting with the same people or series
- Decision log (31) → `decisions.md`; read before reopening anything, and before any decision meeting
- Standing series (17) → `series.md`; read when scheduling, killing or auditing a recurring meeting
- Board pack minutes Q2 → `artifacts/minutes-board-2026-q2.md`; read before the next board meeting
- Weekly leads charter → `artifacts/charter-weekly-leads.md`; read before changing that meeting's shape
- Retro format that stuck → `artifacts/retro-format-team-a.md`; read when facilitating a retro

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Follow-up sweep | week, Friday | 2026-07-24 | 2026-07-31 |
| Meeting-load audit | month | 2026-07-01 | 2026-08-01 |
| Series kill review | quarter | 2026-04-14 | 2026-07-14 |
| Skip-level round | quarter | 2026-05-20 | 2026-08-20 |

## Follow-Ups
### Open
| Item | Owner | Due | Done means | From |
|---|---|---|---|---|
| Vendor comparison for the CDN swap | Priya | 2026-07-30 | Table in the channel, three options with prices | 2026-07-23 platform sync |
| Send Acme the revised timeline | me | 2026-07-28 | Email sent, dates agreed in writing | 2026-07-21 Acme status |

### Waiting On
| What | Who | Asked | Chased | Next step |
|---|---|---|---|---|
| Legal sign-off on the DPA | Marc (legal) | 2026-07-15 | 2026-07-22 | 2026-07-29 name the launch-date impact |

## Series
| Series | Cadence | Owner | Purpose type | Attendees | Expires | Last held |
|---|---|---|---|---|---|---|
| Platform sync | weekly Tue 25m | me | align | 6 | 2026-10-01 | 2026-07-23 |
| Acme status | biweekly Wed 25m | me | align | 4 | 2026-09-15 | 2026-07-21 |
| 1-on-1 Priya | weekly Mon 30m | me | build trust | 2 | — | 2026-07-20 |

## Meeting Norms
No-meeting Wednesday mornings, respected by everyone except the sales team.
Timezone spread 9h (Madrid ↔ SF): the 17:00 CET slot is the only overlap; it rotates monthly.
Board never reads the pre-read; the first 15 minutes are a silent read, and it works.
Standup is async in a thread on Mondays and Fridays, live on the other days.

## Pain Points
2026-05: three decisions reopened in one month because recaps went only to attendees. Distribution now includes the whole affected group.
2026-06: retro produced 9 actions, 1 shipped. Now capped at 3 owned experiments.

## How They Work
Chairs most meetings. Wants the agenda and the recap drafted, not coaching. Will cut a meeting rather than shorten it. Hates being asked what the meeting is for — infer it from the title and the attendees, then state the assumption.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, and the cadences come from `cadence` in `config.yaml` when the user has declared them.
- **`## Follow-Ups`**: **open items only**. `Done means` is what makes the item closeable by someone other than its author. When an item closes, delete the row and record the closure in that month's record block — a ledger that keeps its history stops being a to-do list. `Waiting On` is for things owed *to* the user; the `Next step` column is what the escalation ladder does next (`follow-through.md`).
- **`## Series`**: `Expires` is a date, never blank for a group meeting — a series with no expiry is one nobody will ever cancel (SKILL.md Rule 7). 1-on-1s are exempt and carry `—`. `Last held` is what exposes a series that quietly died.
- **`## Meeting Norms`**: facts about how this org meets that changed a decision, one line each. This is the section that stops the same timezone, pre-read or no-meeting-block problem from being rediscovered every quarter.
- **These headings are exactly the ones `follow-ups.md` and `series.md` get** when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their meetings, people and norms |
| `complete` | Know the series, the decision rights and the room |

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every skill that touches people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Priya Raman | priya@acme.com | VP Product, Acme | email | Decides on scope; wants numbers before an opinion | 2026-07-23 | — |
| Marc Oliver | marc.oliver@acme.com | Counsel, Acme | slack | Never attends live; answers in writing within 48h | 2026-07-22 | `contacts/marc-oliver.md` |
```

- **Identity is `Key`**: lowercase email; if there is none, the handle; if there is neither, `<kebab-name>` plus a stable disambiguator (`john-smith-acme`). The key is a **column of the row**, never implicit — `Preferred channel` is the kind of channel, not the address, so it can never serve as the key.
- **Read the file before adding.** If the key is already there, update the row in place — never a second row for the same person. Only absence justifies a new row.
- **You update and retire your own rows and never touch another skill's.** When a person is no longer a contact, delete the row and note the date in `## Meeting Norms`; an address book that only grows stops being one.
- **Meeting-shaped context goes in `Context`, one clause**: how they decide, what they need before deciding, whether they read pre-reads, whether they speak in the room or afterwards. The moment it no longer fits the cell, create `~/Clawic/data/contacts/<kebab-name>.md`, move the context there under a `## Meetings` heading, and put the path in the `File` column.
- **`Last contact` is the date of the last meeting or exchange**, updated after every meeting they attended. It is what answers "who have I not spoken to in months".
- **Scale cut**: one row per person while there are ≤15, or until one no longer fits its row. Past that, one file per person at `~/Clawic/data/contacts/<kebab-name>.md` with the same fields, and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never a personal phone number the user did not choose to store, and never a credential.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, shared with every skill that tracks work.

- **Identity is the file name**, the project name in kebab-case (`acme-migration.md`). Read the folder before creating: if a file for that project is already there under any spelling, write into it — never a second file for the same work.
- The **decision summary** of a meeting about that project belongs there in one line, dated: the full entry with its rejected options stays in `~/Clawic/data/meetings/decisions.md` here, referenced by date.
- The project is named in the meeting record; the record never copies the project's status, milestones or scope. Duplicating them is how two skills come to disagree about where the project stands.
- Closing a project is `status: done | cancelled — <date>` inside its file, never deleting the file: it is the record of what was delivered.
- **Scale cut**: past ~20 closed projects, move the closed ones to `~/Clawic/data/projects/archive/<project>.md` **without renaming the file**, so any pointer written by another skill still resolves. Open projects never move.
- **Foreign layout wins.** If the folder already exists with another shape — one file per project with front-matter, a single `projects.md` index, subfolders per client — follow it and append your line in its idiom. Never rewrite another skill's structure or headings; add a `## Meetings` heading inside the existing file instead.
- If the file does not exist and the work is genuinely a tracked project, create it with the project name as an H1 and the one-line decision; do not invent a status.

## records/

One file per month at `~/Clawic/data/meetings/records/<year>-<mm>.md` (or under `record_location`), append-only, newest block at the bottom. Shaped by `record_style`; this is `decisions-first`, the default.

```markdown
# Meeting Records — 2026-07

## 2026-07-23 · Platform sync · align · 25 min · 6 people
Attendees: me, Priya, Tomás, Lena, Sam, Aziz (Marc absent)

**Decisions**
- CDN stays on the current vendor until Q4. Decider: Priya (owner-decides after input). Logged in `decisions.md`.

**Actions**
- Priya — vendor comparison table in the channel — 2026-07-30 — three options with prices
- me — send Acme the revised timeline — 2026-07-28 — email sent, dates agreed in writing

**Open questions**
- Does the DPA block the EU rollout? → Marc, answer by 2026-07-29

**Context**
Latency regression is in the origin, not the CDN — that killed the swap argument for now.

**Recap sent**: 2026-07-23 to the platform channel plus the two absent leads.
```

- The header line is the index: `date · series or title · purpose type · length · attendee count`. It is what makes a month grep-able.
- **Attendees are names, and each one that is new or changed gets its `contacts.md` row in the same turn.** Absences are recorded — an absent decider explains a reversal two weeks later.
- Decisions appear both here and in `decisions.md`: here as the narrative, there as the searchable row. That is the one deliberate duplication in this skill, and the row is the authority.
- `full-notes` adds a `**Discussion**` section under Context; `verbatim` adds quoted lines with speaker attribution, and is for board, legal and client-commitment contexts only.
- No credential, and nothing marked off the record, ever reaches this file.

## decisions.md

The reason this skill has long-term value: a decision nobody can find gets made again.

```markdown
# Decision Log

| Date | Decision | Owner | Method | Rejected | Reversible | Revisit | Where |
|---|---|---|---|---|---|---|---|
| 2026-07-23 | CDN stays on the current vendor until Q4 | Priya | owner-decides | Vendor B (migration cost 3 weeks), self-hosted (no on-call) | yes | 2026-10-01 | `records/2026-07.md` |
| 2026-06-04 | Hiring freeze on the platform team | Ana | daci | Backfill only (rejected: budget) | no | — | `records/2026-06.md` |
```

- **`Rejected` is the column that stops relitigation.** A decision without its rejected options is an opinion with a date, and it gets reopened by the first person who thinks of option B.
- `Reversible` decides how hard to defend it: a reversible decision is reopened on any new argument, a one-way door only on new information.
- `Revisit` is a date or `—`. When a decision carries one, add a `## Due` row so it actually comes back.
- A decision that came with reasoning worth reading whole — a diagram, a cost model, a memo — gets an `artifacts/decision-<kebab>.md` and the `Where` column points at it.

## artifacts/

One file per thing, at `~/Clawic/data/meetings/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **an agenda that worked**, **a series charter**, **a prep brief for a recurring meeting**, **formal minutes**, **a workshop or offsite plan**, **a facilitation script for a hard conversation**, **a retro format**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Charter — Weekly Leads
*Read before changing this meeting's shape, and at every kill review. Written 2026-07-26.*

Purpose type: align. Output: one prioritized list of cross-team blockers with owners.
Owner: me. Attendees: 6 leads (decision ceiling 8). Cadence: weekly, 25 min, Tue 10:00 CET.
Timeboxes: blockers 12 · decisions 6 · close 5 (80% of 25 min = 20).
Not this meeting: status (async thread Monday), design debate (own session), 1-on-1 topics.
Expires 2026-10-01. Kill test: if fewer than two blockers arrive in three consecutive weeks, it becomes async.
```

```markdown
# Prep — Acme quarterly business review
*Read the day before every Acme QBR. Updated 2026-07-21.*

Their standing asks, our open commitments, the numbers they always challenge,
who actually decides on their side, and what we will not concede.
```

```markdown
# Minutes — Board, 2026 Q2
*Formal record. Read before the Q3 board meeting. Approved 2026-07-10.*

Date, time, venue, attendance and quorum · items in order with proposer and outcome ·
resolutions in full wording, with votes for/against/abstained · time of close · next meeting.
```

If the work belongs to a tracked project, the one-line summary also goes to `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## transcripts/

Only when the user explicitly asks to keep the raw text: `~/Clawic/data/meetings/transcripts/<date>-<kebab-topic>.md`. The structured record is written in the same turn and must stand alone — a transcript is raw material, never the record.

- Strip credentials before writing (Secrets above), and drop anything marked off the record entirely.
- Its `## Boxes` line carries a real condition: `read only if the record is disputed`. Nobody reads a transcript twice for pleasure.
- Default is not to keep it. Say in one line that the record was written and the transcript was not stored.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`follow-ups.md` — `## Open` and `## Waiting On`, identical columns. This is the file the weekly sweep reads end to end; the sweep is why it exists as one list instead of one list per meeting.

`series.md` — `## Series`, plus a `## Killed` table (series, date killed, what replaced it) once the first one dies. The killed list is what stops a cancelled meeting from being reinvented under a new name two quarters later.
