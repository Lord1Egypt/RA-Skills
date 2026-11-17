# Executing a Price Increase

A raise is a project with a sequence, a churn budget, and a written plan. Almost every visible pricing disaster is an execution failure, not a wrong number.

**Before planning**, read `price-book.md`, `## Price History` in `~/Clawic/data/pricing/memory.md` (what was raised, when, and what it cost last time), and `## Cost Inputs` for the margin the break-even needs. **Write the plan** to `artifacts/plan-<what>-<year>.md`, one row per change to `## Price History` with its cohort and grandfather expiry, and a `## Due` row for each checkpoint and each expiry date — all in the same turn (`memory-template.md`).

**Contents:** [Is It a Price Problem](#decide-whether-it-is-a-price-problem) · [Churn Budget](#the-churn-budget-computed-first) · [The Sequence](#the-sequence) · [Grandfathering](#grandfathering) · [Notice and Communication](#notice-and-communication) · [Save Ladder](#the-save-ladder) · [Reading the Result](#reading-the-result) · [Cuts and Rollbacks](#cuts-and-rollbacks) · [Traps](#traps)

## Decide Whether It Is a Price Problem

Raise when at least one is true, with evidence:

- Objection rate on price is far below the discount depth you grant — you are already selling at a price nobody argues with (→ Signals in SKILL.md).
- Unit costs moved and the margin is now below `target_gross_margin_pct`.
- The product gained capability that changed the buyer's alternative.
- The list price has not moved in years while the market and the reference price did.

Do not raise when churn is concentrated at first renewal, when activation is the failure, or when the last raise's outcome was never measured. Those are the three cases where a raise converts a product problem into a public one.

## The Churn Budget, Computed First

From SKILL.md Rule 2: a rise of `x` at contribution margin `m` survives a volume loss of `x / (m + x)`.

Worked: raising 39 → 45 is +15.4%. At `m = 0.82`, the tolerable loss is `0.154 / 0.974` = **15.8% of that cohort**. Set the stop line below the break-even — half of it is a common choice — so there is time to reverse before the move is already unprofitable.

Three numbers go in the plan before anything ships: the break-even loss, the stop line, and the date each checkpoint gets read. A raise with no stop line does not get reversed; it gets defended.

## The Sequence

Always in this order. Each stage de-risks the next.

1. **New logos only.** The cleanest possible test: no incumbent expectation, no notice obligation, no goodwill at stake. Run it for at least one full sales cycle and read win rate, not just conversion.
2. **Renewals.** Customers already at a decision point, with a contract boundary to do it at. Their reaction tells you what the installed base will do.
3. **Existing customers on notice.** The loudest stage, and the one the whole plan protects. Never first.

Skipping to stage 3 because the finance model wants the revenue this quarter is the decision behind most of the public backlash stories.

## Grandfathering

`grandfather_policy` picks the default; the plan states which applies and until when.

| Policy | What it means | Costs you |
|---|---|---|
| `forever` | Existing customers keep the old price indefinitely | A permanent second product: its own code path, its own support answers, its own migration project later |
| `fixed-term` | Old price held to a stated date | A calendar entry and one more comms cycle |
| `next-renewal` | Old price until their next renewal date | Nothing structural — the default |
| `none` | Everyone moves on the notice date | The largest single churn event, concentrated |

- **Every grandfather has an end date, written down.** "Indefinitely" is how a legacy plan becomes permanent by accident. The expiry goes into `## Due` the same day it is promised.
- Grandfathering is worth most where switching cost is low and goodwill is the retention mechanism; it is worth least in high-switching-cost enterprise, where the renewal is the natural boundary.
- Do not grandfather *and* keep selling the old plan. One or the other.

## Notice and Communication

- **Notice period**: 30 days is the practical floor for a monthly plan and 60 for annual, and the contract or local consumer rules may demand more — check before the date is announced (`compliance.md`). Under-noticing converts a price change into a compliance problem.
- **One message, from the company, before any invoice moves.** The invoice must never be the first the customer hears of it.
- Structure that survives contact: what is changing, the new number, the exact date, what is *not* changing, what they should do if nothing (usually nothing), and where to reply. Six lines.
- **Do not apologize and do not over-explain.** A raise justified by your costs is about you; a raise justified by what shipped since the last one is about them. Neither needs three paragraphs.
- No countdowns, no "act now to lock in the old price" unless you will genuinely honor it forever — that offer is a grandfather clause with a marketing hat on, and it binds.
- Tell the support and sales teams before the customers, with the answer to "can I keep my old price" already decided. An improvised answer becomes the policy.

## The Save Ladder

Decide in advance what a churning customer can be offered, in ascending order of cost, and who may offer it:

1. Annual prepay at the old effective rate (converts churn risk into cash).
2. A longer term at a smaller increase.
3. A downgrade to a tier that fits their real usage — often the honest answer and a retained logo.
4. A time-limited hold with a stated expiry, recorded as a grandfathered cohort in `## Price History`.
5. Nothing. Some churn is the intended outcome of a raise; a customer who leaves at +15% was not going to fund the roadmap.

Every rung used gets a row in `## Deals` with what was traded back, and any hold gets its expiry in `## Due`.

## Reading the Result

| Checkpoint | Read | Watch for |
|---|---|---|
| Day 0-7 | Support volume, cancellation starts, public reaction | A spike here is comms, not price |
| Day 30 | Cohort churn vs the stop line, ARPU on the new price | Compare against the same cohort's prior baseline, never against the whole book |
| Day 60 | Downgrades and downsells, not just cancellations | Silent downgrades are how a raise disappears |
| Day 90 | Net revenue for the cohort, win rate on new logos | This is the number that decides whether stage 3 proceeds |

Write each read into the outcome column of the `## Price History` row on the day it is taken. A blank outcome column three months later means the next raise gets argued from feelings again (SKILL.md Rule 9).

## Cuts and Rollbacks

- A price cut is far harder to justify arithmetically than a raise (`elasticity.md`) and far harder to reverse socially. Prefer a time-boxed promotion, a lower entry tier, or a discount you can withdraw.
- Rolling back a raise publicly costs less than defending one that missed the stop line, but it can only be done once. Say what you learned and what the new date is; do not pretend it did not happen.
- Record the rollback as its own row in `## Price History`, including the reason. It is the most useful row in the file.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Flat percentage across every cohort | Cohorts differ in tolerance; the best accounts absorb the least scrutiny | Segment and sequence (→ The Sequence) |
| Raising because the model needs the revenue | The break-even was never computed, so the move has no stop line | Churn budget before the date |
| Announcing on the invoice | Turns a price change into a trust event | Notice period, one message, before billing |
| Grandfather with no expiry | A permanent second product nobody owns | Fixed date, recorded in `## Due` |
| Offering a hold to whoever complains loudest | The policy becomes "shout" and it spreads | A written save ladder with named authority |
| Reading churn against the whole customer base | The affected cohort is a minority; the signal disappears in the average | Cohort-level reads at 30/60/90 |
| Raising and repackaging in the same message | Nobody can tell which one they are angry about, including you | One change per message, weeks apart |

**Write the outcome**: the plan goes to `artifacts/plan-<what>-<year>.md`; each change, cohort and grandfather expiry to `## Price History`; each checkpoint date and expiry to `## Due`; each save-ladder concession to `## Deals`; the new numbers into `price-book.md` (`memory-template.md`).
