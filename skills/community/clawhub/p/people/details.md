# Details — What Is Worth Recording

The value of a record is not how much it holds; it is the ratio of lines that change behavior to lines that do not. A record where every line matters gets read. A record where one line in twenty matters gets skimmed once and abandoned.

**Read the person's existing record before adding a detail**: half of what sounds new is already there in different words, and duplicated facts in different phrasings are how a record starts contradicting itself.

**Contents:** [The Thirty-Second Filter](#the-thirty-second-filter) · [The Catalog Of What Pays](#the-catalog-of-what-pays) · [What Never Goes In](#what-never-goes-in) · [Facts, Not Verdicts](#facts-not-verdicts) · [Secondhand And Inferred](#secondhand-and-inferred) · [Detail Decay](#detail-decay) · [Where A Detail Lives](#where-a-detail-lives)

## The Thirty-Second Filter

Before writing anything: **would this change the first thirty seconds of the next conversation?**

| Candidate line | Verdict | Why |
|---|---|---|
| "Her father had surgery in March" | Keep | The first question next time, and getting it wrong is worse than not asking |
| "Works at Acme" | Keep once, as role | Answers "who do I know at Acme"; re-verify at the roster review |
| "Nice person, good chat" | Drop | True of everyone worth a record; carries zero routing information |
| "Doesn't drink" | Keep | Changes where you suggest meeting, permanently |
| "Wearing a blue jacket" | Drop | Not repeatable, and appearance notes read badly when the file is seen |
| "Wants to move to Kalymnos and climb for a year" | Keep | The specific thing; the reconnection message writes itself from this line |
| "Said the roadmap was a mess" | Keep as a topic, not a quote | Their words about their employer are theirs; store that the subject is live |
| "Her salary is 90k" | Drop (or `full` only) | Third-party financial detail; the topic existing is enough at `minimal` |
| "Replies within a day on WhatsApp, never on email" | Keep | Sets the preferred channel, which decides whether messages are read at all |
| "Talked about the weather" | Drop | If nothing survived the filter, the interaction gets a date and no content |

A record with three lines that all pass is stronger than one with thirty where four do. When in doubt, the drop is cheap: the detail will come up again if it matters, and it will come up in a version that is more current.

## The Catalog Of What Pays

The recurring categories, with what each one buys.

| Category | What to store | What it buys |
|---|---|---|
| Household | Partner's name, children's names with birth years, pets by name | Never asking "and how's your wife?" about an ex; ages compute, never store an age |
| Work shape | Role, who they report to or are, what they actually own | Whether they can decide the thing you might need decided |
| The live thing | The project, worry, or plan they were animated about, with its date | The specific opener that proves you listened |
| Constraints | Dietary, alcohol, allergies, mobility, religious observance | Choosing a venue without a round of questions |
| Channel | Preferred channel, response pattern, timezone, hours they read | Messages that arrive at a readable moment |
| Origins and geography | Where they are from, where they live, where they have lived | Answers "who do I know in Berlin"; grounds small talk in something real |
| Interests | The two or three they actually pursue, not everything they mentioned | Sending the article that gets a reply, and the whole basis of `gifts` |
| How you connect | Who introduced you, mutual friends, groups you share | Routing an introduction, and knowing who not to gossip to |
| Do not raise | The topic that reliably goes badly, with why in four words | The single most valuable line in any record |
| Reciprocity | What they have done for you and what you owe | Kept as open loops, never as a balance (`network.md`) |
| Their kids' ages, in years | Never — store birth years | An age is wrong within twelve months and nobody remembers to fix it |

## What Never Goes In

Three categories that stay out regardless of how useful they would be, because the cost of the file being read by anybody else is asymmetric:

1. **Medical detail about a third party.** At `sensitive_details: minimal` the record holds "health thing going on, ask carefully, since 2026-05" and never the diagnosis. At `full` it holds what they themselves said, attributed and dated.
2. **What they told you about someone else's private life.** Affairs, diagnoses, finances, custody. If it must be kept because it prevents a disaster at the next dinner party, it goes as a `do not raise` line on the person it concerns, with no content.
3. **Anything the user is only speculating about.** Sexuality, immigration status, mental health, whether they are being pushed out. An inference recorded once becomes a fact by the third reading.

Also out: opinions the user holds about the person's worth, appearance, or competence (Facts, Not Verdicts, below), and any credential or code they mentioned in passing (`memory-template.md`).

## Facts, Not Verdicts

Every line is written as if the person will read it, because the file gets synced, restored, screen-shared, and eventually inherited.

| Verdict | Fact that carries the same information |
|---|---|
| "Flaky" | "Cancelled the last three plans, same week each time" |
| "Cheap" | "Splits to the cent; suggest venues accordingly" |
| "Difficult" | "Reacts badly to changes announced late; give notice" |
| "Boring" | "One shared subject: cycling. Keep it there" |
| "Doesn't like me" | "Replies to group threads, not to direct messages" |
| "Networking with me" | "Contacts before their fundraises, 2024 and 2026" |

The fact version is more useful anyway: it survives the mood it was written in, it dates, and it tells the next reader what to do.

## Secondhand And Inferred

- Secondhand facts carry **source and date**: `heard from Luis, 2026-05: looking to move back to Madrid`. Without the attribution, a rumor is indistinguishable in six months from something the person said themselves, and the user acts on it in front of them.
- A secondhand fact is never used as the opener of a conversation. It is context for interpreting what the person says, and nothing else.
- Inferences are labeled as inferences or dropped. "Seemed uncomfortable about the reorg" is an observation with a date; "was pushed out" is a conclusion the user does not have.
- When the person later states the thing directly, the secondhand line is **replaced** by the firsthand one, not stacked underneath it.

## Detail Decay

Facts have half-lives, and a stale one is worse than an absent one because it is used with confidence.

| Detail | Typically stable | Recheck trigger |
|---|---|---|
| Name, how you met, origin | Permanent | A name change (`names.md`) |
| Children's names and birth years | Permanent | New child |
| Dietary and alcohol constraints | Years | They mention a change |
| Employer, role, city | ~2 years | Any interaction; roster review flags records untouched for a year |
| Partner | Years, and the failure mode is severe | Any hint; never assume a partner still exists |
| The live thing | Weeks to months | Every interaction — it is the field most worth overwriting |
| Contact channel and address | ~2 years | A bounce, or no reply on a channel that used to work (`hygiene.md`) |

The roster review pass rechecks the decaying rows rather than the whole book (`hygiene.md`), and the rule for the partner row is asymmetric on purpose: asking about a partner who has left is one of the few errors a record can cause that is worse than having no record.

**Write in the same turn**: every detail that passed the filter into the person's record — their `Context` line in `~/Clawic/data/contacts/contacts.md` while they are one row, or `## Details` in `~/Clawic/data/contacts/<name>.md` once they have a file, which is triggered at the seventh detail. A replaced fact is overwritten, never appended below the old one (`memory-template.md`).
