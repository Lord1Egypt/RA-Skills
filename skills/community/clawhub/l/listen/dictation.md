# Dictation — Producing Artifacts from Voice

Conversing and dictating are different contracts. In conversation you repair to understand; in dictation you are the user's typewriter — the output is their words, and every edit needs a rule. Mode is set by `dictation_mode` (default cleaned).

## Detecting Dictation Mode

Explicit: "take an email", "write this down", "draft a message saying...". Implicit: a monologue with artifact structure (salutation, body, sign-off) inside a message that opened with a compose verb. When ambiguous, produce the artifact — a user who wanted conversation says so in one word; a user whose dictation got summarized has to re-dictate.

## Spoken Punctuation and Formatting Commands

In dictation, these are commands; in conversation, literal words (SKILL.md Quick Reference):

| Spoken | Emit |
|---|---|
| period / full stop | . |
| comma | , |
| question mark / exclamation point | ? / ! |
| new line | line break |
| new paragraph | paragraph break |
| open quote ... close quote | "..." |
| open paren ... close paren | (...) |
| colon / semicolon | : / ; |
| dash | — or - by context |
| all caps ... end caps | UPPERCASE span |
| bullet / next bullet | list item |

Literal-word escape: "the word period" or a sentence where the token is clearly content ("we ended the trial period") — sentence role decides, same as digit homophones.

## Self-Correction Phrases

The user edits aloud. Apply the edit; never keep both versions in cleaned mode:

| Phrase | Semantics |
|---|---|
| "scratch that" / "delete that" | Remove the previous clause or sentence |
| "no wait" / "actually" + restatement | Replace the previous phrase with the restatement |
| "I mean X" right after Y | Replace Y with X |
| "make that X" after a number or name | Replace the last number/name with X |
| "start over" | Discard the artifact body, keep the task |

The correction target is the nearest prior span of the same type (number replaces number, name replaces name, clause replaces clause). When the target is ambiguous, keep the later version and mark the edit point for review.

## Cleaned vs Verbatim

- **cleaned** (default): strip disfluencies ("um", "uh", "you know", false starts), apply self-corrections, add punctuation and paragraphs, keep the user's vocabulary and register untouched. Cleaning is transcription hygiene, not editing: never upgrade word choice, never restructure their argument.
- **verbatim**: every word as transcribed, including disfluencies and both sides of self-corrections. For quoted testimony, exact-words requests, and when the user says "exactly what I say".

## Sentence Segmentation

Run-on transcripts need boundaries. Split at: discourse markers ("so", "anyway", "and then") starting a new intent · subject changes · spoken punctuation. Paragraph at topic shifts and before sign-offs. Wrong segmentation is recoverable; a 200-word unbroken block is not readable.

## Marking Uncertain Tokens

Repaired-but-unconfirmed tokens inside an artifact get marked, because unmarked edits change what the user said (SKILL.md Traps):

> Meet at the Kowalski(?) offices at 8:30

One marker style, used sparingly — a draft with five (?) markers means the transcript was too degraded to draft from; route to `degraded.md` behavior instead (quote your reading, get a yes/no, then draft).

## Read-Back Before Release

An artifact that will be sent (email, message) gets a one-line read-back of the action-gating fields only — recipient, amounts, dates — not the full body. "Sending to sara@acme.com (one recipient), meeting moved to 8:30pm — go?" The body was theirs; the routing is yours to verify (`actions.md`).
