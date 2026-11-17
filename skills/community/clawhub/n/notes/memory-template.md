# Working File Templates — Notes

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/notes/config.yaml` | Key by key, read-modify-write |
| Corpus state: conventions settled, platform facts, note map, box index, due dates | `~/Clawic/data/notes/memory.md` | Rewritten in place; stays small |
| The notes themselves, one file per note | `~/Clawic/data/notes/<type>/<name>.md` — `meetings/`, `decisions/`, `journal/`, `projects/`, `research/`, `quick/` | Born as its own file from the first note of that type; the folder is created with that note, never before |
| Action items, open and recently closed | `~/Clawic/data/notes/actions.md` | One table, from the first action item; a commitments question reads it without loading anything else |
| Tag, person and recency index over the corpus | `~/Clawic/data/notes/index.md` | Created at 30 notes (SKILL.md Rule 7), updated in the same turn a note is created |
| Weekly and monthly review output | `~/Clawic/data/notes/reviews/<year>.md` | Append-only, cut by year |
| A template the user reshaped | `~/Clawic/data/notes/templates/<type>.md` | One file per note type, created the first time the user changes its shape |
| Attendees, action owners, anyone named in a note | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill writing into one inventory |
| The project a note belongs to | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; the note keeps only the project name |
| Things you produced that get re-read whole — a taxonomy decision, a migration plan, an export map, a handover | `~/Clawic/data/notes/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/notes/<plural-noun>.md`, or `~/Clawic/data/notes/artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A note of any type was produced | Its file under `~/Clawic/data/notes/<type>/` |
| An action item was created, completed, rescheduled, or dropped | Its row in `actions.md` |
| A decision was made, or an older one superseded | `decisions/<date>_<slug>.md`, plus the `supersedes` line in both |
| Someone was named as an attendee or an owner | Their row in the shared `contacts.md` |
| A note belongs to a project | The project file in the shared `projects/`, and the project name in the note |
| A platform was routed, a vault path or database id was found, a folder or notebook was named | `config.yaml` for the declared choice; `## Platform Facts` for what you discovered |
| A naming, tagging, or folder convention got settled | `## Conventions` |
| A question was left open, or a thread is waiting on someone | `## Open Threads` |
| A weekly or monthly review ran | `reviews/<year>.md`, and the row in `## Due` |
| A recurring meeting was identified | `## Recurring Meetings` |
| The corpus passed 30 notes | Create `index.md` and its `## Boxes` line |
| A tag merge, archive run, or migration was executed | `artifacts/<kebab-name>.md` with what changed and how many files |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except notes, actions, reviews, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/notes/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Notes, reviews and artifacts are the exception: each is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not a note you create, not text the user pastes in and asks you to keep. Notes are the highest-risk domain for this: a dump written up after a call routinely carries the bridge PIN, the wifi password, and the key somebody read out loud. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:NOTION_API_KEY` · `keychain:bear-token` · `1password:Work/Notion/agent` · `bitwarden:Personal/Evernote` · `file:~/.config/notion/api_key` · `profile:work`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `token: <file:~/.config/notion/api_key>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: note titles and filenames, folder and notebook names, tag names, vault paths, Notion database and page ids, Bear note ids, attendee names and work email addresses, meeting dates, project names, CLI names, and the fact that a token exists together with where it lives. **Secrets, strip them**: Notion integration tokens (`ntn_…`, `secret_…`), Bear API tokens, Evernote auth tokens, any password or passphrase, meeting bridge PINs and host keys, MFA and recovery codes, private keys, connection strings carrying a password, card and national-ID numbers read out on a call, and anything pasted straight out of a `.env` file or a password manager.

Two things are not secrets but still may not belong in a note: another person's health, pay, or performance, and anything under an NDA that has no business in a searchable corpus. That is a decision, not a redaction — `sensitive.md` has it.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [actions.md](#actionsmd) · [note files](#note-files) · [index.md](#indexmd) · [templates/](#templates) · [reviews/](#reviews) · [artifacts/](#artifacts) · [shared contacts inventory](#shared-contacts-inventory) · [shared projects box](#shared-projects-box) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/notes/` if it does not exist.

