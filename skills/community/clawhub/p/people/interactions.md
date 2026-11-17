# Interactions — Logging So It Is Readable In A Year

The log is what turns an address book into memory. It is also the section that most often kills a system, because a log written as a transcript stops being read within a month, and a log that is never read stops being written.

**Read the person's `## Log` before writing a new entry** — the last entry usually contains the thread the new one continues, and continuing it is the whole point.

**Contents:** [What Counts As An Interaction](#what-counts-as-an-interaction) · [The Shape Of An Entry](#the-shape-of-an-entry) · [Worked Examples](#worked-examples) · [Last Contact Is Not The Log](#last-contact-is-not-the-log) · [Group Interactions](#group-interactions) · [Compression Over Time](#compression-over-time) · [What Not To Log](#what-not-to-log)

## What Counts As An Interaction

An interaction is a **two-way exchange between the user and the person**. That is the whole definition, and it exists to keep `Last contact` honest.

| Event | Interaction? | Effect |
|---|---|---|
| Coffee, lunch, a call, a video call | Yes | Log entry plus `Last contact` |
| A text thread that got a reply, however short | Yes | `Last contact`; log entry only if something survived the filter |
| An email sent that got no reply | No | Note as an open loop if a reply is expected; `Last contact` unchanged |
| Liking or commenting on their post | No | Nothing. This is the most common way a `Last contact` date becomes fiction |
| Reading about them, or thinking of them | No | Nothing |
| A group dinner where you spoke to them | Yes | Log entry on their record, plus a line in `## Groups` if the group is recurring |
| A group dinner where you did not speak to them | No | Nothing on their record |
| They replied to a mass message or a birthday wish | Yes, weakly | `Last contact` updated, no log entry |
| An introduction the user made where both replied | Yes, for both | `Last contact` for both, and the open loop closes (`introductions.md`) |

## The Shape Of An Entry

One to two lines, reverse chronological, and always in this order:

`YYYY-MM-DD` · **what it was** (three words) · **what changed** (one sentence) · **next step**, if any.

- **What changed** is the whole entry. Not what was discussed — what is now different, or newly known, or decided. "Talked about her job" is not an entry; "leaving Acme in September, has not told her team" is.
- **Next step** is written only if it exists, and if it exists it also gets a line in `## Open Loops` with a date. An intention living only inside a log entry is not tracked (`memory-template.md`).
- Two lines is the ceiling. `log_max_lines` in `config.yaml` can raise it, but the ceiling is the reason the log is still being read next year.
- Where the interaction produced a durable fact about the person rather than an event, the fact goes to `## Details` and the log entry just points at it: the log is chronology, `## Details` is state (`details.md`).

## Worked Examples

Bad, then good, for the three most common cases.

**A catch-up call.**
Bad: `2026-04-02 — Long call with Maria, we talked about the kids, her job, the holidays in Greece, and my move. She seems well.`
Good: `2026-04-02 call — Sofia started school; her father's anniversary in January was hard. Wants to hear about the move when it's done.`
The second is shorter and answers what the first cannot: what to open with, and what to be careful about.

**A short text exchange.**
Bad: no entry, and `Last contact` untouched, because "it was only a text".
Good: `Last contact: 2026-07-02`, no log entry. The date is the fact; there was no content to keep.

**A first business meeting.**
Bad: `2026-05-11 — Meeting with the vendor. They presented. Good meeting.`
Good: `2026-05-11 first meeting — owns the integration budget, defers to Priya on timing. Sending the security doc by Friday.` Plus `## Open Loops`: security doc, by 2026-05-15.

## Last Contact Is Not The Log

`Last contact` is a single date on the row and the entire overdue mechanism runs on it (SKILL.md Rule 4). Three failure modes to avoid:

- **Aspirational updates.** Drafting a message is not contact. The date moves when the exchange happened.
- **Backfilling with the log's newest entry.** If the log has gaps, the date is the last *known* contact; write `unknown` rather than a plausible date. A confident wrong date silences the sweep for months.
- **Letting the log grow while the date rots.** They are updated together or not at all. A record with a July log entry and a March `Last contact` is a record nobody has trusted since March.

## Group Interactions

- Each person present gets their own `Last contact` update; the log entry goes on whoever the conversation was actually with.
- The event itself, if it recurs, is a block in `## Groups` — who attends, and who does not know whom. That last line is what prevents an introduction that should not be made and a plus-one invitation that should not be sent.
- A one-off gathering large enough to be worth remembering is an artifact debrief instead, with the people rows written into the address book in the same turn (`capture.md`).
- Never write the same log entry onto five records. One entry on the person it concerns, plus a group line, keeps the address book from turning into five copies of one evening.

## Compression Over Time

The log is the only section that grows without limit, and it needs a stated policy or it silently becomes the largest thing in the box.

1. Entries stay verbatim for **two years**.
2. Past ~40 entries, or past two years, older entries move to `## Earlier` at the bottom of the person file and compress to **one line per year**: `2023 — three meetings, worked together on the migration; she left in November.`
3. What survives compression: relationships formed, jobs changed, moves, losses, and anything that still explains a current fact. What does not: individual coffees.
4. Compression is never deletion of the person's `## Details` — state is preserved in full, only chronology is thinned.

## What Not To Log

- Anything that failed the thirty-second filter (`details.md`).
- The user's feelings about the interaction. "Felt awkward" is not durable and reads badly later; if something concrete happened, record the concrete thing.
- Verbatim quotes of the person criticizing a third party. Record that the subject is sensitive, not the sentence.
- Anything the person asked to be kept between you. If it is important enough to need remembering, the record holds "asked me not to repeat something about X — do not raise it" and nothing more (`privacy.md`).

**Write in the same turn**: `Last contact` in the person's row in `~/Clawic/data/contacts/contacts.md`, the entry at the top of `## Log` in `~/Clawic/data/contacts/<name>.md` — creating that file if this is their second logged interaction — any durable fact into `## Details`, and any next step into `## Open Loops` in `~/Clawic/data/people/memory.md` with its date (`memory-template.md`).
