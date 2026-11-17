# Decisions — Who Decides, How, And Where It Is Written

**Before any decision meeting, and before anyone reopens anything**, read `~/Clawic/data/meetings/decisions.md` — the log answers "was this already decided, by whom, and what did we reject" faster than the room can reconstruct it. Read `decision_method` in `config.yaml` for the house default, and `## Series` for whether this decision belongs to an existing body.

**Contents:** [Set The Method First](#set-the-method-first) · [The Four Methods](#the-four-methods) · [Reversibility Decides The Rigor](#reversibility-decides-the-rigor) · [Forcing A Decision](#forcing-a-decision) · [Disagree And Commit](#disagree-and-commit) · [The Decision Log](#the-decision-log) · [Reopening](#reopening)

## Set The Method First

The most common reason a meeting ends with "let's take it offline" is that nobody said who decides. Announce it in the first 60 seconds, before any argument (`facilitation.md`), because after the debate every method looks partisan.

Two checks before the discussion starts:

- **Is the decider in the room?** If not, this meeting produces a recommendation, so say that out loud and design for it — recommendation meetings are shorter and rarely need eight people.
- **Does the decider have the authority the decision needs?** Money above a threshold, headcount, legal commitments and customer promises usually sit somewhere else. A room that decides beyond its authority produces a decision that gets quietly reversed and a team that stops trusting decisions.

## The Four Methods

| Method | Who decides | Best for | Cost |
|---|---|---|---|
| **Owner-decides after input** | One named person, after hearing everyone | Most decisions; the default | Fast and clear; feels arbitrary if the input is not visibly used |
| **DACI** | The **D**river runs it, the **A**pprover decides, **C**ontributors inform, **I**nformed get told | Cross-team decisions with unclear ownership | Setup cost; worth it above ~2 teams |
| **RAPID** | Recommend, Agree, Perform, Input, **D**ecide — the D is one person | Large orgs where the veto (Agree) is real, e.g. legal or security | Heavy; only pays off when a veto genuinely exists |
| **Consent** | Nobody objects with a **named harm** — not the same as everybody agreeing | Peer groups, reversible calls, teams without a hierarchy | Fast; degenerates if "harm" is not policed |

Consensus is the absent fifth: legitimate for cheap reversible calls in a group of ≤6, corrosive as a standing rule because it hands a veto to the most stubborn person and produces decisions nobody owns. Voting is for genuinely peer bodies (boards, committees) where the vote is the constitutional mechanism — inside a team it converts a discussion into a popularity contest and buries the minority argument.

## Reversibility Decides The Rigor

Sort every decision into one of two doors before choosing the method:

- **Two-way door** (reversible in days, cheap to undo): decide fast, at the lowest level, with the smallest room. Trying to make these carefully is the largest source of organizational slowness. Escape hatch: attach a review date and move on.
- **One-way door** (hard or expensive to reverse — a public commitment, a migration, a hire, a contract, a deprecation): slow method, pre-read, the decider present, the rejected options written. A one-way door decided in a corridor is the most expensive habit in this domain.

Test when it is unclear: **what does it cost to undo this in three months?** Under a week of work, treat it as reversible. Over a quarter, or visible to customers, treat it as one-way.

## Forcing A Decision

When the room keeps circling, in escalating order:

1. **Restate the exact question**, narrow enough to be answered yes or no.
2. **Put the options on the table with the do-nothing option included**, and say which one you recommend. An unstated recommendation makes the discussion abstract.
3. **Ask for the objection, by name**: "Sam, what would have to be true for you to say yes?" Objections that cannot be named are preferences.
4. **Convert the disagreement into a test.** "We disagree about whether latency is origin-side. What measurement settles it, and who runs it by when?" Half of all stuck decisions are unresolved facts, not conflicting values.
5. **Split the decision.** The reversible part decides today; the irreversible part gets its own slot with the right people.
6. **Time-box the deferral with a default**: "Priya decides by Thursday 12:00; if nothing by then we go with option A." A deferral without a default and a date is a decision to do nothing, made accidentally.

Never resolve a deadlock by averaging the positions. The midpoint of two coherent designs is usually incoherent, and nobody owns it.

## Disagree And Commit

The mechanism that makes fast decisions survivable: someone who lost the argument commits to executing the decision as if it were theirs, and says so out loud.

- **Ask for it explicitly**, by name, at the moment of the decision. Silence is not commitment; it is an option to relitigate later.
- **A "no, I can't commit" is valuable information**, not insubordination. It means either the decision is wrong or the objection was never actually heard — spend two more minutes finding out which.
- **Record who dissented and committed anyway.** Six months on, that person is the one whose warning you should reread before the retro.
- Commitment does not mean the decision is unreviewable: it means it is not reopened in hallways, only through the reopening rule below.

## The Decision Log

Every decision that took a meeting gets a row in `~/Clawic/data/meetings/decisions.md`, written in the same turn as the record block. The format, columns and split threshold are in `memory-template.md`. What earns its keep:

- **`Rejected` with the reason.** A decision without its rejected options is an opinion with a date, and the first person to think of option B reopens it.
- **`Method` and `Owner`.** They answer "who can change this" without a political conversation.
- **`Revisit`** as a real date for anything time-bound, mirrored as a `## Due` row so it actually comes back instead of expiring silently.
- Decisions with reasoning worth reading whole — a cost model, a diagram, a memo — get `artifacts/decision-<kebab>.md`, with the log row pointing at it.
- A decision on a tracked project also gets its one-line summary in `~/Clawic/data/projects/<project>.md`; the full entry stays in the log and is never duplicated.

Cheap decisions do not need a row. The test: **would someone plausibly ask "why did we do it this way?" in six months?** If yes, log it.

## Reopening

Decisions must be reopenable, or people stop making them. The rule that keeps this from becoming a treadmill:

- **New information reopens a decision. A new audience does not.** Someone arriving who was not in the room gets the log entry, not a rerun.
- **The reopener carries the burden**: what changed, what it costs to switch now, and what they propose instead. "I still don't like it" is not a reopening.
- **Reversible decisions reopen cheaply; one-way doors need the original decider.**
- **Third time is a structural problem, not a decision problem.** If the same question returns three times, either the decision rights are unclear or the decision is not being executed — fix that, not the argument.

**Write in the same turn as the decision**: the row in `~/Clawic/data/meetings/decisions.md`, the narrative in `records/<year>-<mm>.md`, the resulting action items in `## Follow-Ups`, a `## Due` row for any `Revisit` date, and `artifacts/decision-<kebab>.md` plus its `## Boxes` line whenever the reasoning is worth rereading (`memory-template.md`). An unlogged decision will be made again, and the second version will not match the first.