```yaml
default_platform: obsidian
routing:
  meeting: obsidian
  decision: local
  journal: bear
  quick: apple-notes
  research: obsidian
vault_path: ~/Documents/Vault
notion_database_id: 1f2c9a...        # id only, never a token
filename_pattern: date-first
capture_verbosity: standard
tag_style: nested
review_cadence: weekly
review_day: fri
action_target: notes
archive_after_months: 12

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  frontmatter: [date, type, title, tags, attendees, project]
  links: wikilinks
  emoji_headings: false
safety_posture:
  network_platforms_confirm: true
  never_write: [salary, performance reviews, client X]
integrations:
  task_app: things
  citation_manager: zotero
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Notes Memory

## Status
status: ongoing
last: 2026-07-26
corpus: 64 notes (41 obsidian, 18 local, 5 bear)

## Boxes
- Action items (11 open) → `actions.md`; read before any commitment, deadline or "what do I owe" question
- Tag, person and recency index (64 notes) → `index.md`; read before searching, and update it in the same turn a note is created
- Weekly reviews (2026) → `reviews/2026.md`; read when comparing weeks or reconstructing what happened
- Tag taxonomy decision → `artifacts/tag-taxonomy.md`; read before creating a tag or merging two
- Notes → `meetings/`, `decisions/`, `journal/`, `projects/`, `research/`, `quick/`; open a file only when its subject comes up

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Weekly review | week, Friday | 2026-07-17 | 2026-07-24 |
| Inbox triage (quick/) | 7 days | 2026-07-22 | 2026-07-29 |
| Tag + orphan-link sweep | month | 2026-07-01 | 2026-08-01 |
| Backup restore test | quarter | 2026-04-12 | 2026-07-12 |
| Archive run (>12 months) | year | 2026-01-04 | 2027-01-04 |

## Note Map
Where each type lands today, and why it is not the default:
- meeting, research → Obsidian vault `~/Documents/Vault` (backlinks matter here)
- decision → local markdown (must survive leaving Obsidian)
- journal → Bear (captured from the phone)
- quick → Apple Notes inbox, triaged into local weekly

## Platform Facts
Facts that cost effort to find and would cost it again:
- Obsidian default vault is "Work"; a second vault "Personal" exists and is never written to
- Notion database "Notes" id 1f2c9a…, properties Name/Type/Date/Tags/Status
- Bear must be running before any `grizzly` call; token at `keychain:bear-token`

## Conventions
- Filenames `YYYY-MM-DD_topic-slug.md`; journal is `YYYY-MM-DD.md`
- Nested tags, two levels max: `#product/pricing`
- Attendees as `@first-last`, matching the key in contacts.md

## Recurring Meetings
| Meeting | Cadence | Attendees | Note home | Carry-forward |
|---|---|---|---|---|
| Product sync | weekly, Tue | @alice, @bob | meetings/ | open questions from last week |
| 1-on-1 with @alice | biweekly | @alice | meetings/ | her topics, both action lists |

## Open Threads
| Question | Waiting on | Since | Source note |
|---|---|---|---|
| Do we keep tier 3 pricing? | @bob | 2026-07-14 | `decisions/2026-07-14_pricing-tiers.md` |

## How They Work
Dictates after calls, never during. Wants the note back in under 10 lines with the actions on top.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file or folder that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the box is created. Never delete a line without deleting what it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Cadences come from `review_cadence`, `review_day` and `archive_after_months`; every recurring thing this skill schedules belongs here.
- **`## Status`**: `corpus` is the note count with the per-platform split, because it is what decides Rule 7 (index at 30) and it is expensive to recount. Update it whenever you create or archive notes.
- **`## Note Map`** records the routing that is *live*, including fallbacks that stuck; `config.yaml` records what the user *asked for*. When they disagree, the user's declaration wins and the discrepancy gets said out loud once.
- **`## Open Threads`** is the only place an unanswered question survives a note being closed. A thread whose answer lands becomes a line in the note it came from, and its row is deleted.
- These headings are exactly the ones the split-out files get, so a split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their apps, conventions and rhythm |
| `complete` | Routing, conventions and cadence are settled |

