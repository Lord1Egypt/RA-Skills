# Discount Discipline

A discount is a price change granted one customer at a time, with no plan and no measurement. Governing it is worth more than most repricings.

**Before approving anything**, read `price-book.md` (the floor and who may breach it), `## Deals` in `~/Clawic/data/pricing/memory.md` (what this customer and comparable ones already got), and `discount_floor_pct` in `config.yaml`. **After any deal outside policy**, write the row — depth, term, what was traded back, who approved — to `## Deals` in the same turn (`memory-template.md`).

## What a Discount Costs

Gross profit lost = `discount% ÷ margin%`.

| Discount | at m=0.50 | at m=0.70 | at m=0.85 |
|---|---|---|---|
| 10% | 20% of profit | 14.3% | 11.8% |
| 20% | 40% | 28.6% | 23.5% |
| 30% | 60% | 42.9% | 35.3% |
| 50% | 100% — the deal contributes nothing | 71.4% | 58.8% |

And the volume it must earn back: a discount of `d` needs `d / (m − d)` more units to stand still. At 70% margin a 30% discount needs **75% more volume** from that customer to be neutral. Almost no deal delivers that, which is why "we'll make it up in expansion" needs the expansion written into the contract, not hoped for.

## Everything Is Traded, Nothing Is Given

A discount buys something back or it is a price cut delivered slowly. The trade list, in rough order of value received:

| Give | Get | Worth roughly |
|---|---|---|
| Annual prepay | Cash now and one renewal decision instead of twelve | The prepay discount already in `annual_discount_pct` |
| Multi-year term | Two or three renewals removed from risk | 5-10% beyond the annual rate, with an uplift clause (`enterprise.md`) |
| Volume commitment | Revenue floor regardless of usage | Published schedule, applied mechanically |
| Reference, logo, case study | Distribution you would otherwise buy | One-off, on the first year only |
| Scope reduction | A cheaper product, honestly named | Not a discount at all — the right answer more often than it is used |
| Faster close | Nothing. A date is not consideration | Zero |

The last row is the one that costs the most money. A discount for closing this quarter teaches every buyer, and every buyer's network, to wait until the last week of the quarter permanently.

## The Approval Ladder

Authority is the mechanism; a policy with no named approver is a suggestion.

| Depth | Approver | Required before approval |
|---|---|---|
| 0 to `discount_floor_pct` | Anyone selling | Something traded back, named in the record |
| `discount_floor_pct` to +10pp | One level up | Trade + the break-even volume (→ What a Discount Costs) |
| Beyond that | Whoever owns the price book | Written justification and a review date; it becomes a `## Deals` row that is read at the next audit |
| Below the floor in `price-book.md` | Nobody, absent an explicit exception | An exception recorded in `## Floor Exceptions` with the argument, so the pattern is visible later |

- Approval must be **slow on purpose**. Instant approval at any depth teaches the field that the first number is decoration.
- Publish the volume schedule so the large discount is a rule rather than a negotiation outcome. This also removes most price-discrimination exposure between trade buyers (SKILL.md, Legal Tripwires).

## Annual Prepay

Two months free = 16.7% off. Whether that is generous depends entirely on churn:

Annual wins over monthly when `12 × (1 − d)` exceeds the months a monthly customer would actually pay, and at monthly logo churn `c` the expected months paid within a year is `(1 − (1 − c)^12) / c`.

| Monthly churn | Expected months paid in a year | 16.7% annual discount |
|---|---|---|
| 1% | 11.4 | Loses — you gave away a month you would have collected |
| 3% | 10.2 | Roughly break-even |
| 5% | 9.2 | Wins on revenue, before counting the cash |
| 8% | 7.9 | Wins clearly; the discount is cheaper than the churn |

Add the cash-flow value on top: a year collected upfront funds the acquisition of the next customer. Below roughly 3% monthly churn, deep annual discounts are a habit rather than a decision — and past two months free the discount usually exceeds the churn it prevents.

## Coupons and Promotions

- **Every promotion has an end date, published.** A permanent discount is a price, and it should be in `price-book.md` as one.
- Reason beats depth: launch, seasonal, education, non-profit, migration-from-a-competitor. A discount with a stated reason does not devalue the list price; a discount with no reason redefines it.
- Never run a public code that stacks with a sales-negotiated discount. Cap total discount at the deal level, not at the coupon level.
- Codes that grant money to whoever holds them are treated as secrets: an unpublished code is stored as a pointer, never written into any file under `~/Clawic/data/` (`memory-template.md`).
- Sunset old codes deliberately. Codes from a launch two years ago are still being posted on aggregator sites and still redeeming.

## The Quarterly Discount Audit

Cheap, and it finds real money. For the last quarter's closed deals:

| Check | Threshold | Action |
|---|---|---|
| Median realized discount vs list | Above `discount_floor_pct` | List is too high, or the fences are wrong (`packaging.md`) |
| Share of deals at exactly the approval ceiling | Above ~30% | The ceiling is the price; move it or enforce it |
| Deals with an empty "traded for" | Any | Coaching problem, not a pricing problem |
| Discount depth vs deal size | Larger discounts on smaller deals | Authority is leaking downward |
| Discounts granted below the floor | Any | Each one needs a `## Floor Exceptions` row and a decision to stop or to change the floor |

Run it on `cadence.discount_audit` and record the run in `## Due`. An audit with no last-run date gets skipped for a year.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Discounting to close the quarter | Teaches the market to wait; the effect compounds every quarter | Trade for term or prepay, or lose the deal on time |
| Percentage off as the default lever | Everything after it is measured against the discounted number, including the renewal | Reduce scope to a cheaper tier — same price integrity, honest product |
| Matching whatever discount the buyer claims a competitor gave | Unverifiable and rewards the claim | Ask for the quote; price against value, not against a story |
| Discount now, "we'll raise at renewal" | The renewal negotiation starts from the discounted number, never from list | Set the uplift in the contract at signature (`enterprise.md`) |
| One-off exceptions that are never recorded | The exception becomes the norm because nobody can see the pattern | Every out-of-policy deal is a `## Deals` row, no exceptions |
| Free months instead of a discount | Same margin loss, but it hides in a different line and never appears in discount reporting | Price it as a discount so it shows up in the audit |
| Discount past contribution margin | The customer costs money to serve, forever | The floor in `price-book.md` is absolute unless the owner breaches it in writing |

**Write the outcome**: every deal outside `discount_floor_pct` to `## Deals` with what was traded back and who approved; every breach of the price-book floor to `## Floor Exceptions`; the discount policy itself to `artifacts/discount-policy.md`; the audit run to `## Due` (`memory-template.md`).
