# Working File Templates — Journal

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced; `entries/` is what the user wrote and is never edited by you. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/journal/config.yaml` | Key by key, read-modify-write |
| Practice state, box index, due dates, themes, open threads, read scope, prompt results | `~/Clawic/data/journal/memory.md` | Rewritten in place; stays small |
| The entries themselves | `<entries_path>/<year>/<YYYY-MM-DD>.md` | One file per day, appended within the day; never rewritten |
| Attachments belonging to an entry | Next to it, same date prefix: `<year>/<YYYY-MM-DD>-<name>.<ext>` | One per attachment |
| Weekly, monthly, quarterly, annual reviews | `~/Clawic/data/journal/reviews/<year>.md` | Append-only, one heading per period, cut by year |
| Decision entries with prediction, confidence and review date | `~/Clawic/data/journal/decisions/<year>.md` | Append-only, cut by year; review dates copied into `## Due` |
| Work wins, failures, impact numbers, lessons | `~/Clawic/data/journal/work-log/<year>.md` | Append-only, cut by year |
| Topics never to prompt about, analyze, or resurface | `~/Clawic/data/journal/no-go.md`, pointed at by `no_go_file` | One line per topic |
| Things read whole when their subject comes up — unsent letters, annual reviews, values statements, year themes, one-on-one prep, assembled performance reviews, runbooks | `~/Clawic/data/journal/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Letters written to a person | `~/Clawic/data/journal/artifacts/letters/<date>-<who>.md` | One file per letter |
| Mood and symptom ratings measured in series | `~/Clawic/data/health/mood.md` (**shared**) | One row per rating, every skill's ratings in one series |
| A person the user asks to track | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, name and channel only |
| A decision that belongs to a tracked project | `~/Clawic/data/projects/<project>.md` (**shared**) | One line, the summary only |
| A compensation or subscription figure the user asks to track | `~/Clawic/data/finances/` (**shared**) | One row per account or subscription, in the file its kind picks |
| **Anything durable this table does not name** | `~/Clawic/data/journal/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, a health metric, a booking, a figure? Then the shared box, not here, and only the neutral field (`privacy.md`). (2) Is it a text read whole when its subject comes up — a letter, a policy, a decision with its reasoning, a review? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| The user wrote or dictated anything | The entry file, verbatim (SKILL.md Rules 1-2, 5) |
| They gave a mood rating | `~/Clawic/data/health/mood.md` (shared) |
| An entry was saved | `## Practice`: last entry date, run length, slot |
| They said they would come back to something | `## Open Threads` |
| They said not to reread something, or to drop a topic | `## Read Scope`, and the topic to `no-go.md` |
| A prompt was offered | `## Prompts That Land`, marked landed or flopped |
| A review ran | `reviews/<year>.md` under its period heading; run date into `## Due` |
| The annual review ran | `artifacts/annual-review-<year>.md`, plus its summary line in `reviews/<year>.md` |
| A theme cleared the pattern bar (SKILL.md Rule 7) | `## Themes`, with count, week-spread and window |
| A decision was made | `decisions/<year>.md`, and its review date into `## Due` |
| A decision's review date arrived and was scored | The same row in `decisions/<year>.md` |
| A work win, failure, or lesson happened | `work-log/<year>.md` |
| A letter, values statement, or long piece was written | `artifacts/` |
| A practice was started, changed, or abandoned | `## Practice`, with the date and why |
| A lapse was diagnosed, or the floor changed | `## Practice` |
| Anything in SKILL.md Red Flags fired | `## Escalations`: date, observation, action — never content |
| A migration, layout change, backup drill, share, or deletion happened | `## Practice`, one dated line |
| Recurring work was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Entries, reviews, decisions, work log, artifacts and the shared boxes are born as their own files. Everything else begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/journal/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

