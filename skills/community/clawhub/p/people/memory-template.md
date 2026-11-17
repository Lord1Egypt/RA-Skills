# Working File Templates — Contacts

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md`, the address book, and everything they index is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/people/config.yaml` | Key by key, read-modify-write |
| A person: identity key, role, channel, one line of context, last contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's people in one address book |
| A person with more than a row's worth: details, dates, interaction log | `~/Clawic/data/contacts/<name>.md` (**shared**) | Own file from the second logged interaction or the seventh detail |
| Roster shape, groups, open loops, upcoming dates, how the user works, box index | `~/Clawic/data/people/memory.md` | Rewritten in place; stays small |
| The date-ordered view of birthdays and anniversaries | `## Dates` in `memory.md`, then `~/Clawic/data/people/date-index.md` | The same six-column table in both places from the first entry; splits at the threshold below |
| Promises, favors and introductions still open, in both directions | `## Open Loops` in `memory.md`, then `~/Clawic/data/people/open-loops.md` | One line per loop, closed lines deleted |
| Households, friend groups, teams, and who knows whom | `## Groups` in `memory.md`, then `~/Clawic/data/people/groups.md` | One block per group |
| Anyone who must never be surfaced: died, estranged, breakup, asked not to be contacted | `~/Clawic/data/people/do-not-surface.md` | Own file from the first entry |
| Candidates from a bulk import, not yet real contacts | `~/Clawic/data/people/candidates.md` | Append on import, rows leave when promoted |
| Things you produced that get re-read — forwardable intro blurbs, a message that landed, event debriefs, guest lists, a group map, an import mapping | `~/Clawic/data/people/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/people/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials, codes, passwords of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A person was met, or named for the first time with context | Their row in `contacts.md` |
| A detail passed the thirty-second filter | Their row's context, or their file once they have one |
| Any real interaction — met, called, texted, emailed back and forth | `Last contact`, plus a log line in their file if they have one |
| A birthday, anniversary, or the date of a loss was learned | The person's record **and** its row in `## Dates` |
| A life event happened: job, birth, illness, move, bereavement, breakup | Their record, and the follow-up date as a row in `## Dates` if the event has one |
| A promise, favor, or introduction was made, accepted, or chased | `## Open Loops` with a name and a date |
| An introduction landed, or died | Close the loop; keep the blurb in `artifacts/` if it is reusable |
| A tier or a per-person cadence was decided | The person's record |
| Two records were merged, a name changed, an address bounced | The surviving record, and the merge note in `## Roster Shape` |
| An import ran | `candidates.md`, and the mapping in `artifacts/` if it took thought |
| Someone died, went estranged, or asked not to be contacted | `do-not-surface.md`, in the same turn, before anything else |
| A group, household, or who-knows-whom edge became relevant | `## Groups` |
| The user declared a preference | Its key in `config.yaml` |
| The roster review or the overdue sweep ran | `## Due` |

## Start flat, split only when it hurts

Everything except the address book, artifacts, the suppression list and the candidate list begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/people/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings **and the table columns** identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Dates` becomes `date-index.md` with the same six columns it already had; `## Open Loops` becomes `open-loops.md`; `## Groups` becomes `groups.md`. A section that would have to be reshaped on the way out was written in the wrong shape on day one.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

The address book has its own cut, described below. Artifacts are the other exception: a blurb, a debrief or a guest list is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`1password:Personal/Alarm-code` · `bitwarden:Home/Wifi` · `keychain:carddav` · `env:CONTACTS_EXPORT_TOKEN` · `file:~/.config/carddav/creds` · `vault:shared/house`

When the user pastes something to save — a message thread, an exported record, a note about a house-sit — replace each secret value before writing and leave the pointer visible: `alarm: <1password:Personal/Alarm-code>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: names, preferred names and pronunciation, email addresses, phone numbers, social handles, employer and job title, city, birthday and other dates, family member names, interests, dietary needs, preferred channel, how you met. **Secrets, strip them**: door and gate codes, alarm codes and duress codes, wifi passwords, where a spare key is kept, shared account logins and streaming passwords, account recovery answers, national ID and passport numbers, full card numbers and bank account numbers, any API token or cookie used to export an address book.

Two things sit between the lists and are governed by `sensitive_details`, not by the secret rule: a **home address** — record it only when the user needs it for something concrete, never harvested — and any **health, legal, financial, or relationship detail about a third party**, where `minimal` records that the topic exists and `full` records the content (`privacy.md`).

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared address book](#shared-address-book) · [person file](#person-file) · [do-not-surface.md](#do-not-surfacemd) · [candidates.md](#candidatesmd) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/people/` if it does not exist.

