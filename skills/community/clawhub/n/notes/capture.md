# Capture — Inbox, Dumps, Transcripts, Voice

Raw input arrives faster than structure. This file covers the moment between "the user said something worth keeping" and "a note exists that someone can find".

**Contents:** [The Capture Rule](#the-capture-rule) · [Quick Capture](#quick-capture) · [Splitting a Dump](#splitting-a-dump) · [Transcripts and Voice](#transcripts-and-voice) · [Screenshots, Links, Attachments](#screenshots-links-attachments) · [Inbox Triage](#inbox-triage) · [Capture Traps](#capture-traps)

**Before capturing**, read `## Conventions` and `## Note Map` in `~/Clawic/data/notes/memory.md` — the tag vocabulary and the inbox location are already decided, and a second convention invented now costs a merge later.

## The Capture Rule

Capture is optimized for latency, not for quality. The cost of a badly shaped note is a minute of cleanup; the cost of a missed capture is total.

- **Never block capture on a decision.** Type unknown, project unknown, tag unknown → it goes to `quick/` with a claim title and today's date. Classification is a triage job (7 days, SKILL.md Rule 8), not a capture job.
- **The claim, not the topic, even at capture speed.** "Sarah: they will not renew unless SSO ships by Q4" takes the same three seconds as "Sarah call" and is still findable in March.
- **Timestamp on quick captures, date only on everything else.** Two captures on the same day about the same subject collide on filename otherwise: `2026-07-26_14-30_call-sarah.md`.
- **Never rewrite a capture into prose at capture time.** Fragments with the right nouns beat sentences with the wrong ones.

## Quick Capture

Minimal shape. Everything optional here is genuinely optional.

```markdown
---
date: 2026-07-26 14:30
type: quick
tags: [renewal]
---

# Sarah: no renewal without SSO by Q4

Called about the renewal. SSO is the blocker, not price.
Mentioned a competitor already has it.

Actions:
- [ ] @me: check the SSO roadmap date — 2026-07-29
```

- One claim per capture. Two unrelated things in one capture means neither is findable by its own subject — split at capture, it is cheaper than at triage.
- A capture with an action goes to `actions.md` in the same turn, even before it is triaged; a commitment that waits for triage is a commitment that is missed.
- A capture that is really a question with no owner goes to `## Open Threads` in `memory.md`, not to `quick/`.

## Splitting a Dump

A pasted email thread, a Slack export, a long voice dump: the input is a *source*, the note is what you extract from it.

Extraction order — run it top to bottom, stop when the input is exhausted:

1. **Decisions.** Anything of the form "we're going with", "let's do", "approved". Each becomes a decision note (`decisions.md`) or a decision line in the meeting note.
2. **Commitments.** "I'll", "can you", "by Friday". Each becomes a row in `actions.md` with owner, verb, absolute date (SKILL.md Rule 4).
3. **Facts with a shelf life.** Numbers, dates, names, versions, prices. These are why the note gets reopened.
4. **Open questions.** Anything unresolved with a person attached → `## Open Threads`.
5. **Everything else.** Discard. If the user insists on keeping the raw text, it goes to `artifacts/<kebab-name>.md` as a source and the note links to it — never inline in the note, where it destroys the signal-to-noise of every future search.

Ratio check: a 4,000-word thread that produces a 40-line note is normal. A 4,000-word thread that produces a 3,000-word note means step 5 was skipped.

## Transcripts and Voice

Machine transcripts arrive with three defects: no speaker discipline, no paragraph structure, and confident errors on names and numbers.

| Defect | What it costs | Handling |
|---|---|---|
| Names transcribed phonetically | The note is unfindable by person and `contacts.md` gets a garbage key | Reconcile every name against `contacts.md` before writing; flag any you cannot resolve as `@unknown-1` rather than guessing |
| Numbers and dates misheard | The one thing that gets quoted later is wrong | Any figure that drives a decision is marked `(verify)` unless the user confirmed it in the same conversation |
| No speaker attribution on the decisive line | "We decided" with no decider — worthless in three months | Attribute decisions and commitments or mark them `attribution unclear`; never assign to the most likely person |
| Filler and repetition, 90%+ of the text | Buries the content | Rule 3 applies to transcripts too: ≤20% survives |

- **Keep the transcript, do not become it.** Raw transcript to `artifacts/transcript-<kebab-name>.md`, the note links to it. The transcript is evidence; the note is the product.
- **A transcript is not consent.** If the user pastes a recording of other people, `sensitive.md` decides whether it can be stored at all before any of this runs.
- **Dictated notes carry secrets more often than typed ones**: bridge PINs, passwords read aloud, card numbers. Strip to pointers before writing (`memory-template.md`).

## Screenshots, Links, Attachments

- **A link with no claim is a bookmark, and bookmarks are never revisited.** Capture the URL *and* one line of why it matters; without that line the note is a URL nobody will open.
- **Attachments break portability.** Local markdown: store the file next to the note in `<type>/attachments/` and link relatively, so a copy of the folder still works. Apple Notes and Evernote hold attachments the CLI cannot reach (`apple-notes.md`, `evernote.md`) — a note whose content is an attachment there is effectively unsearchable from outside the app.
- **Screenshots of text are the worst format available**: not searchable, not diffable, not quotable. Transcribe the three lines that matter into the note and keep the image as an attachment only if the layout is the point.

## Inbox Triage

Runs every 7 days (SKILL.md Rule 8), or whenever `quick/` passes 20 files, whichever comes first. Its `## Due` row is `Inbox triage (quick/)`.

For each capture, exactly one of four outcomes:

| Outcome | When | What happens |
|---|---|---|
| Promote | It is a meeting, decision, project or research note in disguise | Rewrite into the typed shape, move to that folder, delete the capture |
| Fold | It adds to an existing note | Append with its date, delete the capture |
| Keep | It is a standalone claim worth its own file | Give it a real type and tags, move out of `quick/` |
| Delete | It has not been touched in 30 days and no action came out of it | Delete it, and say how many were deleted |

Nothing stays in `quick/` after triage. An item that survives two triages untouched is a delete, not a keep — that is the whole signal.

**After triage**, update `## Status` (`corpus` count) in `memory.md`, the `Inbox triage` row in `## Due`, and `index.md` if it exists.

## Capture Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Asking which folder before writing anything | The user loses the thought while answering | Capture to `quick/`, classify at triage |
| One running "inbox.md" file | Grows to hundreds of lines, cannot be moved or deleted per item, and its edits conflict on every sync | One file per capture |
| Capturing the conversation instead of the claim | The note reads like a chat log and answers nothing | Extraction order above |
| Titling a capture "Notes" or "Call" | Two of them collide and neither is findable | Claim title, always (SKILL.md Rule 2) |
| Leaving the transcript as the note | Nobody rereads 6,000 words, including the person who recorded them | Transcript to `artifacts/`, note links to it |
| Trusting a transcript's numbers | Transcription errors on figures are common and silent | Mark `(verify)` unless confirmed live |

**Write triggers for this file** — in the same turn, no ceremony: the capture itself to `~/Clawic/data/notes/quick/<date>_<time>_<slug>.md`; any commitment found in it to `actions.md`; an unresolved question to `## Open Threads` in `memory.md`; a raw transcript or pasted source to `artifacts/transcript-<kebab-name>.md` with its `## Boxes` line; the triage run to the `## Due` row and the updated `corpus` count in `## Status`. Formats and thresholds: `memory-template.md`.