The entry corpus is exempt: it is a dated log and lives in `entries/<year>/` from the first day, never inside `memory.md`. Artifacts are exempt: a letter or an annual review is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not the entries, not files you create, not text the user pastes in and asks you to keep. A vented work log, a pasted error message, a `.env`, or a screenshot transcript is the densest source of secrets there is: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:API_KEY` · `keychain:home-router` · `1password:Personal/Bank` · `bitwarden:Personal/Journal` · `vault:secret/personal/backup` · `profile:work` · `file:~/.ssh/id_ed25519`

In a text, the pointer goes where the value was: `the router password is <keychain:home-router>`. Say in one line that you did it — silent redaction leaves the user believing something was saved that was not.

This pair of lists is the one place they are written; `privacy.md` explains the distinction and points here rather than repeating it.

In this domain — **not secrets, keep them**: names of people, employers, places, projects, clinics, banks and insurers; dates and times; feelings, diagnoses and medications the user chose to record; amounts with their currency; last four digits of a card; usernames and email addresses; tag names; mood scores; filenames of attachments.

**Secrets, strip them**: passwords, PINs and passphrases (including the journal's own encryption passphrase); API keys, tokens and connection strings pasted from a work log; recovery phrases and 2FA backup codes; private keys; full card and bank account numbers; national identity or passport numbers; anyone else's credentials mentioned in passing.

Private is not the same as secret: most of a journal is private and stays exactly as written. Only values that authenticate something are stripped (`privacy.md`).

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [entries/](#entries) · [reviews/](#reviews) · [decisions/](#decisions) · [work-log/](#work-log) · [artifacts/](#artifacts) · [no-go.md](#no-gomd) · [shared health series](#shared-health-series) · [shared contacts, projects, finances](#shared-contacts-projects-finances) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/journal/` if it does not exist.

```yaml
entries_path: ~/Clawic/data/journal/entries/
entry_naming: YYYY/YYYY-MM-DD
day_boundary: "04:00"
agent_read_scope: on-request
reflection_style: mirror
mood_scale: 1-5
review_cadence: weekly
nudge: false
no_go_file: ~/Clawic/data/journal/no-go.md
entry_language: german

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  intake: dictation           # entries usually arrive spoken
conventions:
  frontmatter: [date, tags, mood, practice]
cadence:
  slot: "after the first coffee"
  review_day: sunday
  on_this_day: false
safety_posture:
  redact_third_parties: always
restrictions:
  rejected_practices: [five-minute-journal]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Journal Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Entries (412, 2021-2026) → `entries/<year>/<YYYY-MM-DD>.md`; open only within `agent_read_scope`, or for a review or search the user asked for
- Reviews (2026) → `reviews/2026.md`; read before running any review
- Decisions (7 open) → `decisions/2026.md`; read at every quarterly and whenever a decision is being made
- Work wins and lessons (2026) → `work-log/2026.md`; read before any review, 1-on-1, or interview prep
- Annual review 2025 → `artifacts/annual-review-2025.md`; read at the next annual review
- Letter to Dad, unsent → `artifacts/letters/2026-04-11-dad.md`; read only if the user names it
- No-go topics (3) → `no-go.md`; read before every prompt, analysis, review and resurfacing
- Mood series (approx. 300) → `~/Clawic/data/health/mood.md` (shared); read before any mood claim

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Weekly review | week, Sunday | 2026-07-19 | 2026-07-26 |
| Monthly review | month, last day | 2026-06-30 | 2026-07-31 |
| Quarterly: decision scoring + tag prune + backup restore | quarter | 2026-04-05 | 2026-07-05 |
| Decision review: leave the contract role | once, 2026-09-01 | — | 2026-09-01 |
| Annual review | year, mid-January | 2026-01-14 | 2027-01-14 |

## Practice
Started 2021-03. Daily entries, evening slot, dictated on the walk home; typed at weekends.
Current run 12 days, longest 96, 22 entries in the last 30 days. Floor: one sentence.
Morning pages tried 2024, dropped after 3 weeks — "felt like homework". Do not re-recommend.
2025-11: migrated from Day One (JSON export kept). 2019-2020 entries lost their times, dates intact.
2026-02: lapsed 5 weeks after the move; restarted at 3/week, back to daily in April.

## Read Scope
- 2024-09 to 2024-11 — the separation. Not to be reopened or resurfaced.
- Letters in `artifacts/letters/` — only when named.

## Themes
| Theme | User's words | Entries | Weeks | Window | First seen |
|---|---|---|---|---|---|
| work overload | "the sprint thing" | 11 | 6 | 2026-05 to 2026-07 | 2026-05-04 |
| sleep | "wired at night" | 7 | 5 | 2026-06 to 2026-07 | 2024-01-18 |
Active tags: work, sleep, family, money, health, writing, travel.
Merged 2026-07: "job" → "work". Retired: "misc" (2 uses).

## Open Threads
- Whether to stay in the contract role — decision entry open, review 2026-09-01
- "Come back to what happened with M." — raised 2026-07-14, not yet written
- Carry-forward from 2026-W29: ask for the Thursday off

## Prompts That Land
| Date | Prompt | Result |
|---|---|---|
| 2026-07-19 | "What did you avoid all week?" | landed, longest entry of the month |
| 2026-07-12 | "What are you grateful for?" | flopped, two lines |
| 2026-06-30 | "What would have to be true for the other option to be right?" | landed, own — reuses it unprompted |

## Escalations
2026-02-08: ratings ≤2 for 11 of 14 days plus sleep loss in the writing. Named it, recommended a GP, they had an appointment already. No content recorded.

## How They Work
Writes to think, not to record. Wants a mirror, not advice — one sentence back, then silence.
Will stop writing if a pattern is surfaced uninvited. Analysis only on request.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session. State an overdue item in one line only when `nudge` is true or the user is already asking about the practice — a due date is not a licence to nag (`consistency.md`).
- **`## Practice`**: the diagnosis history is the point. A lapse recorded with its cause is what stops the next lapse getting the advice that already failed.
- **`## Read Scope`**: dates and a label, never content. This section is read before any entry is opened, by every part of the skill.
- **`## Themes`**: only themes that cleared SKILL.md Rule 7's bar, with the counts that cleared it. `User's words` is the label used in every future report — never substitute your own vocabulary (`patterns.md`).
- **`## Prompts That Land`**: `landed` means the entry was not stopped early; `flopped` means under two lines or a change of subject; `own` means the user invented it.
- **`## Escalations`**: date, observable signal, what was said, what was recommended. Never a quote, never a diagnosis, never a risk score.
- These headings are exactly the ones `themes.md` and `prompt-log.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their practice and their register |
| `complete` | Know their slot, their floor, their register and their no-go list |

## entries/

The user's writing. **Written verbatim, appended within the day, never edited, never rewritten** (SKILL.md Rules 2 and 5).

```markdown
---
date: 2026-07-26
tags: [work, sleep]
mood: 3
practice: daily
---

