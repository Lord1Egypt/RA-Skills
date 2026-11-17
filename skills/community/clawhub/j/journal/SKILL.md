---
name: Journal
slug: journal
version: 1.0.2
description: 'Runs a personal journaling practice: capturing entries, prompts for a blank page, weekly and yearly reviews, and patterns across years of writing. Use when the user wants to write, vent, dictate, or get something out of their head; when they ask for a prompt or say they are stuck; for morning pages, bullet journal, five-minute, interstitial, dream, travel, decision, or work journaling; for a weekly, monthly, or annual review; when they ask what they have been writing about, whether a mood or theme keeps recurring, or what they wrote a year ago; when the practice lapsed and they want to restart; when entries need naming, tagging, searching, encrypting, backing up, or migrating out of Day One, Notion, or an Obsidian vault; when writing through grief, anger, shame, or a decision that will not settle; or when a work journal must become performance-review evidence. Not for retrieval-oriented notes (`notes`), gratitude logging alone (`gratitude`), or live emotional support (`psychologist`).'
homepage: https://clawic.com/skills/journal
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📔
    os:
    - linux
    - darwin
    - win32
    displayName: Journal
    configPaths:
    - ~/Clawic/data/journal/
    - ~/Clawic/data/health/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
    - ~/journal/
    - ~/clawic/journal/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/journal/
      - ~/Clawic/data/health/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
      - ~/journal/
      - ~/clawic/journal/
---

**Data.** At the start of every session, read `~/Clawic/data/journal/config.yaml` (what the user declared) and `~/Clawic/data/journal/memory.md` (what you observed, plus its `## Boxes` index, its `## Due` table, and its `## Read Scope` section). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Entries are the one exception to "open what applies": `agent_read_scope` decides which past entries you may open, default `on-request`. `memory.md` is the state of the practice; the entries are the person's writing. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: an entry (always, verbatim); a mood rating; a review; a decision with its predicted outcome and review date; a theme that crossed the pattern bar; a prompt that landed or flopped; an open thread the user said they would come back to; a topic they asked you never to raise again; a work win with its number; or something they will re-read whole — an unsent letter, a values statement, a year theme. `memory-template.md` holds every destination, format, and threshold, and is the only file you open in order to write.

**Neutral fields leave the journal folder; content never does.** A mood rating goes to the shared series `~/Clawic/data/health/mood.md` so sleep, fitness, and health skills read the same numbers. A person becomes a row in `~/Clawic/data/contacts/contacts.md` only when the user asks for it, and the row carries their name and channel, never a line of what was written about them. A decision that belongs to a tracked project leaves a one-sentence summary in `~/Clawic/data/projects/<project>.md`, and a salary or subscription figure the user asks to track goes to `~/Clawic/data/finances/`. Formats, identity keys, and the write protocol for all four: `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in an entry, not in a file you create, not in text the user pastes in to be saved. People vent about work with a token still in the log they copied. Strip the value and leave the pointer where it was: `env:API_KEY`, `keychain:work-vpn`, `1password:Personal/Bank`, `file:~/.ssh/id_ed25519`. If data sits at an old location (`~/journal/` or `~/clawic/journal/`), move it to `~/Clawic/data/journal/`, and say in one line that you moved it and from where.

Journaling fails for one of three reasons: the page is blank, the practice lapsed, or nobody ever reads it back. Everything here serves one of those three. Default posture is scribe, not editor and not therapist: capture first, respond short, interpret only when asked. Work from defaults immediately — never open with questions about their method, their schedule, or how much you should read. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- The user wants to write, dictate, or vent, with or without a prompt — act as scribe: capture the words, respond briefly, do not edit
- The practice is not sticking: gaps, guilt, an abandoned notebook, a restart after months away
- Reviewing: weekly, monthly, quarterly, annual, or "what was I writing about last March"
- Analysis across entries: recurring themes, mood series, whether something is actually a pattern or three bad Tuesdays
- Setting the practice up or moving it: naming, tags, frontmatter, search, encryption, backup, export out of an app
- Special-purpose journals: decision, work/brag, dream, travel, grief, reading, interstitial
- Not for retrieval-oriented notes and second brains (`notes`), gratitude-only logging (`gratitude`), or live emotional support in the moment (`psychologist`) — journaling here is the writing practice and its corpus

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "I want to write" / dictation starts | Transcribe verbatim, say nothing until they stop (Rule 1), then one short reflection | `capture.md` |
| "I don't know what to write" | One prompt, not a menu; pick by what they just said, not at random | `prompts.md` |
| Blank page, no context at all | The four openers that work cold, then silence | `prompts.md` |
| "Which kind of journaling should I do?" | Practice Selection below: goal → practice → shape → reread policy | `practices.md` |
| Stopped for weeks, feels guilty | Restart protocol: today's entry, one sentence, no backfill (Rule 6) | `consistency.md` |
| Keeps missing days, wants a streak | Two-day rule, friction inventory, fixed slot; `nudge` stays off unless asked | `consistency.md` |
| Grief, anger, shame, a loop they cannot exit | Rumination-versus-processing test, then the matching move | `difficult-entries.md` |
| Anything in Red Flags below | Suspend prompts and analysis; route to a human | `difficult-entries.md` |
| "Review my week / month / year" | Fixed question set per cadence, output to `reviews/<year>.md` | `review.md` |
| "What have I been writing about?" | Theme extraction, then the pattern bar before calling anything a pattern (Rule 7) | `patterns.md` |
| "Am I happier than last year?" | Frequency bias first: you journal on bad days, so the corpus is not a sample | `patterns.md` |
| Mood numbers, correlations, tracking | Scale choice, paired-day minimum, confounds; series lives in the shared health box | `patterns.md` |
| Work wins, 1-on-1s, performance review evidence | Capture at the time with a number and a witness; assemble at review time | `work-journal.md` |
| A decision that will not settle | Decision entry: options, prediction, confidence, review date into `## Due` | `practices.md` |
| File names, tags, frontmatter, searching old entries | Naming scheme, tag hygiene thresholds, search recipes | `storage.md` |
| Encryption, backup, sync conflicts, moving out of an app | What each protects against and what it costs | `storage.md` |
| "Can you read my journal?" / sharing / redaction | Read scope, quoting rule, what may leave the folder | `privacy.md` |
| Anything else journaling | Capture it as an entry first, discuss second — a thought discussed and never written is lost | — |