```yaml
nudge_style: on-ask
reconnect_months: 6
birthday_lead_days: 5
brief_lines: 5
sensitive_details: minimal
roster_review: quarter
name_order: as-given

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  tags: [work, family, neighbor, climbing, madrid]
  log_max_lines: 2
relationship_model:
  tiers: {inner: 8w, regular: 6mo, orbit: none}
cadence:
  sweep_day: sunday
  quiet_until: 2026-09-01     # no nudges raised before this date
safety_posture:
  never_record: [politics, religion]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Contacts Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Address book (41 people) → `~/Clawic/data/contacts/contacts.md`; read before adding anyone or answering who-do-I-know
- Never surface (3) → `do-not-surface.md`; read before naming anyone to contact, congratulate or be reminded of
- Intro blurb for Maria → `artifacts/blurb-maria-garcia.md`; read when introducing her to anyone
- Berlin conference debrief → `artifacts/debrief-berlin-2026.md`; read before the next edition or before contacting anyone met there

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Overdue sweep | week, Sunday | 2026-07-19 | 2026-07-26 |
| Roster review (bounces, stale, untiered) | quarter | 2026-04-05 | 2026-07-05 |
| Annual date scan for the next 12 months | year | 2026-01-03 | 2027-01-03 |

## Dates
| MM-DD | Who | What | Year | Lead | Notes |
|-------|-----|------|------|------|-------|
| 01-19 | Maria Garcia | father's death | 2025 | 1d | she marks it; short message only |
| 03-14 | Maria Garcia | birthday | 1987 | 5d | turns 40 in 2027 — flag 3 weeks ahead |
| 09-02 | Tom Reeves | work anniversary | 2019 | 2d | — |
| 11-08 | Pablo Garcia | birthday (Maria's son) | 2022 | 5d | via Maria |

## Roster Shape
41 people: 6 inner, 14 regular, 19 orbit, 2 dormant. 7 still untiered.
2026-07-12: merged duplicate rows for Tom Reeves (personal + work email); work email kept as key.

## Open Loops
| Who | What | Direction | Since | By |
|-----|------|-----------|-------|----|
| Maria Garcia | intro to Luis Ferrer, double opt-in sent to Luis | I owe | 2026-07-14 | 2026-07-28 |
| Tom Reeves | said he'd send the contract template | owed to me | 2026-06-30 | chase 2026-08-01 |
| Ana Ruiz | book recommendation she asked for | I owe | 2026-07-20 | 2026-07-27 |

## Groups
**Climbing Tuesdays** — Luis, Ana, Tom's partner Sara. Meets weekly; Ana does not know Tom.
**Garcia household** — Maria, partner Diego, kids Sofia (2019) and Pablo (2022), dog Nube.

## How They Work
Writes in Spanish and English, prefers voice notes to calls. Hates being reminded twice. Will not use tiers by name — set `cadence` per person instead.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line, subject to `nudge_style`. Every recurring thing this skill schedules belongs here — never individual birthdays, which live in `## Dates`.
- **`## Dates`**: the six-column table shown above from the very first entry — `| MM-DD | Who | What | Year | Lead | Notes |` — ordered by `MM-DD` so the next four weeks read at a glance. It is written in that shape on day one precisely so the split into `date-index.md` is a copy-paste. `Year` empty means the year is unknown, which is a fact, not a gap; `Lead` overrides `birthday_lead_days` for that one date (`dates.md`). The authority for a date is the person's record in the address book; this table is the ordered index over it, and if the two disagree the record wins and the index row is corrected.
- **`## Open Loops`**: a loop is closed by **deleting its row**, not by marking it done — a list of completed favors is not a list anyone reads. `Direction` is `I owe` or `owed to me` and nothing else; running totals are not kept (SKILL.md Traps).
- **`## Roster Shape`**: counts per tier plus the merges and renames, so the next session knows the address book has been curated and does not redo it. Keep the merge notes; they are what stops a merged duplicate from being re-created on the next import.
- These headings **and these columns** are exactly the ones the split-out files get, so a split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Roster still being built; untiered people remain |
| `complete` | Everyone tiered, dates known for the inner and regular tiers |