...their words, exactly as written or dictated, their line breaks, their typos...

## 23:40

...a second entry the same day, appended under its own time heading...

## Update 2026-07-28

...a correction the user makes later. Never an edit to the text above.
```

- Frontmatter is optional and stays optional until the user asks for tags or a rating (`storage.md`).
- `practice` is what lets an analysis exclude never-reread material. Set it whenever the entry belongs to a named practice.
- Your interpretation never goes in this file. It goes in the reply, or in `reviews/<year>.md` when it was asked for.
- Attachments sit beside the file with the same date prefix and are referenced by filename.

## reviews/

```markdown
# Reviews — 2026

## 2026-W30
Window: 2026-07-20 to 2026-07-26 · 5 entries across 5 days · morning pages excluded (2).
Themes: work 4, sleep 3, family 1.
Avoided: the conversation about the contract.
Carry-forward: ask for the Thursday off.

## 2026-07
Window: 31 days · 22 entries across 20 days.
Patterns (bar cleared): work overload — 11 entries, 6 distinct weeks.
Counts (bar not cleared): money, 3 entries in one week.
Carry-forward from 2026-06: "sleep before midnight" — dropped, not attempted.
Mood: 24 paired days, median 3, four days ≤2 (all Sundays — weekday is a confound).
Carry-forward: schedule the decision review.

## 2026 Annual
One sentence: the year I stopped waiting for the contract to resolve itself.
Next year's theme: finish things. Full review: `artifacts/annual-review-2026.md`.
```

- Every review states its **window, entry count, days covered, and what was excluded**. A review without its denominator cannot be compared to the next one.
- Paraphrase and count; never quote an entry (SKILL.md Rule 9).
- Carry-forwards are named in the next review by name, with their outcome: done, dropped, or still open.

## decisions/

```markdown
# Decisions — 2026

## 2026-07-14 — Leave the contract role at the end of the term?
Options: leave at term end · renew 6 months · renew and look while inside.
Chose: leave at term end.
Expected outcome: 2 months without income, offer signed by November.
Confidence: 60%.
Know: two warm intros, 4 months runway. Assuming: the market in September is like May.
State: tired, third bad week in a row, decided on a Sunday night.
Premortem — a year later it failed because: the runway went on the tax bill and I took the first offer.
Review date: 2026-09-01.

