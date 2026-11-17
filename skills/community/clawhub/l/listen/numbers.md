# Numbers — Digits, Times, Money, and Spoken Addresses

Numbers are the highest-stakes repair class: they gate bookings, payments, counts, and schedules, and STT errors on them are phonetically systematic. Default routing: any number that feeds an action gets echoed as digits (SKILL.md Rule 6, tunable via `number_echo`).

## The Seven -teen/-ty Pairs

The canonical STT number confusion — final-syllable stress is all that separates them, and stress dies first in noisy audio:

13/30 · 14/40 · 15/50 · 16/60 · 17/70 · 18/80 · 19/90

- Echo format: digits plus spelled digits — "15 (one five)". The parenthetical disambiguates in one read; the user corrects with one word.
- Context bounds beat confirmation: "book a table for 40" at a restaurant is almost certainly 14; "40 servers" in a fleet of 50 is plausible. Confirm only when both readings survive the context check.

## Digit Homophones

"to/too → 2", "for → 4", "ate → 8", "won → 1", "oh → 0". Two-way trap: the engine also writes digits where the user meant the word — "I want 2 go". Repair direction follows sentence role: preposition slot → word; quantity slot → digit.

## Times and Dates

| Signal | Risk | Play |
|---|---|---|
| "eight thirty" | Written as "830", "8 30", or "8:30" inconsistently | Normalize to HH:MM; carry am/pm from context (meeting hours default to daytime) |
| Missing am/pm | 12-hour ambiguity on bookings | Echo with meridiem: "8:30pm" — user corrects in one word |
| "half eight" | UK English = 8:30; German-influenced speakers mean 7:30 ("halb acht") | If `languages` includes German/Dutch/Scandinavian, confirm; otherwise read as 8:30 |
| "the third" vs "the 3rd" vs "3" | Ordinal day vs count | Sentence role decides; echo full date ("March 3") when it gates scheduling |
| "next Friday" | Not an STT error — a human ambiguity | Echo the resolved date, same one-word-correction principle |
| Month/day order | "three four" → 3/4 vs 4/3 | Echo as month-name form; never emit ambiguous numeric dates in replies |

## Money and Magnitudes

- "fifteen hundred" = 1,500 — engines sometimes emit "15 100". Rejoin before interpreting.
- "one point five million" vs "1.5 M" vs "$1,500,000" — normalize to one form and echo it when the amount gates anything.
- "two to four" (range) vs "224" — a fused number where the sentence needs a range is a segmentation error; re-split.
- Currency words ("euros", "bucks", "quid") survive transcription well; the symbol placement is yours. Read `~/Clawic/profile.yaml` currency as fallback if the user's currency is unstated.

## Phone Numbers, IDs, and Codes

- "oh" = 0 inside digit strings; "double five" = 55; "triple seven" = 777.
- Grouped read-out ("five five five... one two one two") arrives with arbitrary spacing — strip to a single digit string, then format by the ID's known shape (phone, ticket number, OTP).
- Mixed alphanumerics ("a b 1 2") are the worst STT class: letters collide with words ("bee", "are", "you"). Echo the reassembled code character by character, and prefer asking the user to type codes that gate authentication — voice is the wrong channel for OTPs.

## Emails and URLs

Spoken addresses arrive as prose: "john dot smith at gmail dot com".

- Reassemble: "at" → @, "dot" → ., "dash"/"hyphen" → -, "underscore" → _, "plus" → +.
- Lowercase the result; engines capitalize name-like tokens ("John.Smith@...") but addresses are conventionally lowercase.
- "dub dub dub" / "w w w" → www. Protocol is yours to add.
- Echo every reassembled address before using it as a recipient — a wrong recipient is the single most expensive repair miss in this skill (`actions.md`).
- Known-contact shortcut: if the reassembled address is skeleton-close to a stored contact, offer the contact (Rule 2), not the raw reassembly.

## Versions and Code Numbers

- "three eleven" in a Python sentence → 3.11, not 311. Dotted-version shape wins when the noun is a runtime, package, or release.
- "two x" → 2x (multiplier) in performance talk; "v two" → v2 in release talk.
- Port numbers arrive fused or split ("eighty eighty" → 8080); well-known ports (80, 443, 5432, 8080) are the candidate pool.

## Output Gate for This File

Any number that feeds a booking, payment, recipient, quantity, or schedule appears in your reply as normalized digits — once, in the sentence where you use it, not as a separate verification paragraph.