## Shared address book

Lives at `~/Clawic/data/contacts/` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Maria Garcia | maria@acme.com | product lead, Acme | whatsapp | met at Berlin conf 2024 via Luis; two kids; climbing | 2026-07-14 | maria-garcia.md |
| Tom Reeves | tom.reeves@example.com | freelance lawyer | email | neighbour until 2023; contract help | 2026-06-30 | — |
| Ana Ruiz | @anaruiz | illustrator, freelance | signal | climbing Tuesdays since 2025; no email, signal only | 2026-07-20 | — |
```

- **`Key` is the identity, and every row carries it.** The email lowercased; with no email, the primary handle as the user would type it (`@anaruiz`); with neither, `<kebab-name>` plus a stable disambiguator (`john-smith-acme`). It is a column, not a convention: a key held only in the person file — which does not exist until their second interaction — leaves every one-row person undedupable, and deduplication is the reason this box is shared. `Preferred channel` is the channel type, never the address, so it is never the key. Read the file and match on `Key` before adding. If that key is already there, update the row in place — never a second row for the same person, and never touch a row another skill wrote.
- **Foreign columns win.** If `contacts.md` already exists with a different column set — another skill created it — write into its columns as they are. Never rename, reorder, or drop a column, and never touch the cells of a row this skill did not write. The only permitted change to a header written by someone else is **appending** `Key`, `Last contact` and `File` at the end when they are absent — nothing can be deduplicated without the first, the overdue sweep cannot run without the second, and person files cannot be found without the third. Rows from other skills get an empty cell in the appended columns and are left alone; if a foreign header already carries the identity under another name (`Email`, `Contact`, `ID`), that column is the key and no `Key` column is added. Anything else that does not fit goes into the person's own file.
- **`Context` is one line, and it is the reconnection material**: how you met, plus the one thing that makes them them. Not a biography — that is the person file.
- **`Last contact` is a date, `YYYY-MM-DD`**, updated by any real interaction (SKILL.md Rule 4). An empty `Last contact` means never contacted since the record was made, which is different from unknown; write `unknown` when it is unknown.
- **Scale cut**: one row per person while there are ≤15 and their detail fits one line. Past 15 people, or the moment one person needs more, that person gets `~/Clawic/data/contacts/<name>.md` and their row keeps the `File` pointer; `contacts.md` stays the index for everyone. If you arrive and the folder already looks like that, follow it — do not start a parallel file.
- **Removal is part of the address book.** A person who drifts moves to `dormant` in their record and stays. A person the user asks to remove is deleted from `contacts.md` and their file, and the deletion is noted with its date in `## Roster Shape` — that note carries no personal detail, only that a removal happened, so the next import does not resurrect them.
- **Death and estrangement do not delete anyone.** The record stays; the name goes on `do-not-surface.md`.
- Never write a credential, code, or password into any of these files.

## Person file

`~/Clawic/data/contacts/<kebab-name>.md`, created on the second logged interaction or the seventh detail — whichever comes first.

```markdown
# Maria Garcia
key: maria@acme.com · tier: regular · cadence: 4mo · channel: whatsapp (voice notes, not calls)
role: product lead at Acme, Berlin · met: Berlin conf 2024, introduced by Luis Ferrer
name: says MAH-ree-a, not muh-REE-a; signs mail "Mar"

## Dates
- 1987-03-14 birthday
- 2019-06-02 Sofia born · 2022-11-08 Pablo born
- 2025-01-19 her father died — she marks it

## Details
- Partner Diego (architect), kids Sofia and Pablo, dog Nube
- Climbing, badly and enthusiastically; wants to do Kalymnos
- No alcohol since 2024, does not make a thing of it
- Do not raise: the Acme reorg, she was on the wrong side of it

## Log
- 2026-07-14 lunch — leaving Acme in September, has not told her team. Asked what I thought about going independent.
- 2026-04-02 call — Sofia started school; father's anniversary was hard.

## Open with them
The independence decision, before anything else.
```