### Review 2026-09-04
Outcome: no offer yet, 1 month in. Prediction: unclear — too early, review again 2026-11-01.
Confidence check: pending.
```

- **Written before the decision, never after** (`practices.md`). An entry created after the outcome is known is a memoir, not a decision journal.
- Confidence is a number, or the entry produces nothing at review time.
- The review date goes into `## Due` the same turn the entry is written.
- Score the prediction and the confidence **separately**, and read the entry before recalling the outcome.
- If the decision belongs to a tracked project, one sentence goes to `~/Clawic/data/projects/<project>.md`; the deliberation stays here.

## work-log/

```markdown
# Work Log — 2026

| Date | What | Impact | Who saw it | Link |
|---|---|---|---|---|
| 2026-07-22 | Cut CI build 14 min → 3 min | ~147 eng-hours/month at 40 builds/day (estimate, from the CI dashboard) | Marta, whole backend team | PR 1841 |
| 2026-07-09 | Talked the team out of the rewrite | ~2 quarters of work; shipped the adapter instead | Tech lead, staff eng | design doc |
| 2026-06-30 | Missed the migration rollback window | 40 min degraded; runbook now has the checkpoint | on-call channel | incident 204 |

## Learning
| Date | Believed | Happened | Do differently |
|---|---|---|---|
| 2026-06-30 | The rollback was one command | The command needed a flag nobody had run in prod | Rehearse rollbacks on staging with the exact command |
```

- **Same day, under 30 seconds a line** (`work-journal.md`). A weekly catch-up loses the small wins, and the small wins are what make a review credible.
- Every impact number carries its unit, its period, and whether it is measured or estimated.
- Failures go in the same table with what changed. A log with no failures reads as incomplete at review time.
- A lesson recurring a third time becomes a runbook in `artifacts/`, linked from here.

## artifacts/

One file per thing, at `~/Clawic/data/journal/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **an unsent letter**, **an annual review**, **a values statement or year theme**, **one-on-one prep**, **an assembled performance review**, **a runbook for a recurring lesson**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn. Every secret inside is already a pointer.

```markdown
# Letter — to Dad, unsent
*Read only if the user names this file. Written 2026-04-11.*

...the letter, in full...
```

```markdown
# Annual review — 2026
*Read at the next annual review, and when a year feels like it is repeating. Written 2027-01-14.*

Closed this year: ...
Carried over: ...
Believed in January and no longer: ...
One sentence: ...
Next year's theme: ...
```

```markdown
# Values — what I keep choosing
*Read before any big decision, and at the annual review. Written 2026-02-02, last revised 2026-07-01.*

...three or four statements, each with the evidence from entries that produced it...
```

- **Letters go in `artifacts/letters/<date>-<who>.md`** so they never surface accidentally in a review or a search for something else.
- A shared excerpt, if the user asks for one as a file, goes to `artifacts/shared-<date>-<recipient>.md` — the record of what left (`privacy.md`).
- If an artifact belongs to a tracked project, the one-line summary goes to `~/Clawic/data/projects/<project>.md` and the full text stays here, referenced by name.

## no-go.md

Pointed at by `no_go_file`. Plain list, read before every prompt, analysis, review and resurfacing.

```markdown
# Topics not to raise

- The separation (2024) — added 2025-01-06
- My brother's diagnosis — added 2026-03-12
- Weight — added 2026-05-02
```

- Created the first time it is needed: write the file and set `no_go_file` to its path in `config.yaml`, in the same turn.
- Added the moment the user says any version of "don't bring that up again", with no confirmation question.
- Removed only when the user says so explicitly. A single mention by them does not reopen a topic.
- It constrains the agent, not the user: a no-go topic in a fresh entry is captured normally, without comment.

## Shared health series

Lives at `~/Clawic/data/health/mood.md` and is shared with every health, sleep, and fitness skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Mood

Scale: 1-5, where 1 = "cannot get anything done", 5 = "the good version of a normal day" (anchored 2026-01-04).

| Date | Score | Scale | Time | Source |
|------|-------|-------|------|--------|
| 2026-07-26 | 3 | 1-5 | 22:40 | journal |
| 2026-07-25 | 2 | 1-5 | 23:10 | journal |
```

