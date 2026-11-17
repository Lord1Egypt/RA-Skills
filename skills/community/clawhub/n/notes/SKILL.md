---
name: Notes (Local, Apple, Notion, Obsidian & more)
slug: notes
version: 1.1.5
description: Captures, structures, and retrieves notes in local markdown, Apple Notes, Bear, Obsidian, Notion, or Evernote. Use when the user says take notes, write this up, capture this, or turn this transcript into a note; for meeting, 1-on-1, decision, journal, project, or research notes; when a note must land in a specific app or vault; when action items need owners and real dates; when a note cannot be found again and titles, tags, folders, or an index are the problem; when quick captures pile up untriaged; when a decision needs a durable record; when a vault shows conflicted copies, duplicates, or links broken by a rename; when notes must move between apps, be exported, or be backed up; and when something is too sensitive to write down at all. Not for journaling practice and prompts (`journal`), meeting facilitation and agendas (`meetings`), Notion API development (`notion-api-integration`), running a to-do list (`task-list`), or growing a linked atomic-note knowledge base (`pkm`).
homepage: https://clawic.com/skills/notes
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📝
    os:
    - linux
    - darwin
    - win32
    displayName: Notes (Local, Apple, Notion, Obsidian & more)
    configPaths:
    - ~/Clawic/data/notes/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/notes/
    - ~/clawic/notes/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/notes/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/notes/
      - ~/clawic/notes/
---

**Data.** At the start of every session, read `~/Clawic/data/notes/config.yaml` (what the user declared: routing, vault path, cadences) and `~/Clawic/data/notes/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files; never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/notes/actions.md` before any question about commitments, deadlines, or what someone owes. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a note of any type; an action item, a completion, or a changed deadline; a decision and what it supersedes; a person who now owns something; the project a note belongs to; a routing choice, vault path, database id, or folder name that cost effort to find; a naming or tagging convention that got settled; a review that ran; or a template the user reshaped. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and projects go to shared boxes**, not here: attendees and action owners to `~/Clawic/data/contacts/contacts.md`, and the project a note belongs to `~/Clawic/data/projects/<project>.md`. The note keeps only the name as a pointer. Duplicating a person or a project is how two skills start contradicting each other.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a note you create, not in text the user pastes in to be saved. This is the domain where the user pastes most: a dump from a call carries the bridge PIN, the wifi password, the key someone read out loud. Replace each value with its pointer before writing — `env:NOTION_API_KEY`, `keychain:bear-token`, `1password:Work/Notion/agent`, `file:~/.config/notion/api_key` — and say in one line that you did it. If data sits at an old location (`~/notes/` or `~/clawic/notes/`), move it to `~/Clawic/data/notes/`, and say in one line that you moved it and from where.

