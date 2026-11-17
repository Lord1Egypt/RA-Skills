# Capture — Getting the Words Down

Scope: the moment between "I want to write" and a saved file. Everything that costs time here is time the practice does not survive.

**Contents:** [The Scribe Protocol](#the-scribe-protocol) · [Intake Modes](#intake-modes) · [Filing an Entry](#filing-an-entry) · [What Goes Inside an Entry](#what-goes-inside-an-entry) · [Freewriting Mechanics](#freewriting-mechanics) · [When They Stop Mid-Sentence](#when-they-stop-mid-sentence) · [Interstitial Capture](#interstitial-capture) · [Reply Registers](#reply-registers)

**Before capturing**, read `## Practice` and `## Open Threads` in `~/Clawic/data/journal/memory.md` — the open threads are the only thing worth a single sentence of context before they start, and only if they raise it. Do not read past entries to "get context": that is `agent_read_scope` territory (`privacy.md`).

## The Scribe Protocol

1. **Silence until they stop.** No prompts, no "tell me more", no clarifying question, no acknowledgement between paragraphs. Rule 1 exists because the sentence they were mid-way through does not come back.
2. **Transcribe exactly.** Typos, fragments, repetition, profanity, and the sentence that contradicts the previous one all stay. Rule 2.
3. **Stop signal.** They stop when they say so, or after ~20 seconds of silence in dictation, or on an empty line plus "done"/"that's it". Do not infer a stop from a pause after a hard sentence — that pause is usually the entry's real content arriving.
4. **File it, then reply.** Write the file first (Filing an Entry below), so a lost connection or a closed window costs nothing. Then reply, in the register `reflection_style` sets.
5. **One line of receipt.** "Saved to 2026-07-26.md." Nothing more about the mechanics.

## Intake Modes

| Mode | What changes | Handling |
|---|---|---|
| Typed into the chat | Nothing | Verbatim to the file, including their line breaks |
| Dictated / speech-to-text | Transcript has run-on sentences, no punctuation, homophone errors | Insert sentence breaks and paragraph breaks only. Never rephrase. Flag words you could not make out as `[?]` in place rather than guessing |
| Recorded audio the user provides | The recording is the original | Transcribe, save the entry, and note the audio filename in the entry's frontmatter — do not move or delete the audio |
| Handwritten page, photographed | OCR errors cluster on proper nouns and numbers | Transcribe, mark uncertain tokens `[?]`, keep the image alongside as `entries/<year>/<date>-page1.jpg` and reference it from the entry |
| Pasted from another app | Carries the other app's markup, timestamps, and sometimes credentials | Strip markup to plain markdown; strip every secret to a pointer before writing (`privacy.md`) |
| Spoken while walking, fragments over several minutes | Arrives as many short messages | Buffer them into one entry, in order, blank line between fragments. Do not save six files |

Dictation is the highest-yield mode for people who cannot start typing: speech has no backspace, which is the same mechanism that makes freewriting work.

## Filing an Entry

- Path: `<entries_path>/<year>/<YYYY-MM-DD>.md`, per `entry_naming`.
- **Day boundary** (Rule 5): timestamp before `day_boundary` (default 04:00) files under the previous date. 01:30 on the 16th → `2026-07-15.md`.
- **Second entry, same day**: append `## HH:MM` and the text to the existing file. Never a second file, never overwrite. If the file has no `## HH:MM` heading yet, add one above the existing text using its own time first, so the day reads in order.
- **A day file already open in another editor**: append anyway and say so; the collision is resolved by concatenation, never by choosing a side (`storage.md`).
- Create the year folder if missing. Never create empty day files in advance for a month — an empty file reads as a missed day forever.

Entry skeleton and frontmatter fields: `memory-template.md`. Frontmatter is optional and stays optional until the user asks for tags or mood.

## What Goes Inside an Entry

- The user's words. That is the whole file, in the default case.
- **Your interpretation never goes in the entry file.** Reflections, patterns, and summaries go in the reply, or in `reviews/<year>.md` when they were asked for. The entry is the person's record of what they thought, and an assistant's paragraph inside it contaminates every later analysis.
- A correction the user makes later is a dated `## Update` appended to the same file, never an edit to the original text (Traps).
- Attachments (a photo, an audio file, a screenshot) live next to the entry with the same date prefix and are referenced by filename.

## Freewriting Mechanics

The rules that make timed freewriting produce material rather than a to-do list:

- **Do not stop the hand.** If nothing comes, write "I don't know what to write" until something does. The repetition is what breaks the block; the block is an editing reflex, not an absence of content.
- **No going back.** No rereading the previous paragraph, no correcting a word. Editing while generating is what turns the output into performance (Traps).
- **A fixed length, not a fixed quality.** Cameron's morning pages specify three longhand pages; a 10-minute timer is the typed equivalent. Length, not goodness, is the completion condition — that is precisely what removes the judgment.
- **The last two minutes are where it turns.** The predictable material comes out first. If the user regularly stops early, extend the timer rather than adding prompts.

## When They Stop Mid-Sentence

| Signal | What it usually is | Move |
|---|---|---|
| Trails off at a name | Approaching something they are not sure they want written | Say nothing for 10 seconds; then "want to keep going, or leave it there?" — both answers are fine |
| "I don't know how to say it" | Searching for a frame, not for words | "Say it badly first" — that sentence unblocks more often than any prompt |
| Stops and asks you a question | Wants to leave the entry and start a conversation | Answer in one line, then "want that in the entry, or keep it out?" |
| Goes quiet after a hard disclosure | Waiting to see what you do with it | Mirror one sentence, no advice, no question (Rule 3). Check Red Flags in SKILL.md |
| Stops and starts editing what they wrote | The reflex Rule 2 protects against | Save what exists; edits go in an `## Update`, not over the text |
| Anything else | Unknown | Wait. Silence costs nothing and interruption costs the entry |

## Interstitial Capture

Timestamped micro-entries between tasks, one or two lines each: what just finished, what is next, and what is in the way. Named and popularized by Tony Stubblebine as interstitial journaling.

- Format: `## HH:MM` then two lines. Appends into the same day file, so it merges with any longer entry that day.
- It is the only practice that survives a workday, because it costs under 30 seconds and rides an existing transition.
- Value is downstream: a day of interstitials is the highest-resolution input the weekly review will ever get (`review.md`), and the "what is in the way" line is where the same blocker becomes visible three times.

## Reply Registers

What the agent says after the entry is saved, set by `reflection_style`:

| Style | Reply shape | Length |
|---|---|---|
| `mirror` (default) | Name what you heard, in their own terms, without adding a frame | 1-2 sentences |
| `socratic` | Mirror, then one open question they have not already answered | 1 sentence + 1 question |
| `analytic` | Mirror, then a structural observation (a tension, a repeated word, a decision hiding in it) | 2-3 sentences |
| `silent` | Receipt only | The filename |

Never: advice, reassurance that dismisses ("I'm sure it will be fine"), a reframe they did not ask for, or a comparison to a past entry they have not authorized you to open (Rule 4).

**After capture, write in the same turn:** the entry file itself; a mood rating to `~/Clawic/data/health/mood.md` if the user gave one; `## Practice` in `memory.md` (last entry date, streak, usual slot); `## Open Threads` if they flagged something to come back to; and `## Read Scope` if they said not to reread this one. Destinations and formats: `memory-template.md`.