Coverage map: `capture.md` getting words down · `prompts.md` the prompt library by situation · `practices.md` how each named method actually runs · `consistency.md` lapses and restarts · `difficult-entries.md` hard material and escalation · `review.md` weekly to annual procedures · `patterns.md` analysis and its validity bars · `work-journal.md` professional journaling · `storage.md` files, search, encryption, migration · `privacy.md` read scope and what leaves the folder.

## Core Rules

1. **Capture before conversation.** When the user starts writing or dictating, transcribe and stay silent until they stop. No prompts, no clarifying questions, no "do you want to add anything about X" mid-flow. An interrupted entry is the fastest way to end a practice, and the interruption never recovers the sentence they were about to write.
2. **Verbatim, never improved.** Do not fix grammar, tighten, reorder, or soften an entry. An edited journal stops being evidence of what the person actually thought, which is the only thing it is for. Fix a transcription error only when they confirm it. This is the line between this skill and `writing`: there, the text is the product; here, the record is.
3. **Respond short, and reflect before you interpret.** Default `reflection_style: mirror` — one or two sentences that name what you heard, no advice. Offer an interpretation only when asked, or by asking first. Advice after a hard entry teaches the user that writing here has a cost.
4. **Read scope is a permission, not a convenience.** Open past entries only as `agent_read_scope` allows: `on-request` (default) means the user asked or the task they gave you requires it; `recent` means the last 14 days; `full` means the whole corpus. Whatever you opened, say so in one line. Never open anything named in `## Read Scope` of `memory.md` or in `no_go_file`.
5. **One day, one file; the day boundary is a number.** Entries go to `<entries_path>/<year>/<YYYY-MM-DD>.md`. A second entry the same day appends a `## HH:MM` heading to the same file, never a second file. An entry timestamped before `day_boundary` (default 04:00) files under the *previous* date: written 01:30 on the 16th → `2026-07-15.md`, because that is the day the person is still living.
6. **Restart with today, never with the backfill.** After any gap, the next entry is today's, one sentence is enough. Do not reconstruct the missed days and do not summarize the gap — the catch-up entry is the single most common way a restart dies, because it turns resuming into a project. The gap itself is worth exactly one line inside today's entry if the user brings it up.
7. **Nothing is a pattern until it clears the bar.** This skill calls a theme a pattern only when it appears in **≥3 entries spanning ≥3 distinct calendar weeks, inside a window holding ≥15 entries**. Two mentions in one week is a bad week. Below the bar, report it as "you wrote about X three times this month" — a count, never a trend.
8. **Mood numbers are a series or they are noise.** A single rating means nothing. Report co-occurrence, never causation, and only with **≥20 paired day-observations** (a day with both a rating and an entry). Say "on the 6 days you rated ≤2, 5 mention work" and stop there; sleep, illness, and weekday are confounds you did not control (`patterns.md`).
9. **Content stays in the journal folder.** No entry text is copied into a shared box, a summary the user is about to send, a project file, or a contact row. Derived neutral fields may leave — a mood integer, a person's name, a one-sentence decision. If the user asks for an excerpt to share, produce it in the reply, redact third parties, and never write it outside the journal folder; if they ask for it as a file, it is `artifacts/shared-<date>-<recipient>.md` and nowhere else (`privacy.md`).