- **Identity is `Date` + `Source`.** Read the file before adding. If that pair is already there, update the row in place — it is yours. Never touch a row whose `Source` you did not write; another skill owns it.
- **The scale travels in the row**, because a 1-10 row and a 1-5 row in one column are not comparable and someone will average them. The endpoint anchors go in the header line, in the user's words, with the date they were set.
- **Never rescale historical values.** Changing `mood_scale` starts a new series; the old rows keep their old scale and comparisons across the boundary are not available.
- **No content leaves with the number**: no entry text, no reason, no events (`privacy.md`).
- **Scale cut**: one row per rating in `mood.md`; past ~400 rows, split by year into `~/Clawic/data/health/mood-<year>.md` and leave `mood.md` as the index with the anchors and a line per year.
- **Adapt to what exists.** If ratings are already under a `## Mood` heading in `~/Clawic/data/health/profile.md` (where a health skill may have started them while there were few), follow that until it passes ~15 rows, then move them to `mood.md` and leave the index line in `profile.md`. If `mood.md` exists with different columns, match its columns and add anything missing as a trailing note — never rewrite its header.
- **Retirement**: when the user stops tracking, add a final line stating the date tracking stopped. Do not delete the series; a gap with no explanation reads as lost data.
- A symptom tracked in series follows the same rules in `~/Clawic/data/health/<symptom>.md` (`practices.md`).

## Shared contacts, projects, finances

Written to only when the user asks, and only the neutral field (`privacy.md`).

**`~/Clawic/data/contacts/contacts.md`** — `Name | Key | Role | Preferred channel | Context | Last contact | File`.

- **Identity is `Key`**: lowercase email → handle → `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- Read before adding. If the key exists, update in place; only absence justifies a new row.
- **`Context` holds a neutral relationship fact** ("sister", "manager 2024-2026"), never a characterization and never anything drawn from an entry.
- Past 15 people, or as soon as one does not fit its row, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If the folder already looks like that, follow it.
- Foreign columns win: match the header you find, add anything missing as a trailing note, never rewrite it.

**`~/Clawic/data/projects/<project>.md`** — one file per project, from the first. This skill adds at most a one-line decision summary under a `## Decisions` heading, dated, with a pointer to `decisions/<year>.md`. Never the deliberation.

- **Read the file before writing.** Identity is the decision, not the date: if that decision is already summarized there, update its line in place; only absence justifies a second line.
- Foreign structure wins: if the file already exists with other headings, put the line under whatever heading holds decisions there and match its shape — never rewrite its header, and never create a duplicate `## Decisions` beside one that exists under another name.
- Closing a project is `status: done | cancelled — <date>` inside the file, never deleting it.

**`~/Clawic/data/finances/`** — only a figure the user asks to track, never the negotiation, the comparison, or the feeling. The figure picks the file: a recurring charge → `subscriptions.md`; a salary, balance, or other standing figure → `accounts.md`; a planned allocation → `budget.md`. Create only the file the figure needs.

- **Identity is the name of the account or subscription**, in the user's words, in a `Name` column. Read the file before adding: if the name is there, update that row in place; only absence justifies a new row. Never touch a row you did not write unless the user is changing that exact figure.
- Amounts carry their currency inside the value (`3,200 EUR`, not `€3,200`), and an estimate carries the date it was estimated in its own column, so nobody later reads it as measured.
- `subscriptions.md` — `Name | Amount | Period | Renews | Source`. It never splits: cancelling deletes the row, which is what keeps the table small.
- `accounts.md` — `Name | Kind | Amount | As of | Source`. Past 15 accounts, one file per account at `~/Clawic/data/finances/accounts/<name>.md` with the same fields, and `accounts.md` becomes the index (`Name | Kind | → file`).
- **Retirement**: a closed account or an ended salary keeps its row with `closed <date>` — a figure that vanishes reads as lost data. Only a cancelled subscription is deleted outright.
- **Adapt to what exists.** If the file is already there with different columns, match its header and add anything missing as a trailing note; never rewrite it. If the folder already keeps everything in one file, follow that until it passes ~15 rows.
- Account references only, never credentials: last four digits and a bank name are fine, full numbers and access details are not (Secrets above).

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`themes.md` — `## Themes`, plus `## Retired` for merged and deleted tags with the date and reason. This file is the reason a theme count means the same thing in July as in January; without it, every analysis re-invents the vocabulary and no two months are comparable.

`prompt-log.md` — `## Prompts That Land`, same three columns. It exists so a prompt that flopped is never offered twice, which is the single most visible sign to the user that the practice is being paid attention to.