A note is worth what it is worth on the day someone searches for it, which is usually months later and usually not the person who wrote it. Write for that day: a title that states the claim, a date, the people, the decision, and the commitments with owners. Capture during the event, not after — Ebbinghaus's forgetting curve costs you most of the unrecorded detail within 24 hours, and none of it comes back. Work from defaults immediately: never open with questions about which apps they use or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- Turning a conversation, call, transcript, or voice dump into a note that someone can act on
- Meeting, 1-on-1, interview, retro, client-call, decision, journal, project-update, or research notes
- Extracting action items with owners and dates, and keeping one honest list of what is open
- Retrieval work: a note that cannot be found, a naming scheme, tags versus folders, an index, dead links
- Housekeeping on a note corpus: conflicted copies, duplicates, backups, archiving, moving between apps
- Deciding whether something should be written down at all, and what to strip before writing it
- Not for journaling practice and prompts (`journal`), running a meeting (`meetings`), building against the Notion API (`notion-api-integration`), or growing a linked atomic-note knowledge base out of whatever gets sent in, where the link graph is the product (`pkm`) — this covers writing, storing, and finding the notes themselves

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Take notes on this call" | Capture decisions and commitments verbatim, everything else at ≤20% (Rule 3) | `meetings.md` |
| 1-on-1, interview, retro, client call | Each has one section that carries the value; the rest is optional | `meetings.md` |
| Transcript, voice memo, or a wall of pasted text | Extract claim → decision → action; the raw text is a source, not the note | `capture.md` |
| "Note this down" with no context | Quick capture to the inbox with a claim title; triage within 7 days (Rule 8) | `capture.md` |
| "We decided X" | Decision record: context, options, rationale, what it supersedes | `decisions.md` |
| Daily note, weekly review, monthly rollup | Cadence and prompts that survive a missed week | `journal.md` |
| Project status, handover, or launch write-up | Status note plus the pointer into the shared `projects/` box | `projects.md` |
| Book, paper, course, or highlight import | Quote versus your words, atomic notes, progressive summarization | `research.md` |
| "What do I owe anyone" / overdue chase | One tracker, absolute dates, escalation ladder | `action-items.md` |
| "I can't find that note" | Search order title → tag → full text; if only full text worked, the title is wrong | `retrieval.md` |
| Where does this note go — tags, folders, or links? | Thresholds that decide, not taste | `retrieval.md` |
| Conflicted copies, two devices, missing edits, backups | Conflict markers, merge by section, 3-2-1 backup | `sync.md` |
| Leaving an app, importing a corpus, exporting a vault | Fidelity matrix and the restore test before you commit | `migration.md` |
| "Should this even be written down?" | The record test, redaction, and what never enters a note | `sensitive.md` |
| Local markdown files | Naming, frontmatter, grep patterns, git | `local.md` |
| Apple Notes | `memo` CLI, folders, attachment limits | `apple-notes.md` |
| Bear | `grizzly` CLI, tag trees, append-only reality | `bear.md` |
| Obsidian | Vault selection, wikilink-safe renames, direct file edits | `obsidian.md` |
| Notion | API calls, database properties, pagination, rate limit | `notion.md` |
| Evernote | `clinote` CLI, notebooks, lossy formatting | `evernote.md` |
| Anything else notes | Write it as a quick capture with a claim title, route by Rule 1, and state where it landed | — |

Coverage map: `capture.md` inbox and raw input · `meetings.md` conversations · `decisions.md` records · `journal.md` daily and review · `projects.md` status · `research.md` sources · `action-items.md` commitments · `retrieval.md` finding things again · `sync.md` devices and backups · `migration.md` moving corpora · `sensitive.md` what not to write · `local.md` `apple-notes.md` `bear.md` `obsidian.md` `notion.md` `evernote.md` platforms.

## Core Rules

1. **Route by type, fall back loudly.** Platform = `routing.<type>` in `config.yaml`, else `default_platform`, else local. When the configured platform is unavailable (CLI missing, app not running, key absent), write locally and stamp the note `platform: local (fallback from notion)` — a silent fallback gives one note two homes and neither gets updated.
2. **The title is the claim, not the topic.** "Pricing" returns forty hits and answers nothing; "Pricing: staying at three tiers, revisit at 500 customers" answers the search before the file is opened. Local filenames: `YYYY-MM-DD_topic-slug.md` — date first so the directory sorts chronologically, slug so `grep` and fuzzy-open both work (`local.md`).
3. **Capture during, write up after — and cap the volume.** Target ≤20% of what was said, 100% of decisions, owners and dates. A verbatim transcript is not a note: it is 6,000 words in which the one decision is undiscoverable. Governed by `capture_verbosity`.
4. **Owner, verb, absolute date, or it is not an action item.** `@alice: send the pricing deck — 2026-08-04`. Resolve relative dates at write time ("next week" → the date it means), because the note gets read in November. No owner → it belongs in Open Questions, not the tracker (`action-items.md`).
5. **One fact, one home.** A decision lives in one decision note; meetings link to it. When a note is mirrored into another platform, the copy holds a pointer and is never edited — the second copy is where the two versions start disagreeing.
6. **Tag thresholds, not tag taste.** A tag matching more than ~10% of the corpus does not discriminate — promote it to a note type or a folder. A tag used once is a typo — merge or drop it at the monthly sweep. Working ceiling: ~20 live tags; past that, retrieval goes back to full-text (`retrieval.md`).
7. **No index before 30 notes.** Under 30, `grep -r` finds anything faster than a hand-maintained index goes stale. At 30+, build `index.md` and update it in the same turn a note is created — an index that is refreshed "later" is worse than none, because it is trusted and wrong (Rule 2 of `retrieval.md`).
8. **The inbox is triaged within 7 days.** Every quick capture gets promoted to a typed note, folded into an existing note, or deleted. An inbox older than 7 days is an archive nobody reads, and its existence stops the user from trusting search.
9. **What you write becomes a record.** Meeting, 1-on-1 and interview notes get read by people who were not there, and in an HR process or litigation by people you did not expect. Record decisions, evidence and commitments; keep speculation about people, health, and pay out of them (`sensitive.md`).

