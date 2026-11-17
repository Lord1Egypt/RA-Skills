# Introductions — Both Directions

An introduction spends the connector's credibility on both sides at once. Done well it is the highest-leverage thing an address book produces; done badly it costs two relationships to save one email.

**Read both records before proposing anything** — `## Details`, `do not raise`, and `## Groups` for whether they already know each other — and **read `do-not-surface.md`**, which suppresses a person as an introduction target as much as a contact target.

**Contents:** [Double Opt-In](#double-opt-in) · [The Forwardable Blurb](#the-forwardable-blurb) · [The Intro Message Itself](#the-intro-message-itself) · [When Someone Asks The User For An Intro](#when-someone-asks-the-user-for-an-intro) · [Being Introduced](#being-introduced) · [Tracking It To Landing](#tracking-it-to-landing) · [Introductions Not To Make](#introductions-not-to-make)

## Double Opt-In

The rule: **ask the receiving side first, privately, with an easy no.** Never connect two people in a single message without permission from at least the person being asked for their time.

1. Message the receiver alone. Say who, why them specifically, what is being asked, and how long it would take.
2. Include the forwardable blurb so they can decide on evidence rather than on trust in the connector.
3. Make declining costless and unembarrassing: "no is completely fine, and I won't mention it." Then honor that — an unexplained silence back to the requester is the correct outcome of a no.
4. Only after a yes, send the connecting message.

Cost of skipping it: the receiver's time is spent without consent, the requester gets an unenthusiastic response, and the connector is the one who looks careless. The one exception is two friends of equal standing in an obviously symmetric context — a dinner invitation, two people who both asked to meet.

## The Forwardable Blurb

Written by the **requester**, not the connector, and this is the part almost everyone gets wrong. A connector who writes it is doing the requester's work and will write it worse.

The blurb is two to four sentences, written to be forwarded verbatim:

- Who they are, in the terms that matter to the receiver.
- The specific reason it is *this* person, not a category of person.
- The concrete ask, with its size: "twenty minutes", "one question about pricing", "an opinion on the deck".
- One line of credibility that is checkable.

Anything private, anything about the receiver, and anything the requester would not want the receiver to read stays out — the blurb goes to its subject by default. A blurb worth reusing becomes `artifacts/blurb-<name>.md`, and it is written and stored as if the subject will read it, because they will (`memory-template.md`).

## The Intro Message Itself

Once both sides have agreed:

- **Both names in the first line**, each described in one clause, using how each would describe themselves.
- **Why this connection exists**, in one sentence. The reason is what makes it not a cold email.
- **Hand off explicitly**: name who owns the next move. "Ines, over to you." An introduction with no named owner dies in the mutual politeness of waiting.
- **Then leave.** The connector drops off the thread after the handoff; staying makes every subsequent message a performance for an audience.
- Match the channel each side prefers. An email intro to someone who lives in messaging is a slow no.

## When Someone Asks The User For An Intro

| Situation | Response |
|---|---|
| Good fit, the user knows the target well | Ask the requester for the blurb, run the double opt-in, connect |
| Good fit, but the user barely knows the target | Say so honestly and offer the weak version: "I can mention you, but we've met twice" — a weak intro presented as strong burns the target's trust |
| Bad fit, or the target would find it a waste | Decline directly, name the reason, offer an alternative person if one exists. Passing along a bad intro to avoid an awkward no is how connectors stop being trusted |
| The user does not know what the ask is | Ask for the blurb first. The request usually clarifies itself, or evaporates |
| The requester has burned a previous intro | Do not make another. Note it on their record, factually and dated (`details.md`) |
| The target is on `do-not-surface.md` | No, without explanation, and no alternative naming them |
| Repeated requests from the same person | Look at the record: three intros requested and none reciprocated is a pattern worth seeing before the fourth (`network.md`) |
| Anything else | Default to double opt-in; it resolves most of these on its own |

## Being Introduced

- **Reply within 24 hours**, moving the connector to bcc in the same message. Leaving them on the thread makes them witness every scheduling exchange.
- **Thank the connector separately**, and this is the part that gets skipped — the connector spent credibility and hears nothing about whether it worked.
- **Close the loop with the outcome**, weeks later: what came of it. A connector who never learns the outcome introduces less next time, and the record should hold why.
- If the intro was declined or went nowhere, tell the connector that too, briefly and without blame.

## Tracking It To Landing

Every introduction is an open loop from the moment it is proposed until it lands or is closed, with a name and a date (`memory-template.md`).

| State | What it looks like | Next action |
|---|---|---|
| Requested | Someone asked; no blurb yet | Ask for the blurb; drop after two weeks of no blurb |
| Opt-in pending | Receiver asked, not answered | One reminder at 5 days, then treat silence as a no and say so kindly to the requester |
| Connected | Intro sent | Nothing for two weeks |
| Stalled | Two weeks, no thread activity | One nudge to the side that owed the move; then close |
| Landed | They met or exchanged substantively | Close the loop; log on both records; keep the blurb if it is reusable |
| Declined | Receiver said no | Close silently; never tell the requester who declined or why |

Loops older than 60 days surface at the roster review and are either chased once or dropped explicitly (`hygiene.md`). An introduction that quietly evaporates is worse than a decline, because both sides remember it as unfinished.

## Introductions Not To Make

- Anyone the user cannot honestly describe. If the description would require inflation, the intro is a liability.
- Two people whose only commonality is a category ("you both work in design").
- Anyone who has been asked and said no, until circumstances visibly change.
- Across a rupture — two people who fell out, or an ex and a current partner — even when the context looks unrelated.
- On behalf of someone the user would not vouch for. An introduction is a vouch, whatever the wording says.
- To a person on `do-not-surface.md`, in any form and for any reason (SKILL.md Rule 7).

**Write in the same turn**: the introduction as a line in `## Open Loops` in `~/Clawic/data/people/memory.md` with both names, direction and date; a log entry on both records when it lands (`interactions.md`); a reusable blurb to `~/Clawic/data/people/artifacts/blurb-<name>.md` with its `## Boxes` line; and a burned or declined intro as a dated fact on the relevant record — factual, never a verdict (`details.md`).
