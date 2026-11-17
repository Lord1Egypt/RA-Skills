# Keeping In Touch — Cadence, Drift, And The Reconnection

Relationships end by decay far more often than by rupture, and decay is invisible: nobody notices the message that was not sent. Cadence exists to make the invisible countable.

**Read `~/Clawic/data/contacts/contacts.md` for `Last contact` and tier before any sweep**, and **read `~/Clawic/data/people/do-not-surface.md` before naming a single person** (SKILL.md Rule 7).

**Contents:** [The Overdue Sweep](#the-overdue-sweep) · [Reading The Signal Behind A Gap](#reading-the-signal-behind-a-gap) · [The Reconnection Message](#the-reconnection-message) · [Worked Reconnections](#worked-reconnections) · [Gap Length Changes The Message](#gap-length-changes-the-message) · [When Not To Reconnect](#when-not-to-reconnect) · [Keeping The Warm Ones Warm](#keeping-the-warm-ones-warm)

## The Overdue Sweep

Runs weekly by default, or on request; output obeys `nudge_style`.

1. For each person: `overdue = today − Last contact > cadence`, where cadence is the per-person `cadence` if set, otherwise the tier default (SKILL.md, Relationship Tiers).
2. Drop everyone on `do-not-surface.md`. Drop `orbit` and `dormant` entirely — orbit people are for recall, not for outreach.
3. Drop anyone with an open loop that is theirs to close: chasing is a different move from reconnecting, and doing both in one message reads as a chase (`network.md`).
4. Rank by **relationship value at risk**, not by gap length: an `inner` person at 9 weeks outranks a `regular` at 14 months.
5. Surface **at most three**, each with the one line of context that makes a message writable. A list of ten names produces zero messages.
6. A person surfaced and not acted on is not surfaced again next week. Twice is a nudge; three times is nagging, and nagging is how the whole system gets turned off.

`inner`-tier silence is treated as information, not as a task: eight weeks without contact with someone in the support clique usually means something happened to one of the two people, and the right move is a question, not a scheduled catch-up.

## Reading The Signal Behind A Gap

Not every gap is neglect, and the wrong reading produces the wrong message.

| Pattern | Likely meaning | Move |
|---|---|---|
| Both sides went quiet at once | Ordinary drift; life got loud for both | Straight reconnection, no apology needed |
| User stopped replying | The user's backlog, not the relationship | Reconnect and acknowledge in one clause, then move on |
| They stopped replying, after being reliable | Something changed for them, often not about the user | One low-cost message with no ask; then stop |
| They reply late and briefly, consistently | The relationship has resettled at a lower tier | Change the tier, not the frequency |
| Gap started right after a specific event | Something happened | Check the log for the last entry before the silence, then decide |
| They see the user in group settings but never one-to-one | It is a group friendship, and that is a valid resting state | Set tier `orbit`, cadence none |
| Gap after the user asked for something | The ask landed badly, or went unanswered and is now awkward | Release them explicitly: close the loop, ask for nothing |
| Anything else | Unknown | Default to the straight reconnection below |

## The Reconnection Message

Four rules, in order of how often they are broken.

1. **Ask for nothing in the first message.** A reconnection carrying a favor is a transaction, and it is remembered as one — for years (SKILL.md Traps).
2. **Lead with the specific remembered thing.** The whole point of a record is that this message can start with "did you ever get to Kalymnos" instead of "how have you been". The second question is unanswerable and gets no reply.
3. **Name the gap in one clause, then stop.** "Long overdue on my side —" is complete. A paragraph of apology transfers the discomfort to them and asks them to absolve it.
4. **Make replying cheap.** One question, answerable in a sentence, with no scheduling in it. "Coffee sometime?" turns a reply into a calendar negotiation; "are you still in Berlin?" does not.

Do not explain the absence, do not summarize two years of the user's life, and do not open with what the user needs. Length is the tell: a good reconnection message is three to five lines.

## Worked Reconnections

**14 months, a former colleague.**
Weak: `Hey! It's been forever, sorry I've been terrible at keeping in touch. How are you? We should catch up properly sometime — are you around for a coffee in the next few weeks?`
Strong: `Long overdue on my side. I saw the piece about the platform migration and thought of the mess we inherited in 2024 — did the new team finish it? Still in Berlin?`
The strong version proves the record exists, gives one answerable question, and asks for nothing.

**Three years, a friend who moved abroad.**
Weak: `Happy new year! Hope you're doing well!`
Strong: `Thinking about you — Sofia must be starting school around now. How is Lisbon treating you three years in?`
Specific, computed from the record, and it invites the update they actually want to give.

**Six months, someone who stopped replying.**
Weak: a second message chasing the first.
Strong: `No reply needed — just saw the climbing gym opened near you and remembered you were waiting for it. Hope things are good.`
A gift with no hook. If it goes unanswered, the tier moves to `orbit` and the sweep stops raising them.

## Gap Length Changes The Message

| Gap | What the message must do | What it must not do |
|---|---|---|
| Under 3 months | Nothing special; continue the last thread | Treat it as a reconnection — it is just a message |
| 3-12 months | Reference the specific thing, one clause on the gap | Apologize at length |
| 1-3 years | Update in one line, then a question about them | Summarize the user's life |
| 3+ years | Establish that the memory is real and warm; expect no reply | Assume the relationship resumes where it stopped |
| After a known bad event on their side | Acknowledge it plainly and offer something concrete | Pretend not to know, or ask how they are "coping" |
| After a fallout | See When Not To Reconnect | Reconnect as though nothing happened |

## When Not To Reconnect

- Anyone on `do-not-surface.md`. This is absolute, and the reason is stored so the handling matches (`privacy.md`).
- When the only reason is that the user needs something. That is a favor request, and it is handled honestly as one: acknowledge the gap, state the ask, and accept the answer (`network.md`).
- Immediately after a fallout, on the reasoning that time will have fixed it. What repairs a rupture is addressing it, not a casual message that requires the other person to decide alone whether it is being addressed.
- When the person has said no. A single unanswered message is ambiguous; two are not.
- When the relationship has ended for a good reason. Some people leave the roster, and `dormant` exists so the history is kept without the system suggesting a message every quarter.

## Keeping The Warm Ones Warm

Maintenance is cheaper than repair, and it does not look like maintenance.

- **Send the thing, not the check-in.** An article, a photo, a job posting, a link to the venue they mentioned — anything that proves the memory is active. It requires no reply, which is why it works.
- **React to what they publish**, but never count it as contact (`interactions.md`).
- **Be specific in the low-effort moments.** A birthday message with a real reference is worth more than a scheduled quarterly coffee, and costs a fraction.
- **Answer within the week.** A reply that arrives a month later teaches the other person to lower their expectations, which is how a `regular` becomes an `orbit` without anybody deciding it.
- **Set a per-person `cadence` for the relationships that only survive with effort** — the long-distance friend, the mentor — and leave everyone else to the tier default.

**Write in the same turn**: the sweep's run date into `## Due` in `~/Clawic/data/people/memory.md`; any message actually sent updates `Last contact` in `~/Clawic/data/contacts/contacts.md` and gets a log line (`interactions.md`); a tier or `cadence` change goes on the person's record; a decision to stop reaching out goes on the record as `dormant`, or on `do-not-surface.md` if the user asks for it (`memory-template.md`).
