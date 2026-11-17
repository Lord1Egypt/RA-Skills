# Names — Getting The One Thing Right

A name is the only field where being wrong is itself the insult. Everything else in a record can be incomplete without cost.

**Read the person's record before writing or saying their name**: the preferred form and the pronunciation are stored fields, not something to re-derive. If the record has neither, the next conversation is the chance to capture them.

**Contents:** [Recall At The Moment Of Introduction](#recall-at-the-moment-of-introduction) · [Preferred Form Beats Legal Form](#preferred-form-beats-legal-form) · [Pronunciation As A Stored Field](#pronunciation-as-a-stored-field) · [Name Orders Across Cultures](#name-orders-across-cultures) · [Name Changes](#name-changes) · [Filing And Disambiguation](#filing-and-disambiguation) · [Recovering From Getting It Wrong](#recovering-from-getting-it-wrong)

## Recall At The Moment Of Introduction

Names are lost at encoding, not at storage: most people never actually hear the name because they are preparing what to say next. Four moves, in the order they apply:

1. **Say it back inside the first sentence.** "Sasha — good to meet you." This is the single highest-yield move and it is free; it also surfaces a mispronunciation immediately, while correcting it is still cheap.
2. **Ask at the moment of the miss, not later.** "Sorry, I lost your name" in the first minute is normal. The same sentence in the fortieth minute is a small wound. The window is roughly the first exchange.
3. **Attach the name to something they said**, not to their appearance. Appearance changes and the association is often unrepeatable in polite company; "Sasha who climbs" survives a haircut.
4. **Use it once more before leaving.** Retrieval, not repetition, is what fixes it — one recall at the end of the conversation beats saying it five times in the first minute.

For a room to be worked rather than a single introduction, capture in waves: names only in the moment, one word each afterwards (`capture.md`).

## Preferred Form Beats Legal Form

Store both when they differ, and use the preferred one everywhere including the file name.

| Situation | Store | Use |
|---|---|---|
| Introduces as a short form ("Sasha" for Aleksandra) | Both, marked | The short form, always, until they use the long one |
| Uses a Western name alongside a name in another script ("Coco" / 王雪) | Both, with the script | Whichever they used with the user; never substitute one for the other in an introduction |
| Has a title that is part of how they are addressed (Dr, Prof, Rev, Sir) | The title as a field | In first contact and in writing; drop it when they drop it |
| Uses a middle name as their name | The full legal form once, then the used name | The used name, and file under it |
| Changed their name (marriage, divorce, transition, migration) | The current name, plus a hidden alias for search | The current name, exclusively (see Name Changes) |
| Pronouns stated or in their signature | The pronouns as a field | Consistently, in drafts and briefs alike |
| Two people in the roster share a name | The disambiguator, in the key, never in the display name | The plain name when talking to the user |

An "alias" field exists for one purpose: search hits when the user types the old or the formal version. It is never used in output.

## Pronunciation As A Stored Field

Write the pronunciation the way the user will read it aloud under pressure, not in a phonetic alphabet nobody parses in a hallway: `MAH-ree-a`, `zhoo-LEE-eta`, `Ng — the g is silent`. Capitalize the stressed syllable. Where the user's own language lacks a sound, store the nearest workable approximation plus one word of instruction, since a plausible attempt lands well and a phonetically perfect attempt is not the goal.

Capture it the first time it is heard from the person themselves. Do not infer pronunciation from spelling: the same spelling is pronounced differently by different families, and the only authority on a name is its owner.

## Name Orders Across Cultures

Order errors are systematic, not random, which means they repeat forever once encoded wrong. Store the **family name explicitly** rather than trusting position.

- **Hungarian, Japanese, Chinese, Korean, Vietnamese and others** conventionally place the family name first in their own context; many people reorder it in international settings and some do not. Whichever order they used when introducing themselves is the one to store and mirror.
- **Spanish and Portuguese naming** carries two family names (paternal and maternal in Spanish; frequently reversed in Portuguese). The everyday form usually uses the first of them in Spanish and the last in Portuguese — store the full form and the everyday form separately.
- **Patronymics** (Icelandic `-son`/`-dóttir`, East Slavic middle names, Arabic `bin`/`bint`) are not surnames and do not sort or address like one; Icelanders are addressed by given name including formally.
- **Mononyms** exist and are complete names. A record forced to invent a surname produces mail addressed to a person who does not exist.
- Honorifics that are grammatically attached (`-san`, `-ssi`) are context, not part of the name, and are never stored inside the name field.

When the order is unknown and it matters — an introduction, a written address — use the form they used themselves and nothing else. Guessing produces the exact error that signals inattention.

## Name Changes

A name change is a rename, never a new record: the interaction history is the asset and it is attached to the old row.

1. Update the display name to the new one everywhere.
2. Keep the previous name in the alias field, so search still finds them.
3. Keep the identity key unchanged if it is an email that still works; if the email changed too, follow the merge order in `hygiene.md`.
4. Rename the person file to the new name and fix the pointer in `contacts.md` in the same turn — a stale pointer orphans the entire history.
5. For a transition, the previous name is stored for search only and never appears in output, drafts, briefs, or file names; if the user asks for it to be removed entirely, remove it, and lose the search hit rather than argue.
6. Note the change and its date in `## Roster Shape`, so a later import that still carries the old name is recognized as a duplicate and not as a new person.

## Filing And Disambiguation

- File name is `<kebab of the used name>.md`, following `name_order`.
- A collision takes a **stable** disambiguator, not a counter: their employer, their city, or how the user knows them — `john-smith-acme`, `john-smith-climbing`. Counters (`john-smith-2`) tell the reader nothing and reassign themselves the day one record is deleted.
- The disambiguator lives in the key and the file name, never in the name shown to the user, who knows perfectly well which John they mean.
- Two records that turn out to be one person: merge (`hygiene.md`). One record that turns out to be two people: split, giving the older interactions to whichever person the context proves owns them, and marking the ambiguous ones as unattributed rather than assigning them by guess.

## Recovering From Getting It Wrong

- Caught in the moment: correct and move on in the same breath, without a paragraph of apology. The apology is what makes it memorable.
- Discovered later: use the right form from then on and say nothing. A message that exists only to apologize for a misspelling asks the other person to manage the user's discomfort.
- Repeat offense on the same person: it is a record failure, not a memory failure. The pronunciation and preferred form belong in the record where the brief will surface them (`briefing.md`).

**Write in the same turn**: the used name, formal name, alias, pronunciation, pronouns, and family-name position into the person's record — their row in `~/Clawic/data/contacts/contacts.md`, or the header of `~/Clawic/data/contacts/<name>.md` once they have a file. A rename also updates the file name, the row pointer, and a dated line in `## Roster Shape` of `~/Clawic/data/people/memory.md` (`memory-template.md`).
