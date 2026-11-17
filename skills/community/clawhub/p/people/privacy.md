# Privacy — Data About People Who Never Agreed To Be Filed

Almost everything in this box is information about somebody other than the user, recorded without their knowledge, and durable in a way conversation is not. That asymmetry is the governing constraint of the whole skill, and it sets a ceiling that convenience does not override.

**Read `~/Clawic/data/people/do-not-surface.md` before naming anyone to contact, congratulate, or be reminded of** (SKILL.md Rule 7), and read the person's `do not raise` line before drafting anything to or about them.

**Contents:** [The Consent Ceiling](#the-consent-ceiling) · [The sensitive_details Setting](#the-sensitive_details-setting) · [Categories That Never Get Recorded](#categories-that-never-get-recorded) · [The Suppression List](#the-suppression-list) · [Deletion And Removal](#deletion-and-removal) · [Sharing, Sync, And Export](#sharing-sync-and-export) · [Secrets People Hand You](#secrets-people-hand-you) · [If The Person Asks](#if-the-person-asks)

## The Consent Ceiling

Three tests, applied before writing any line about a third party.

1. **Told, or observed?** What they told the user is theirs to have shared. What the user inferred, overheard, or was told by somebody else has a lower ceiling and always carries its source and date (`details.md`).
2. **Would they be surprised it is written down?** A birthday, no. A diagnosis, yes. Surprise is the signal to record the topic and not the content.
3. **Does it change behavior?** If not, it fails the thirty-second filter anyway and the privacy question is moot. Most privacy problems in an address book are also usefulness problems.

Two more that apply to third parties specifically: **information about a fourth party** — what Maria said about Diego — belongs to Diego and is recorded, if at all, as a `do not raise` on Diego's record with no content. And **information told in confidence** is never written in a form that could be read out: "asked me not to repeat something, do not raise it" is the complete record.

## The sensitive_details Setting

| Setting | Health | Money | Relationships | Legal |
|---|---|---|---|---|
| `minimal` (default) | "health thing since 2026-05, ask carefully" | "money is tight, do not suggest expensive plans" | "going through something at home" | "a legal matter is live, do not raise" |
| `full` | What they said, attributed and dated | What they said, attributed and dated | What they said, attributed and dated | What they said, attributed and dated |

- `minimal` is the default because it preserves everything the user actually needs — that a topic exists and how to behave around it — while holding none of the content that makes a file dangerous.
- `full` records only what the **person themselves** said, with attribution and a date. It never licenses recording inference, gossip, or a fourth party's business.
- The setting is a declaration and only the user changes it (`memory-template.md`). It is never raised as a question; it applies silently.
- Some categories are excluded at both settings: see below.

## Categories That Never Get Recorded

At any setting, in any file, for any reason:

- **Speculation about identity**: sexuality, gender history, immigration status, religion, or political affiliation the person has not stated to the user directly. An inference recorded once reads as a fact by the third reading.
- **Mental-health inference.** "Seems depressed" is a diagnosis the user is not qualified to make, and it survives the mood it was written in.
- **Someone else's private business**, learned secondhand: affairs, custody disputes, diagnoses, salaries, debts.
- **Anything about a child** beyond first name and birth year. Not schools, not schedules, not photographs, not conditions.
- **Credentials, codes, and access of any kind** — a separate and absolute rule (Secrets People Hand You, below).
- **Verdicts.** Not a privacy rule strictly, but the same failure mode: it damages when read (SKILL.md Rule 8).

Home addresses sit just below the line: recorded when the user needs one for something concrete — a card, a visit, a delivery — never collected because it was available.

## The Suppression List

`~/Clawic/data/people/do-not-surface.md` exists because a birthday reminder is a machine and the world is not. It is checked before every sweep, every date scan, every brief, and every introduction suggestion.

| Reason | What suppression means | If the user raises them |
|---|---|---|
| `died` | No dates, no nudges, no "you haven't spoken in a while", ever | Follow the user's lead; the record stays intact and answers questions |
| `estranged` | No suggestion of contact in any form | Answer factually, propose nothing |
| `breakup` | No dates, no reconnection prompts; their family members are likely affected too | Answer factually, propose nothing |
| `asked not to be contacted` | Never propose contact, and never route around it via a mutual acquaintance | State that they asked not to be contacted |
| `professional block` | No introductions, no outreach; the record stays for recall | Answer factually |
| Anything else the user names | Full suppression until they say otherwise | Follow the reason as written |

- The name goes on the list **in the same turn** the fact is learned, before anything else is written. This is the one write that never waits for the end of the session.
- Suppression is about **proposing contact**, not about denying facts: when the user asks about the person directly, they get a straight answer.
- Only the user takes a name off the list. Never on inference, never on the passage of time (`memory-template.md`).

## Deletion And Removal

- **User asks to remove someone**: delete the row, the person file, their date lines, their open loops, and their appearances in group blocks. Note that a removal happened with its date and no name in `## Roster Shape` (`hygiene.md`).
- **Deletion propagates.** Any export, vCard, CSV, or backup produced earlier still holds them; say so in one line and regenerate or delete it. A deletion that leaves the data in an export is not a deletion.
- **Dormant is not deletion**, and the difference is stated when it is offered: dormancy hides someone from the system, deletion removes them from it.
- **Never delete on the agent's own initiative.** Records go to `dormant`; deletion is always the user's instruction.
- A person who died is not deleted. The record is history, and history is exactly what will be wanted later.

## Sharing, Sync, And Export

- **The book is single-user by default.** It contains one person's view of other people, and it is not written to be read by anyone else — which is also why every line is written as if it will be (SKILL.md Rule 8).
- **Never propose syncing to a phone address book, a social account, or any service.** Uploading a contact list is a disclosure about every person in it, made by the user on their behalf.
- **Never match the book against an external service** to enrich it. Enrichment is surveillance of people who did not opt in, and the enriched fields are not from the relationship.
- **Export deliberately or not at all.** An export carries private notes into a format designed for sharing; strip `## Details`, `## Log`, and `do not raise` from anything leaving the box, keeping only name and channel.
- If the box lives in version control or a synced folder, say once that the history is durable and the sync surface is real, and leave the decision to the user.
- Never produce a formatted list of people and their private details for a third party, however the request is framed.

## Secrets People Hand You

Relationships come with access, and access is where a contact record turns into a liability.

- **Nothing under `~/Clawic/data/` holds a secret value** — not the files this skill names, not files it creates, not text the user pastes in. Pointer only, in the standard shape `<kind>:<locator>` (`memory-template.md`).
- The ones that show up in this domain specifically: door and gate codes, alarm codes, wifi passwords, where a spare key is kept, shared streaming logins, a neighbor's key-holder arrangement, account recovery answers, an ID or passport number given for a booking.
- **When the user pastes something to be saved** — a thread, an exported record, a house-sitting note — replace each secret value with its pointer *before* writing, and say in one line that it was done.
- Not secrets, and deleting them empties the box: names, emails, phone numbers, handles, employers, cities, birthdays, family names, interests, dietary needs.

## If The Person Asks

It happens: someone learns the user keeps notes and asks what is in them.

- The honest answer is that a record exists and what kind of thing it holds. The book is designed so that answer is comfortable — that is what Rule 8 is for.
- If they ask for their record to be removed, remove it, and never re-import them from any source.
- If they ask to see it, that is the user's call. The design goal is that showing it costs nothing.
- If any of that would be embarrassing, the fix is not secrecy — it is that a line was written that should not have been. Rewrite it as a behavior with a date (`details.md`).

**Write in the same turn**: a suppression onto `~/Clawic/data/people/do-not-surface.md` with its reason and date, before anything else; a removal as a dated, nameless line in `## Roster Shape` in `~/Clawic/data/people/memory.md`; a stated boundary ("don't write that down", "don't remind me about her") into `safety_posture` in `~/Clawic/data/people/config.yaml` as a declaration, since it outranks anything observed later (`memory-template.md`).