## actions.md

Created with the first action item, at `~/Clawic/data/notes/actions.md`. One table, sorted by due date ascending — sections by status go stale the moment a date passes; a sort does not.

```markdown
# Action Items

| Task | Owner | Due | Status | Source |
|---|---|---|---|---|
| Send the pricing deck | @alice | 2026-08-04 | open | `meetings/2026-07-26_product-sync.md` |
| Confirm the vendor SOC 2 | @me | 2026-08-06 | blocked: waiting on vendor | `notion:Vendor Review` |
| Draft the migration plan | @me | 2026-07-30 | done 2026-07-25 | `artifacts/migration-plan.md` |
```

- **Identity is `Task` + `Owner`.** Read the file before adding: an item restated in a later meeting updates the existing row (new due date, new source appended), never a second row.
- **`Due` is always an absolute date** (SKILL.md Rule 4). An item that genuinely has no date is not an action item — it is an `## Open Threads` row.
- **`Source` is a pointer**: a local path, `notion:Page`, `bear:#tag/Title`, `obsidian:[[Note]]`, `apple-notes:Title`, `evernote:Title`. It is what lets the user reopen the context that produced the commitment.
- **Owners are pointers too**: `@key` matching the `Key` column of the shared `contacts.md`. Never store the person's details here.
- **Closing is deleting, eventually.** `done <date>` stays in the table until the next weekly review, then moves to `reviews/<year>.md` under that week. A tracker that keeps every completed item stops being readable at about 80 rows.
- **Scale cut**: one table while open items are ≤60. Past that, split by owner into `~/Clawic/data/notes/actions/<owner>.md` with the same columns and leave `actions.md` as the index (`Owner | Open | Next due | → file`).
- With `action_target: external`, this file holds only the items the external app does not: one row per commitment made *by someone else to the user*, plus a pointer to where the user's own tasks live.

## Note files

One file per note, under the folder for its type. The folder is created with its first note and never in advance.

`meetings/2026-07-26_product-sync.md` · `decisions/2026-07-14_pricing-tiers.md` · `journal/2026-07-26.md` · `projects/2026-07-20_atlas-status.md` · `research/kahneman-noise.md` · `quick/2026-07-26_14-30_call-sarah.md`

Every note opens with frontmatter, because it is what makes the corpus queryable without an index:

```markdown
---
date: 2026-07-26
type: meeting
title: "Pricing: staying at three tiers, revisit at 500 customers"
tags: [product, pricing]
attendees: [alice, bob]
absent: [carol]
project: atlas
platform: local
supersedes: decisions/2026-05-02_pricing-tiers.md
---
```

- `title` states the claim, not the topic (SKILL.md Rule 2). The filename slug can be short; the title carries the answer.
- `platform` records where the canonical copy lives, including a fallback: `local (fallback from notion)`.
- `project` is the project name only — the project itself lives in the shared `projects/` box.
- `attendees` and `absent` use the same keys as `contacts.md`. Absentees matter: they are who the summary gets sent to.
- The body shape for each type is in the file that owns the situation — `meetings.md`, `decisions.md`, `journal.md`, `projects.md`, `research.md`, `capture.md`.

## index.md

Created when the corpus passes 30 notes, not before (SKILL.md Rule 7), and updated in the same turn any note is created, renamed, or archived.

```markdown
# Notes Index
*Covers 64 notes. Updated 2026-07-26.*

## Tags
| Tag | Notes | Most recent |
|---|---|---|
| product/pricing | 9 | 2026-07-26 |
| hiring | 4 | 2026-07-11 |

## People
| Person | Notes | Last appears |
|---|---|---|
| @alice | 21 | 2026-07-26 |

## Recent
| Date | Title | Type | File |
|---|---|---|---|
| 2026-07-26 | Pricing: staying at three tiers | meeting | `meetings/2026-07-26_product-sync.md` |
```

Keep `## Recent` to the last 20 rows; everything older is found by tag, person, or grep. An index that mirrors the whole corpus is a second corpus to maintain.

## templates/