## Note Types

Nine types cover the domain. The trigger phrase decides the type; the type decides the required fields and where it lands. When two triggers fire, the type with a decision in it wins.

| Type | Fires on | Required fields | Default home (under `~/Clawic/data/notes/`) |
|---|---|---|---|
| Meeting | "meeting notes", "call with", "we talked about" | Date, attendees, absentees, decisions, actions | `meetings/` |
| 1-on-1 | "1:1", "check-in with", manager or report named | Carry-forward from last time, their topics, actions on both sides | `meetings/` |
| Interview | "candidate", "screen", "debrief" | Evidence and quotes separated from the assessment (`sensitive.md`) | `meetings/` |
| Retro | "retro", "post-mortem", "what went wrong" | Timeline, contributing factors, actions — never a name as a cause | `meetings/` |
| Decision | "we decided", "going with", "decision:" | Context, options rejected, rationale, effective date, supersedes | `decisions/` |
| Project update | "status", "project update", "where are we on" | Status, progress, blockers with who is blocking, next milestone | `projects/` |
| Journal | "daily note", "today I", "how did the week go" | Date, what happened, what it means, tomorrow's top three | `journal/` |
| Research | "notes on this paper", "highlights", "reading" | Source with locator, verbatim quotes in blockquotes, your claim | `research/` |
| Quick | "note:", "remember", "jot this down" | One claim line and a tag; triage in 7 days (Rule 8) | `quick/` |

Templates for each live in the file that owns the situation, so the type and its shape load together: `meetings.md`, `decisions.md`, `journal.md`, `projects.md`, `research.md`, `capture.md`.

## Platform Fit

One default (local), with the reason to leave it. Data flow matters: two of these send note content off the machine.

| Platform | Wins at | Costs you | Data flow |
|---|---|---|---|
| Local markdown | grep, git history, zero dependencies, nothing to lose access to | No mobile capture, no sync unless you build it | Stays on this machine |
| Apple Notes | Instant capture on every Apple device, scans, handwriting, shared folders | No bulk plain-text export, weak linking, CLI cannot touch attachments | Local, through the app |
| Bear | Fast tag-tree capture, honest markdown, nested tags | Apple platforms only; CLI appends but does not edit; app must be running | Local, through the app |
| Obsidian | Backlinks, graph, plugins, and the files stay plain markdown | Sync is a paid add-on or your own problem; renames outside the app break links | Local files |
| Notion | Shared databases, typed properties, teammates who are not in a terminal | Automation is API-only, ~3 requests/second, 100 results per page, lossy markdown export | Note content goes to api.notion.com |
| Evernote | An existing corpus and OCR over scanned pages | Thin CLI, lossy markdown, migration is the usual reason to open it | Note content goes to Evernote servers |

Default to local for anything that must still be readable in ten years, and route the types that need other people to the platform those people already open.

## Output Gates

Before writing or sending a note:

