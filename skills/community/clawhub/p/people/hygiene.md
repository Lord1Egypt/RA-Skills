# Hygiene — Merges, Imports, And Keeping The Book Trustworthy

An address book fails quietly. Nothing breaks; the facts just stop being true, and one day the user checks something against reality, finds it wrong, and never fully trusts the book again. Hygiene is the work that prevents that single event.

**Read the whole of `~/Clawic/data/contacts/contacts.md` before any merge, import, or review pass** — these are the only operations in this skill that touch rows written by other skills, and the constraint is to fix duplicates without ever rewriting a foreign row's meaning.

**Contents:** [The Roster Review](#the-roster-review) · [Duplicates And Merge Order](#duplicates-and-merge-order) · [Bounces And Dead Channels](#bounces-and-dead-channels) · [Imports](#imports) · [Promoting A Candidate](#promoting-a-candidate) · [Decay And Dormancy](#decay-and-dormancy) · [Deletion](#deletion) · [Scale Transitions](#scale-transitions)

## The Roster Review

Runs on `roster_review` (default quarterly), tracked in `## Due`. Top to bottom, and it is a pass over exceptions, not over every record.

| Check | What to do |
|---|---|
| Untiered people | Assign a tier, or `orbit` by default (SKILL.md, Relationship Tiers) |
| Records with no `Last contact` | Set from the newest log entry, or `unknown` — never a guess |
| Employer or city untouched for over 2 years | Mark unverified in the answer, do not delete (`details.md`) |
| Bounced or dead channels | See below |
| Duplicate candidates: same name, same employer, similar handle | Merge or explicitly mark as distinct people |
| Open loops older than 60 days | Chase once, or delete the row — a loop nobody will close is noise |
| Candidates never promoted | Delete from `candidates.md` |
| Tags used exactly once | Delete the tag, keep the person (`search.md`) |
| `inner` tier larger than ~15 | It is not an inner tier; re-tier honestly |
| People with no detail beyond a name | Either capture one line next time they come up, or drop to `orbit` |
| Dates with no person, people with no record | Fix the orphan in whichever direction is real |
| Anything on `do-not-surface.md` older than a year | Leave it. Only the user removes a name from that list |

The review writes its run date to `## Due` and its findings to `## Roster Shape` — counts per tier, merges done, deletions done. Without that line the next review starts from zero and redoes the same work.

## Duplicates And Merge Order

Identity is the email lowercased, then the primary handle, then `<kebab-name>` plus a stable disambiguator (SKILL.md Rule 2), and it lives in the `Key` column of `contacts.md`. A row that arrived without one gets its key filled in before anything else — comparing rows with no keys is comparing names, which is the merge that destroys histories. Duplicates appear from three sources: an import, a name change, and the same person reached on a second channel.

**Before merging, prove they are the same person.** Same name is not proof — same name plus a shared employer, a shared event, or a channel that reaches both is. When proof is absent, mark both records `possible duplicate of <key>` and leave them; a wrong merge destroys two histories and is not reversible from the file.

Merge order, once proven:

1. **Choose the surviving key**: the channel that still works, read from the `Key` column of both rows. If both work, the one the user actually uses. Write it into the survivor's `Key` column in the same turn.
2. **Union the details.** Where two facts conflict, the **newer dated** one wins and the older is kept as a dated line in the log, not deleted — the conflict is often a real change over time.
3. **Concatenate the logs and re-sort by date.** Never interleave by guess: entries with no date go to the bottom under `## Earlier` marked undated.
4. **Union the dates and tags**; take the higher tier and the shorter cadence.
5. **Delete the losing row and file** in the same turn, and add the losing key to the surviving record's alias field so a future import recognizes it as already merged.
6. **Write the merge and its date to `## Roster Shape`.** This line is what stops the next import from re-creating the duplicate.
7. If one of the two rows was written by another skill, keep its columns and its wording intact in the survivor and add what is missing as extra columns or as detail in the person file. Never rewrite a foreign row's meaning to fit this skill's format (`memory-template.md`).

## Bounces And Dead Channels

- A hard bounce, a failed delivery, or a number that no longer connects: mark the channel `dead` with the date on the record. Do not delete it — a dead channel is the evidence that stops the same address being retried in a year.
- Set the preferred channel to the next one that works. If none does, the person is `unreachable`, which is a state, not a deletion.
- **Unreachable is a reason to ask the network, not to drop the record.** Whoever introduced them is in the "how we met" field, and that is the recovery path (`search.md`).
- Silence is not a bounce. A person who does not reply is reachable and has not replied — those are different facts with different responses (`keeping-in-touch.md`).

## Imports

Bulk import is the single fastest way to destroy an address book: 800 rows the user cannot place drown the 40 that matter, and the book stops being consulted within a month (SKILL.md Traps).

The rule: **imports land in `~/Clawic/data/people/candidates.md`, never in `contacts.md`.**

| Source | What it actually contains | Handling |
|---|---|---|
| Phone contacts / vCard | Everyone ever dialed, including plumbers and taxis, with no context | Import as candidates; keep only rows with a real name and a placeable context |
| LinkedIn export | Every accepted connection, with a job title frozen at connection time | Candidates only; the job titles are historical and marked as such |
| Email address book | Everyone ever mailed, including no-reply addresses | Candidates only; filter automated senders before anything else |
| CSV from another tool | Whatever the tool's schema was | Map columns explicitly to the fields in `memory-template.md`; drop columns with no home rather than inventing fields |
| An event attendee list | People who were in a room | Not contacts and not candidates — only those actually met (`capture.md`) |
| A shared or inherited address book | Someone else's relationships | Do not import. Third-party relationship data the user was not given for this purpose (`privacy.md`) |
| Anything else | Unknown | Candidates, with the source and date recorded at the top of the file |

Before writing candidates: check every row against existing keys and drop the ones already present. The import mapping, if it took any thought, is `artifacts/import-map-<source>.md` so the next import from the same source is mechanical.

## Promoting A Candidate

A candidate becomes a contact on a **real interaction** or on the user naming them, never in bulk and never at import time.

1. Read `contacts.md` for the key. Existing row means update in place, not promote.
2. Write the row with tier `orbit` unless the interaction says otherwise, `Last contact` = today.
3. Capture at least the "one specific thing" from the interaction that triggered the promotion (`capture.md`).
4. Delete the candidate row in the same turn. A candidate that also exists as a contact is a duplicate waiting to be merged.

## Decay And Dormancy

- **`dormant` is the answer to almost every "should I delete this?"** The record is preserved intact and never surfaced. Ten years of context costs a few lines and the relationship comes back more often than not.
- Move to `dormant` when: no interaction for years and no reason to expect one, a group friendship that has ended with the group, or a professional contact from a chapter that closed.
- Dormant records are excluded from sweeps, briefs, date scans, and counts — but not from search, which is the entire reason they are kept.
- Reactivation is a tier change and nothing else; the history is already there, and that history is what makes the reconnection message writable (`keeping-in-touch.md`).

## Deletion

Deletion is real and it is different from dormancy.

- **The user asks to remove someone**: delete the row, the person file, their date lines, their open loops, and their entries in group blocks. Note only that a removal happened and its date in `## Roster Shape` — no name, no reason.
- **The person asks to be removed** (they know the book exists and object): same, and additionally never re-import them; the alias record that would prevent re-import cannot be kept either, so the note in `## Roster Shape` is the only defense and it stays anonymous.
- **Deletion propagates to exports.** A CSV or vCard produced before the deletion still holds them; regenerate or delete it (`privacy.md`).
- Never delete on the agent's own initiative. Records are moved to `dormant` instead, always.

## Scale Transitions

| Roster size | What changes |
|---|---|
| Under 15 | One table in `contacts.md`, no person files unless one person outgrows a row |
| 15-150 | Person files for anyone with detail; `contacts.md` is the index. `## Dates`, `## Open Loops` and `## Groups` split out of `memory.md` at their thresholds (`memory-template.md`) |
| Over 150 | Tags stop being optional: unstructured notes are no longer searchable at this size (SKILL.md, Where Experts Disagree). The review moves to monthly, and `orbit` is where most people belong |
| Over 500 | This is a CRM-shaped problem, not an address book. Keep the personal roster here and move commercial relationships to `crm` |

Each transition happens once and is written to `## Roster Shape` when it does, so the next session recognizes the shape it is working in.

**Write in the same turn**: merges, deletions, renames and tier changes into the surviving record and a dated line in `## Roster Shape` in `~/Clawic/data/people/memory.md`; the review's run date into `## Due`; imports into `~/Clawic/data/people/candidates.md` with their source and date; an import mapping worth reusing into `~/Clawic/data/people/artifacts/` with its `## Boxes` line (`memory-template.md`).