One file per note type, created the first time the user reshapes that type: `~/Clawic/data/notes/templates/meeting.md`. A stored template overrides the shape in the reference file for that type, and the difference gets a one-line note at the top of the template ("no effectiveness score, actions first").

## reviews/

Append-only, cut by year. This is where completed action items go to stay countable.

```markdown
# Reviews — 2026

## Week of 2026-07-20
Completed: 6 · Carried over: 2 · Created: 9
- Shipped: pricing decision, vendor shortlist
- Carried: SOC 2 confirmation (blocked on vendor since 2026-07-18)
- Pattern: three meetings produced no decision and no action

## July 2026
Notes: 21 (14 meeting, 3 decision, 4 quick) · Untriaged at month end: 0 · Tags merged: 2
```

The value is the pattern line, not the counts: a month whose meetings produce no decisions is the finding the user will act on.

## artifacts/

One file per thing, at `~/Clawic/data/notes/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a taxonomy or folder-structure decision and its reasoning**, **a migration or export plan with the fidelity findings**, **a handover pack**, **a template library the user wrote**, **a bulk-operation record** (what a tag merge or archive run touched, and how many files). Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Tag taxonomy — two levels, twelve roots
*Read before creating a tag or merging two. Decided 2026-07-12.*

Decision: nested tags, two levels maximum, twelve roots listed below.
Rejected: flat tags — hit 47 tags in three months and search stopped discriminating.
Rule that follows: a tag over 10% of the corpus becomes a root; a tag used once is merged at the monthly sweep.
```

If the artifact belongs to a project, its summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the detail staying here and referenced by filename.

## Shared contacts inventory

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Alice Ruiz | alice@acme.com | Head of Product, Acme | email | owns pricing decisions | 2026-07-26 | — |
```

- **Identity is `Key`**: the lowercase email if there is one, else the handle they are known by, else `<kebab-name>` plus a stable disambiguator (`john-smith-acme`). The key is a column of the row, never implicit and never delegated to a per-person file. `Preferred channel` is the channel *type*, not an address, so it can never serve as the key.
- **Read the file before adding.** If the key is already there, update the row in place — `Last contact`, `Role`, `Context` — and never append a second row for the same person. Rows written by other skills are theirs: add to their `Context` only, never rewrite them.
- **Retirement**: when a person leaves the picture entirely, delete their row and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- **Scale cut**: one row per person while there are ≤15, or until one no longer fits on a line. Past that, `~/Clawic/data/contacts/<name>.md` per person with the same fields, and `contacts.md` becomes the index with the `File` pointer filled in. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never store a credential, a personal phone number the user did not ask you to keep, or anything from `sensitive.md`'s do-not-write list.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every skill that tracks work.

```markdown
# Atlas

status: active
owner: @me
started: 2026-05-02

## Decisions
- 2026-07-14 Pricing stays at three tiers — `notes/decisions/2026-07-14_pricing-tiers.md`

## Milestones
- 2026-08-15 Beta with five customers
```

- **Identity is the project name**, which is the filename slug. Read the folder before creating a file: a project that already exists gets updated, never duplicated under a second spelling.
- **The note stays here in `notes/`; only the one-line summary and the pointer go to the project file.** Duplicating the note content is how the two versions diverge.
- **Closing is a status line, not a deletion**: `status: done — 2026-09-01` or `status: cancelled — 2026-09-01` inside the file, because the file is the record of what was delivered. Past ~20 closed projects, move them to `~/Clawic/data/projects/archive/<project>.md` without renaming.
- **Amounts carry their currency in the value** (`4200 EUR`, not `€4200`) and dates are ISO, because other skills add these columns up.
- **Foreign structure wins.** If the project file already exists with different headings, add under the closest one rather than restructuring it.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`open-threads.md` — `## Open Threads`. Extracted when the table passes ~15 rows, which usually means the weekly review has stopped closing threads and that fact is itself the finding.

`recurring-meetings.md` — `## Recurring Meetings`. Extracted past ~15 recurring series; carries the carry-forward column, which is the only reason the file is worth keeping.

`platform-facts.md` — `## Platform Facts`. Extracted when the user runs three or more platforms and the vault paths, database ids and folder maps outgrow the section.