- Headings are fixed: `## Dates`, `## Details`, `## Log`, `## Open with them`. Omit any that is empty rather than leaving it blank. `## Dates` here is the **authority** and is a bullet list of that one person's dates; the six-column table in `memory.md` is the ordered index across everybody — same name, two roles, and the record wins when they disagree.
- `## Log` is **reverse chronological**, one to two lines per entry: the date, the one thing that changed, and the next step if there is one. It is the only section that grows without limit; past ~40 entries, move everything older than two years to the bottom under `## Earlier` and compress it to one line per year.
- `## Open with them` is a single line that the pre-meeting brief reads first. Rewrite it, never append.
- Secondhand facts carry their source and date: `heard from Luis, 2026-05: looking to move back to Madrid`.

## do-not-surface.md

`~/Clawic/data/people/do-not-surface.md`, created the first time anyone belongs on it. Read before naming anyone to contact, congratulate, or be reminded of.

```markdown
# Never surface

| Name | Reason | Since | If the user raises them |
|------|--------|-------|-------------------------|
| Peter Hall | died | 2025-11-02 | follow their lead; the anniversary is in `## Dates` only if they asked for it |
| Clara Boyd | estranged, no contact | 2024-08 | do not suggest reaching out; answer factually if asked |
| Nils Berg | asked not to be contacted | 2026-03-11 | never propose contact, in any form |
```

`Reason` is one of `died`, `estranged`, `breakup`, `asked not to be contacted`, `professional block` — the handling differs and the word is what tells you which (SKILL.md Rule 7). Entries are never removed on a guess; only the user takes a name off this list.

## candidates.md

`~/Clawic/data/people/candidates.md`, created by an import. Rows here are not contacts and are never counted, swept, briefed, or nudged.

```markdown
# Import candidates

Source: LinkedIn export, 2026-07. 812 rows, 41 kept below.

| Name | Handle or email | Where from | Promote when |
|------|-----------------|------------|--------------|
| Ines Roca | ines@studio.example | LinkedIn 2026-07, worked together 2021 | she comes up in conversation, or we speak again |
```

A candidate is promoted by writing their row into `contacts.md` and deleting it here. Rows never promoted are deleted at the roster review — an import that stays forever is a second address book.

## artifacts/

One file per thing, at `~/Clawic/data/people/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **forwardable intro blurb**, **a hard message that landed** (condolence, reconnection, apology) kept as a pattern rather than to be reused verbatim, **event debrief** (who was met at a conference, wedding, or offsite, and what to do about each), **guest list with its constraints**, **group or family map**, **import mapping**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Intro blurb — Maria Garcia
*Read when introducing her to anyone. Written 2026-07-26, approved by her.*

Two sentences, forwardable as-is, no private detail...
```

```markdown
# Debrief — Berlin conference 2026
*Read before the next edition, and before contacting anyone met there. 2026-06-14.*

| Person | Why they matter | Next step | Done |
|--------|-----------------|-----------|------|
| Ines Roca | runs the design studio Luis mentioned | send the article, week of 06-22 | yes, 06-21 |

Rows for people worth keeping become rows in `contacts.md` in the same turn; this file keeps only the event context.
```

A blurb about a person is written as if they will read it, because they will: an intro blurb is forwarded to its subject by default (`introductions.md`).

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings and the exact columns it had inside `memory.md`.

`date-index.md` — the `## Dates` table, columns and ordering unchanged, under the heading `# Dates`. Nothing about a row changes on the way out; only its file does.

`open-loops.md` — the `## Open Loops` table, unchanged. Its existence usually means the user is the connector in their group; the roster review checks for loops older than 60 days, which are either chased or dropped explicitly.

`groups.md` — one block per group, headings unchanged, plus a `who does not know whom` line per group where it matters for invitations and introductions.
