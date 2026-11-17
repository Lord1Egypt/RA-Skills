# Activation — From Signup to First Real Value

Activation is the only stage where a product change and a growth change are the same change. It is also the stage with the largest available lift in most self-serve businesses, because nobody owns it: acquisition stops at signup and product starts at feature requests.

**Contents:** [Find the Aha Action, Do Not Guess It](#find-the-aha-action-do-not-guess-it) · [Setup Moment vs Aha Moment vs Habit Moment](#setup-moment-vs-aha-moment-vs-habit-moment) · [Time to Value](#time-to-value) · [Cutting the Path](#cutting-the-path) · [Empty States and the Cold Start](#empty-states-and-the-cold-start) · [Onboarding Patterns That Earn Their Place](#onboarding-patterns-that-earn-their-place) · [Measuring It](#measuring-it) · [Traps](#traps)

**Before redesigning onboarding**, read `## Funnel` (activation rate and its definition) and `## Metric Definitions` in `~/Clawic/data/growth/memory.md`, plus `artifacts/activation-spec.md` if `## Boxes` lists it. Redesigning without the current aha action changes the order of steps that never mattered.

## Find the Aha Action, Do Not Guess It

The aha action is a behaviour that separates users who stay from users who leave. Derive it:

1. Take a cohort at least one natural frequency old (`retention.md`) — long enough that retained and churned are distinguishable.
2. Split into retained and churned at that horizon.
3. For every candidate action in the first session and the first week, compute the rate in each group.
4. Rank by the **gap**, not by the absolute rate. An action 90% of everyone does is not a discriminator.
5. Find the **threshold** by plotting retention against count of the action: the point where the curve bends is the number, not a round figure someone likes.

```
Candidate                     Retained M1   Churned M1   Gap
Invited ≥1 teammate               74%          19%      +55
Created ≥3 projects               68%          31%      +37
Connected an integration          52%          38%      +14
Visited settings                  61%          58%       +3   ← not a discriminator
```

Then the honest caveat, stated every time: **this is correlation.** The only way to know whether pushing the action causes retention is to push it and watch the cohort (`experiments.md`). Products have burned quarters forcing an action that merely marked people who were already committed. The test is cheap: prompt the action for half of new users and compare retention at the same horizon.

## Setup Moment vs Aha Moment vs Habit Moment

Three distinct moments, routinely conflated into one "onboarding":

| Moment | Definition | Design goal | Typical failure |
|---|---|---|---|
| Setup | The minimum configuration before value is possible | Remove it, defer it, or do it for them | Asked up front "so it is out of the way" — it is where people leave |
| Aha | The first time the user gets the value they came for | Reach it in one session | Buried behind setup that could have been defaulted |
| Habit | The behaviour that makes them come back unprompted | Trigger it on the natural frequency | Never designed; treated as retention's problem |

The sequencing rule: **value before setup wherever the product allows it** — show the result on sample or imported data, then ask for the configuration once the user wants to keep it. Nothing raises activation like deleting a required field.

## Time to Value

`TTV = median minutes from signup to the aha action, for users who reach it`. Track the median and the reach rate together: a product can shorten TTV by making the aha easier for the few who already got there while the reach rate falls.

- Measure both **in-session TTV** (same session as signup) and **7-day TTV**. The gap between them is the size of the "came back to finish" population, which is exactly who lifecycle messaging can rescue (`lifecycle.md`).
- Every step before value has a survival cost. Count the steps: fields in the form, clicks, screens, decisions, and any wait longer than a few seconds. The count, not the aesthetics, predicts the drop.
- Waits are steps too. If value requires processing, show partial value immediately and complete in the background; a progress bar with nothing behind it converts worse than a partial result.

## Cutting the Path

Ordered by typical yield, highest first. Each is measurable in isolation.

| Cut | Mechanism | Watch for |
|---|---|---|
| Delete form fields | Every required field is an exit; ask for what you need to deliver value and nothing else | Sales' desire for firmographics — collect it after activation or enrich it (`b2b.md`) |
| Defer account creation | Let the user do the work first, ask for the account to save it | Anonymous work must actually persist through signup, or you have built a rage-quit |
| Default every choice | Pre-select the option most users need; make it changeable, not required | Defaults that suit the company (highest plan) rather than the user destroy trust |
| Seed the empty state | Sample data, a template, or import from the tool they came from | Sample data that cannot be deleted, or that pollutes their real workspace |
| Do it for them | Concierge onboarding by a human for high-ACV accounts | It does not scale, and that is fine while it is a diagnostic |
| Remove the tour | A tour is an admission that the interface is unclear | Deleting the tour without fixing the interface |
| Progressive disclosure | Reveal advanced options only when needed | Hiding the one control the user came for |

Verify each cut against the **downstream** metric, not activation alone: it is trivial to raise activation by lowering the bar and end up with more activated users who convert less (`monetization.md`).

## Empty States and the Cold Start

The empty state is the most-viewed screen in most products and the least designed. It has one job: make the next action obvious and cheap.

- **Single-player value first** in any product that eventually needs other people. If the product only works once teammates join, the invite is a setup step and belongs behind a first taste of value, not in front of it.
- **Import beats create.** A one-click import from whatever they used before converts far better than a blank canvas, and it also tells you the competitor set for free.
- **Templates carry intent.** A template picker doubles as segmentation: the template chosen is a use-case property worth putting on the signup event (`instrumentation.md`).
- **Multi-sided products cannot fake the other side.** In a marketplace, an empty state is an inventory problem, not a design problem (`marketplaces.md`).

## Onboarding Patterns That Earn Their Place

- **Checklist with visible progress** — works when the items are genuinely required for value, fails as a chore list for feature discovery. Cap at 3-5 items; the first should already be done by the act of signing up.
- **Personalization question** — one question, only if the answer branches the experience in a way the user can perceive. Otherwise it is a survey the user pays for with attention.
- **Reverse trial** — full features for a fixed period, then downgrade to free. Gets users to the premium aha before the paywall exists, and makes the paywall about losing something rather than buying something (`monetization.md`).
- **Activation email sequence** — behaviour-triggered, not day-based: send when the user *has not* done the next step, stop the moment they do (`lifecycle.md`).
- **In-product prompt at the moment of intent** — beats any email, because the user is already there.

## Measuring It

- Activation rate = users reaching the aha action within the window ÷ signups in that cohort. Window: one natural frequency or 7 days, whichever is shorter, fixed once and written down.
- Report the **step-by-step drop** of the onboarding path, not just the endpoint. The largest single drop names the work.
- Segment by acquisition source always: paid traffic activates differently from referral traffic, and a blended activation rate will hide a channel that buys people who will never activate (`acquisition.md`).
- Re-derive the aha action when the product changes materially or at least every two quarters — the discriminating behaviour moves with the product.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Adopting another company's aha ("7 friends in 10 days") | It was derived from their data, their product, their era | Derive yours from your own cohorts |
| Forcing the correlated action on everyone | Correlation, not causation; you can annoy users into leaving faster | Test the prompt on half the cohort and compare retention |
| Optimising signup rate in isolation | More signups of lower intent lower every rate beneath them | Judge signup changes on activated users, not signups |
| Onboarding tour instead of a fixed interface | Tours are skipped by the majority and forgotten by the rest | Fix the interface; the tour is a diagnostic that you have not |
| Asking for the invite before single-player value | The user has nothing to invite anyone to | Value first, invite at the moment collaboration would help (`loops.md`) |
| Counting activation as "completed onboarding" | Measures compliance with your flow, not value received | Anchor on the value action itself |

**After deriving an aha action, shipping an onboarding change, or measuring a new activation rate**, write it back in the same turn: the rate with its definition and as-of date into `## Funnel`, the aha action and its threshold into `## Metric Definitions`, both in `~/Clawic/data/growth/memory.md`. The onboarding path that finally worked — steps, defaults, seeded state, the aha threshold and how it was derived — is `~/Clawic/data/growth/artifacts/activation-spec.md`, created the first time it exists, with its `## Boxes` line in the same turn (`memory-template.md`). The test that established causation gets its row in `experiments/<year>.md`.