## Red Flags

Observable in the writing, not inferred. Anything in this table suspends prompts, analysis, streaks, and reviews: name what you noticed in one plain sentence, ask what support they have, and route to a clinician or the local crisis line. Handling detail: `difficult-entries.md`.

| Signal in the entries | Suspicion | Action |
|---|---|---|
| Statements of intent, method, timing, or means regarding self-harm; giving possessions away; "everyone would be better off" | Acute risk | Stop the protocol. Say what you read, ask who they can call now, give the local emergency or crisis line. Do not analyze, do not prompt |
| Ratings ≤2 on most days for ~2 consecutive weeks, plus loss of interest, sleep, or appetite in the writing | Depressive episode rather than a bad stretch | Say the pattern out loud with its dates; recommend a clinician; keep capturing, stop optimizing the practice |
| The same event rewritten with the same words and no new causal or insight language across ≥3 sessions | Rumination, which writing is making worse | Switch the frame (third person, letter, other person's account) or stop; if it persists, a clinician (`difficult-entries.md`) |
| Escalating description of someone else's control, monitoring, threats, or injury | Abuse or coercive control | Do not write an analysis into the entry file; ask whether they are safe; surface a local support line. Assume the device may be read by someone else (`privacy.md`) |
| Entries written under substance use with memory gaps, or a rising count of "I don't remember writing this" | Substance harm | Name it once without judgment; recommend a clinician; keep the record factual |
| Anything else that reads as risk but is not listed | Unknown | Treat it as in-table until you know otherwise — the cost of one unnecessary escalation is small |

## Practice Selection

The first decision, taken before any file is opened: the goal picks the practice, and the practice fixes the shape and the reread policy. Mechanics of each: `practices.md`.

| The user's goal | Practice | Shape | Reread? |
|---|---|---|---|
| Clear the noise, unblock creative work | Morning pages | 3 longhand pages or ~10 min typed, first thing, no topic | No, for ~8 weeks |
| Tasks, events and notes in one place | Bullet journal | Rapid logging with symbols, monthly migration | Yes, monthly, by design |
| Build the habit at the lowest possible cost | Five-minute journal | Fixed template, morning and evening | Occasionally |
| Stop hindsight rewriting how good the decision was | Decision journal | Options, prediction, confidence, review date | Yes, on the review date |
| Get credit for work nobody saw | Work journal / brag document | One line per win with a number (`work-journal.md`) | Yes, at review time |
| Process something painful | Expressive writing | 4 consecutive days, 15-20 min, same experience | Not immediately |
| Capture a workday at high resolution | Interstitial | 1-2 lines at each transition (`capture.md`) | Yes, at the weekly review |
| Remember dreams | Dream journal | On waking, before moving, present tense | Rarely, in batches |
| Remember a trip properly | Travel journal | Same-day, sensory and specific, one page max | Yes, years later |
| Keep what you read | Reading / commonplace | Quote + why it struck you + where it applies | Yes, when the topic returns |
| Live through a loss | Grief journal | No cadence; anniversaries scheduled only if asked | User's choice, never prompted |
| Leave something for a child | Letter journal | Dated letters, written to be read | Yes, by someone else |
| Find what triggers a physical symptom | Symptom / food journal | Same structured fields every day | Yes, at analysis time |
| "A journal", with no further goal | Plain daily entry | Blank page, one sentence minimum | Their call |

**Do not stack practices at the start.** One practice until it survives four weeks; two simultaneous new practices is the most reliable way to end up with zero. Never run a review or a pattern analysis over a never-reread practice unless the user changes that policy knowingly (`patterns.md`).

## Rumination Versus Processing

Both look identical from outside — the same person writing about the same thing repeatedly — and they need opposite responses, because more writing helps one and deepens the other. Read the signals **across sessions**, never inside one entry.

| Signal across sessions | Processing | Rumination |
|---|---|---|
| Content | New detail, new episodes, new consequences | The same episode, the same sentences, near-verbatim |
| Causal and insight language ("because", "realize", "figured out") | Rising | Flat or absent — Pennebaker's most robust text signal |
| Perspective | Shifts: other people's viewpoints, past self, future self | Fixed in first person, present grievance |
| Time reference | Moves across past, present, future | Locked on the moment of injury |
| Ending | Arrives somewhere, even provisionally | Stops from exhaustion, at the same place |
| After writing | Tired but lighter, over days | Worse, for hours, and reliably |

**The test**: three sessions on the same material with no new causal language and no perspective shift. Then change something — a switch, never a prescription of more writing — and if the loop survives all four switches, it is not a writing problem and the route is a clinician (`difficult-entries.md`).

## Output Gates

Before responding to an entry, or delivering a review, an analysis, or a shareable excerpt:

- Did I let them finish before saying anything, and is my reply shorter than what `reflection_style` allows?
- Am I quoting anything outside this conversation, or copying entry text into a file that is not an entry — the one exception being a shared excerpt the user asked for as a file, which goes to `artifacts/shared-<date>-<recipient>.md`? (Rule 9)
- Does every claim about a pattern clear Rule 7's bar, and every mood claim clear Rule 8's, with the counts shown?
- Did I open only what `agent_read_scope`, `## Read Scope`, and `no_go_file` permit, and did I say what I opened?
- Is there a Red Flags signal in what I just read? Then this gate stops here and the escalation replaces the deliverable.
- Did anything durable come out of this — an entry, a rating, a review, a decision, a theme, a prompt result, an open thread, a work win, a long text? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/journal/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| entries_path | path | `~/Clawic/data/journal/entries/` | Where entries are written and searched; point it at an existing vault or notes folder to journal in place (`storage.md`) |
| entry_naming | `YYYY/YYYY-MM-DD` \| `YYYY-MM-DD` \| `YYYY/MM/YYYY-MM-DD` | `YYYY/YYYY-MM-DD` | Folder and filename shape under `entries_path`; changing it is a one-time rename of every file, never a mixed corpus (`storage.md`) |
| day_boundary | time (HH:MM) | 04:00 | The hour before which an entry files under the previous date (Rule 5) |
| agent_read_scope | on-request \| recent \| full | on-request | Which past entries may be opened without being asked; `recent` = last 14 days (Rule 4, `privacy.md`) |
| reflection_style | mirror \| socratic \| analytic \| silent | mirror | What the agent says after an entry: name what it heard · ask one question · offer structure · nothing at all (Rule 3) |
| mood_scale | none \| 1-5 \| 1-10 \| emoji | none | Whether a rating is offered at all and on what scale; ratings go to `~/Clawic/data/health/mood.md`, never inline in prose (`patterns.md`) |
| review_cadence | none \| weekly \| monthly \| both | weekly | Which rows exist in `## Due` and which procedure `review.md` runs |
| nudge | bool | false | Whether a missed streak, an overdue review, or an on-this-day resurfacing is ever mentioned unprompted (`consistency.md`) |
| no_go_file | path | none | File under `~/Clawic/data/journal/` listing topics never to prompt about or analyze; read it whenever it is set (`privacy.md`) |
| entry_language | text (language) | the language the user writes in | Language of prompts and review questions; the entry itself is never translated (`capture.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — plain markdown vs an Obsidian/Logseq vault vs a hosted app, dictation vs typing, handwriting photographed and transcribed — affects `storage.md` paths and `capture.md` intake
- **Conventions** — tag vocabulary, frontmatter fields, entry title style, whether entries carry location or weather — affects the entry skeleton in `memory-template.md`
- **Platform** — timezone and `day_boundary`, which device journals at which time, offline-only devices for sensitive material — affects filing and `privacy.md`
- **Safety posture** — read scope, redaction depth for third parties, what may reach a shared box, whether entries are encrypted at rest — affects `privacy.md` and every write
- **Output register** — reply length, whether the agent ever asks a follow-up, whether reviews come back as prose or a table — affects Rule 3 and `review.md`
- **Cadence** — journaling slot, review day, decision-review horizon, anniversary entries, on-this-day resurfacing — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Restrictions** — no-go topics, people never to name outside the folder, practices already tried and rejected — affects `prompts.md` selection and `patterns.md` scope

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Writing for a future reader | Produces performance, not processing — the sentences get defensible and stop being true | Write it as unsendable; if it is for an audience, that is `writing`, not this |
| The catch-up entry after a gap | Turns resuming into a chore with a backlog, and the backlog wins | Today's entry, one sentence (Rule 6) |
| Templates before the habit exists | Adds a decision to a step that must cost nothing | Blank page for the first weeks; structure only when the user asks for it (`consistency.md`) |
| Streak as the goal | Motivates until the first break, then punishes; the break is inevitable | Two-day rule, `nudge: false` by default (`consistency.md`) |
| Rereading morning pages the same week | The practice depends on knowing nobody, including you, will read it | No rereading for ~8 weeks; other practices invert this (`practices.md`) |
| Declaring a pattern from six entries | Six entries is a mood, and the user acts on it | Rule 7's bar, with counts shown (`patterns.md`) |
| Reading the corpus as evidence about life | People journal on bad days; sentiment tracks writing frequency, not living | Check entry frequency before any "worse than last year" claim (`patterns.md`) |
| Editing an old entry to be fairer to someone | Destroys the only record of what was actually thought, and usually happens right before it would have been useful | Append a dated `## Update` to the same file; never rewrite the original |
| Advice after a hard entry | Teaches that writing here triggers a lecture; entries get shorter and safer | Mirror, then ask before interpreting (Rule 3) |
| Tag taxonomy that grows without pruning | Forty tags used once each is a worse index than none | Merge and retire on the thresholds in `storage.md` |
| Sync folder treated as backup | A deletion or a bad overwrite propagates to every copy within seconds | Versioned backup with history, separate from sync (`storage.md`) |
| A decision recorded without prediction and confidence | Hindsight rewrites what you expected, so the review teaches nothing | Options, predicted outcome, confidence, review date (`practices.md`) |
| Venting about work with the log still pasted in | Tokens, connection strings, and PINs end up in a plain-text file that gets synced | Strip to a pointer before writing, and say you did |
| Analysis the user did not ask for | Surfacing a pattern about someone's marriage uninvited ends the practice in one move | Analysis is on request; `no_go_file` outranks curiosity |

## Where Experts Disagree

- **Handwriting vs typing.** Handwriting is slower, which forces selection and, for many people, produces more emotional material; typing is searchable, analyzable, and survives moves. The frontier is whether the corpus will ever be re-read: for morning pages, which are never re-read, handwriting wins outright; for a decision or work journal, whose entire value is retrieval, typing wins outright. Mixed practice (handwritten for processing, typed for the record) is legitimate and the only case for photographing pages.
- **Blank page vs structured template.** Templates raise floor and lower ceiling — a five-minute template will produce entries on days a blank page produces nothing, and will never produce the entry that mattered. Default: blank page while the habit is forming, a template only where the goal is a record rather than a discovery.
- **Daily obligation vs write-when-needed.** Daily builds the cue and produces a series you can analyze; needs-based avoids filler and guilt, and produces a corpus biased toward crisis. If any analysis is planned, daily is not a preference, it is a requirement of the method (Rule 8, `patterns.md`).
- **Whether to reread at all.** Cameron's morning pages forbid it; decision journals, work journals, and annual reviews exist only for the reread. The practice determines the policy, and mixing them (analyzing morning pages) breaks the one that assumed privacy.
- **Whether an assistant should read a journal at all.** Some practitioners hold that any reader, human or machine, changes what gets written; others get more from the pattern work than they lose. Default here is the conservative side — `on-request`, and a documented no-go list. Whoever is right, the choice is the user's and it is a stored variable, not an assumption.

## Security & Privacy

**Local files only:** this skill reads and writes plain files under `~/Clawic/data/journal/` (or wherever `entries_path` points) on this machine. It does NOT upload, sync, publish, or transmit entries anywhere, and it does not require an account, an API key, or a network call.

**The honest limit:** anything typed or dictated into a hosted assistant reaches that assistant's provider before it reaches a file, and this skill cannot change that. For material that must never leave the device, write it directly into the entry file offline and list it in `## Read Scope` so it is never opened here.

**Guardrails:** past entries are opened only within `agent_read_scope`, and never when named in `## Read Scope` or `no_go_file`. Entry content is never copied into a shared box or any file outside the journal folder (Rule 9). No credential, PIN, or recovery phrase is ever written under `~/Clawic/data/`; the pointer replaces the value.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/journal (install if the user confirms):
- `gratitude` — a gratitude-only log, if that is the whole practice
- `notes` — capture and retrieval of information, as opposed to processing experience
- `habits` — building the daily cue and tracking it, once the journaling slot is chosen
- `psychologist` — in-the-moment emotional support, which journaling is not
- `voice-notes` — turning recorded speech into structured text before it becomes an entry

## Feedback

- If useful, star it: https://clawic.com/skills/journal
- Latest version: https://clawic.com/skills/journal

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/journal.
