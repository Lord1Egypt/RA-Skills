# Capture — The First Twenty-Four Hours

Everything a relationship can become depends on a record that exists. The window is short: a name heard once and not written survives about a day, and the specific detail that makes a reconnection possible survives less than that.

**Before capturing anyone**, read `~/Clawic/data/contacts/contacts.md` — a meaningful share of "new" people are already there from a previous life, and a second row for the same person is the failure that takes longest to notice.

**Contents:** [The Five Fields](#the-five-fields) · [Capture In The Moment](#capture-in-the-moment) · [Capture Modes By Context](#capture-modes-by-context) · [What Counts As Worth Keeping](#what-counts-as-worth-keeping) · [Batch Capture After An Event](#batch-capture-after-an-event) · [The Follow-Up That Makes The Record Real](#the-follow-up-that-makes-the-record-real)

## The Five Fields

Written within 24 hours, in this order of importance. A record with fields one through three is useful; a record with all five is durable.

1. **Name as they say it** — including the form they used to introduce themselves. "Alexandra" who said "Sasha" is filed as Sasha with Alexandra as the formal name (`names.md`).
2. **Where and when** — the event, the room, the mutual context. This is what the other person will also remember, which makes it the safest opener two years later.
3. **Who introduced you** — the connector is half the context, and reconnection often routes through them.
4. **One specific thing** — the thing they were animated about, the problem they have, the plan they described. Not their job title; the title is on their profile and carries no signal that you were listening.
5. **What was agreed** — "send her the article", "he'll intro me to his CTO", or nothing. If anything was agreed, it is an open loop with a date before it is anything else (`memory-template.md`).

Missing the email or handle is survivable — the row's `Key` falls back to `<kebab-name>` plus a stable disambiguator and is upgraded when a channel appears; missing field four means you met somebody and kept a business card.

## Capture In The Moment

- Capture the **name** and **one specific thing** immediately after the conversation ends, not at the end of the day. Six conversations blur into three by the taxi home.
- Two words are enough at the point of capture: `sasha — kalymnos`. Expansion happens at the desk. The failure is never that the note was too short, it is that no note was made.
- Never capture during the conversation itself, and never ask someone to spell their name into a device while they are talking. Repeat the name back instead (`names.md`), which does the same job and reads as attention.
- If the user hands over a stack of cards, a photo of a badge, or a screenshot of a chat, the capture job is to extract the five fields and discard the artifact. A photo of a business card is not a contact record; it is a contact record you have not made yet.

## Capture Modes By Context

| Context | What is actually available | Capture priority | Common miss |
|---|---|---|---|
| Conference or meetup | Badge name, employer, the talk they liked | Field 4 — everyone captures the employer, nobody captures the interest | Their real name differs from the badge (`names.md`) |
| Introduced by a friend | The connector's framing | Field 3 and what the connector said about them | Recording the connector's opinion as fact — attribute it (`privacy.md`) |
| A meeting for work | Role, company, the decision they own | Who they defer to, and their preferred channel | Filing them as a role; roles change and the person stays |
| Neighbor, school gate, gym | Faces and first names only | A physical anchor: which door, which class, which slot | No email ever appears — the key is `<kebab-name>` plus the anchor |
| Online, a reply that started a thread | Handle and platform | The platform, because the handle is worthless without it | Handle collision across platforms; store `platform:handle` |
| Reconnection with someone from the past | Everything you already knew, aged | What changed, before it disappears under the catch-up | Overwriting the old context instead of appending to it |
| Someone else's plus-one, at a wedding or dinner | A first name and their relationship to a person you know | Whose plus-one, in `## Groups` | A record with no way back to who they were with |
| Anyone else | Whatever was said | Fields 1, 2 and 4 | Waiting for a "complete" record before writing anything |

## What Counts As Worth Keeping

Not everyone met becomes a record. The test is whether either sentence is true:

- **You would recognize their name in six months and want context.** Then they are at minimum `orbit`.
- **Something was agreed.** Then they are a record regardless of tier, because an open loop needs somebody to attach to.

Everyone else does not get a record, and that is the correct outcome. A roster that captures every person in every room is the same as no roster: the signal is gone and the user stops reading it. When in doubt, `orbit` with one line costs almost nothing and is trivially promoted; a bulk sweep of a badge scanner is not (`hygiene.md`).

## Batch Capture After An Event

A conference, a wedding, or an offsite produces a batch, and the batch has a decay curve steeper than any single meeting.

1. Same evening: names plus one word each, straight into a single list.
2. Within 48 hours: expand into rows. Each person gets tier and field 4; anyone with an agreement gets an open loop with a date.
3. Anyone who does not clear the "worth keeping" test is dropped now, not filed.
4. The event itself becomes an artifact — `artifacts/debrief-<event>-<year>.md` — holding who was met, why they matter and the next step, with `Done` columns. The person rows live in the address book; the debrief keeps only the event context (`memory-template.md`).
5. The debrief is read before the next edition of the same event, which is when it pays for itself: arriving already knowing who to find is the entire value of having attended before.

## The Follow-Up That Makes The Record Real

A record without a first follow-up decays into trivia. The follow-up is a message within 48 hours that references field 4 and delivers whatever was agreed, and it is short — the second contact is what converts a met person into someone who will reply in a year, and length is not what does it.

If nothing was agreed and nothing is owed, no message is sent. A follow-up with nothing in it is worse than silence, because it spends the one thing you had.

**Write in the same turn**: the person's row into `~/Clawic/data/contacts/contacts.md` with its `Key` filled in — email, handle, or `<kebab-name>` plus a stable disambiguator, never left blank, because that row is the only place a one-row person's key exists — `Last contact` set to the day you met, their tier, and anything agreed into `## Open Loops` in `~/Clawic/data/people/memory.md`. A batch from an event also writes its debrief to `~/Clawic/data/people/artifacts/` with its `## Boxes` line. Formats and thresholds: `memory-template.md`.