- Does the title state the claim rather than the topic (Rule 2)?
- Does every action item carry owner, verb, and an absolute date (Rule 4)?
- Were the decisions read back in the user's words, with what they supersede?
- Did the note land where routing says, stamped with the fallback if it fell back — and if that destination is a network platform (Notion, Evernote), did the user route the type there (Rule 1)?
- Is there a credential, PIN, recovery code, or third-party personal detail in what I am about to write? Pointer, or leave it out.
- Did anything durable come out of this — a note, an action, a decision, a person, a project, a routing fact, a settled convention, a review? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/notes/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_platform | local \| apple-notes \| bear \| obsidian \| notion \| evernote | local | Where a note goes when its type has no routing entry (Rule 1) |
| routing | list of `<note type>: <platform>` pairs | none | Per-type override, the first thing Rule 1 reads; e.g. `meeting: notion`, `journal: bear`. A type with no pair falls to `default_platform` |
| vault_path | path | none | Obsidian vault root; unset means `obsidian-cli`'s default vault (`obsidian.md`) |
| notion_database_id | text (id) | none | Target database for created pages (`notion.md`); an id, never a token |
| filename_pattern | date-first \| title-first | date-first | Local filenames and therefore directory sort order (Rule 2, `local.md`) |
| capture_verbosity | minimal \| standard \| verbatim | standard | How much of a conversation reaches the note (Rule 3); `verbatim` still requires the decisions block |
| tag_style | flat \| nested | flat | `#product` versus `#product/pricing`; nested only where the platform supports it (Bear, Obsidian) |
| review_cadence | daily \| weekly \| none | weekly | Which review runs in `journal.md` and which row appears in the `## Due` table |
| review_day | mon…sun | fri | The day the weekly review and the action sweep are due |
| action_target | notes \| external | notes | `notes` keeps `actions.md` as the tracker; `external` hands items to the user's task app and keeps only a pointer (`action-items.md`) |
| archive_after_months | number (3-36) | 12 | Age at which journal and quick notes move to their archive folder (`retrieval.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — which note apps are live at all, CLI versus direct file editing, the transcription source, the editor that opens notes — affects every platform file and the shape of each example
- **Conventions** — frontmatter fields, folder tree, wikilinks versus markdown links, title casing, checkbox style, whether emoji headings are used — affects every template
- **Platform** — OS, the mobile capture path, sync mechanism, vault location, and the language notes are written in when it differs from the conversation
- **Safety posture** — topics and clients that never leave the machine, whether writing to a network platform needs confirmation, how aggressively to redact, whether deletions are allowed at all — affects `sensitive.md` and the Output Gates
- **Output register** — note length, whether the note is shown before saving, how much reasoning is kept versus summarized
- **Work order** — capture-then-structure versus structure-first, and whether action extraction happens live or at the end of the conversation
- **Integrations** — the task app, calendar source, read-later app, and citation manager the user already runs (the choice, never credentials)
- **Cadence** — review day, inbox triage interval, orphan-link sweep, backup drill, archive run — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Thresholds** — the 30-note index trigger, the 7-day inbox limit, the 10% tag ceiling; a user who works differently moves them, and the moved value governs

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Writing the note up after the call | Most unrecorded detail is gone within a day; what survives is the version you now believe | Capture live, clean up after (Rule 3) |
| Topic titles | Search returns everything about pricing and answers nothing | Claim titles (Rule 2) |
| Pasting the whole transcript as the note | The decision exists but nobody will ever find it, and the paste carries data you did not choose to keep | Extract claim, decision, action; keep the raw text as a linked source (`capture.md`) |
| "ASAP", "soon", "next sprint" | Never resolves to a date, so it never becomes overdue and never gets chased | Absolute date at write time (Rule 4) |
| Tracking actions in whichever app holds the note | Three apps each hold a third of the commitments; the user trusts none | One tracker (`action-items.md`) |
| Folders as the primary structure | A note has one folder and three subjects; the other two are unreachable | Folder by type, retrieval by title, tag and link (`retrieval.md`) |
| A tag for every idea | 300 tags is the same as no tags | Rule 6 |
| Renaming a note in Finder or Explorer | Wikilinks break silently and backlinks disappear with no error | Rename through the app's own move command (`obsidian.md`) |
| Editing the same note on two devices with one offline | Last write wins, and the loser is discarded without a prompt | Conflict rules in `sync.md` |
| Trusting an export you never restored | Notion's markdown export flattens nested databases; Evernote's HTML loses checkboxes | Restore one exported note into the target before migrating the corpus (`migration.md`) |
| Hand-maintained index from note one | Stale in a week, and a trusted stale index sends the user to the wrong file | Rule 7 |
| Keeping a "someday" inbox | It becomes the place notes go to die, and its size makes search feel useless | Rule 8 |
| Judgments about a person in a meeting note | The note outlives the opinion and gets read by the person or by legal | Evidence and decisions only (`sensitive.md`) |
| One note per project, appended forever | At 400 lines it is a document nobody re-reads, and the current status is buried mid-file | Status at the top, one note per update (`projects.md`) |

## Where Experts Disagree

- **Folders versus links.** PARA (Forte) organizes by actionability and wins for people who browse and who onboard others; Zettelkasten (Luhmann) organizes by link and wins for ideas that get recombined. The frontier is how you re-enter: mostly search and browse → folders; mostly "what else touched this" → links. Teams get a third constraint — permissions and onboarding are folder-shaped.
- **Atomic notes versus long documents.** Atomic wins for claims you will reuse in other contexts. Long-form wins for meetings and decisions, where chronology and who-said-what *are* the content; atomizing them destroys the record.
- **Capture everything versus capture selectively.** Capture-everything is defensible only when retrieval is fast and pruning is real. If nothing has been deleted in a year, the corpus has already failed and selectivity is the cheaper fix.
- **Daily note as the single entry point.** Strong for people whose work is continuous and self-directed; weak where notes must be found by subject months later by someone else, because a date is the one thing nobody remembers.
- **One vault or two.** Merging work and personal maximizes serendipity and minimizes friction; splitting them is the only defensible answer where an employer policy, a client NDA, or discovery risk applies (`sensitive.md`).

## Security & Privacy

**External endpoints:** only when the user has routed a note type to that platform.

| Endpoint | Data sent | When |
|---|---|---|
| `api.notion.com/v1/pages`, `/blocks/*` | Note title and content | The user routed a type to Notion and supplied a key |
| `api.notion.com/v1/search`, `/data_sources/*/query` | Search terms and filters | The user searches Notion notes |
| Evernote servers, via `clinote` | Note title and content | The user routed a type to Evernote and logged in |

Apple Notes, Bear and Obsidian are local: their CLIs talk to a locally installed app or to files on disk. Local markdown never leaves the machine.

**Credentials:** platform tokens are read by the platform CLIs from the user's own locations (`~/.config/notion/api_key`, `~/.config/grizzly/token`, the OS keychain). This skill does NOT store, log, copy, or transmit them, and never writes a credential into `~/Clawic/data/`.

**Local storage:** notes, action items, index, preferences and memory stay in `~/Clawic/data/notes/`, plus person and project pointers in the shared `~/Clawic/data/contacts/` and `~/Clawic/data/projects/`.

**Guardrails:** nothing is installed. A platform is used only after the user routes a type to it. Deleting or overwriting an existing note is confirmed first, and bulk operations (archive runs, tag merges, migrations) name exactly how many files they touch before running.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/notes (install if the user confirms):
- `meetings` — running the meeting itself: agendas, facilitation, follow-up discipline
- `journal` — the journaling practice, prompts and reflection, once the daily note exists
- `task-list` — a full task system when `action_target: external` and actions outgrow one tracker
- `voice-notes` — voice message transcripts as a structured knowledge base
- `pkm` — a linked atomic-note knowledge base grown from links, quotes and stray ideas, when the graph matters more than the record

## Feedback

- If useful, star it: https://clawic.com/skills/notes
- Latest version: https://clawic.com/skills/notes

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/notes.
