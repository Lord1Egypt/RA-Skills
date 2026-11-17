# Free Tiers and Trials

Free is a distribution channel with a running cost. It works when the limit lands on a user who is already succeeding, and fails when it lands on one still setting up.

**Before designing a free tier**, read `price-book.md` (what the paid tiers gate) and `## Cost Inputs` in `~/Clawic/data/pricing/memory.md` (the marginal cost of serving one free user). **After the design**, update `price-book.md` and write the rationale, including the conversion assumption, to `artifacts/decision-free-tier.md` with its `## Boxes` line (`memory-template.md`).

## Which Free, and When

| Shape | Use when | Cost |
|---|---|---|
| **Free trial, time-limited** | Time-to-value is short and the product is complete on day one | Users who need longer than the window churn before they see it |
| **Free trial, feature-limited** | The paid capability is demonstrable but not consumable | Buyers cannot evaluate the thing they are buying |
| **Reverse trial** — full product for N days, then drops to a free tier | You want both evaluation and a permanent free base | Two states to build and explain |
| **Freemium** | Time-to-value is long, or the free user is the distribution (collaboration, sharing, public artifacts) | Support and infrastructure for users who will never pay |
| **Paid trial / pilot** | Enterprise, with implementation work | Slower funnel, far higher conversion |
| **No free anything** | High-touch sales, or the demo does the job | You lose the buyer who will not talk to anyone |

Credit card up front raises conversion of those who start and cuts the number who start. Neither is wrong; the deciding question is whether your funnel is short of volume or short of qualification.

## Can the Free Tier Pay for Itself

`monthly cost per free user ≤ r × m$ × L`

where `r` is the monthly free-to-paid conversion rate, `m$` the monthly contribution of a paid user, `L` the expected paid lifetime in months.

Worked: at 1%/month conversion, 20 USD monthly contribution and a 24-month life, the ceiling is `0.01 × 20 × 24` = **4.80 USD per free user per month**. If a free user costs 6 USD in infrastructure and support, the free tier is a marketing budget, and it should be argued for as one — with the acquisition it produces on the other side of the equation.

Second lever: free users who bring paying users. If each free user refers `k` paying users over their life, add `k × m$ × L` to the ceiling. That is the honest version of "our free tier is our growth channel", and it is testable.

## Designing the Limit

The limit must bite **on the success path**, when the user is already getting value:

| Good limits | Why they work |
|---|---|
| Collaborators, editors, or shared documents | Only hit once the product has spread inside the org |
| History or retention window | Bites when the data has become worth keeping |
| Volume of the value metric (records, runs, sends) | Scales with the outcome (`value-metric.md`) |
| Integrations with systems of record | Reached when it becomes load-bearing |

| Bad limits | Why they fail |
|---|---|
| Number of projects when everyone has one | Never reached; the user stays free forever |
| Support access alone | Punishes people who are struggling, not people who are winning |
| Export or data access | Reads as a hostage arrangement (`packaging.md`) |
| A rate limit so low the product cannot be evaluated | The evaluation fails, and the failure looks like the product |

Two checks before shipping a limit: what fraction of active free users would hit it in 90 days at today's behavior, and what a user sees at the moment they hit it. If the answer to the first is near zero, the limit is decorative; if the second is an error message, the upgrade moment is being spent on frustration.

## Trial Length and the Extension

- Set the window to comfortably exceed measured time-to-first-value, not to a round number. If most successful users reach value on day 9, a 7-day trial is a decision to lose them.
- **Start the clock at activation, not at signup.** A trial that expires while someone is waiting on their IT department teaches nothing.
- **Extensions for engaged users are almost free.** Somebody using the product on day 13 is not a lost cause; somebody who never logged in does not need more days.
- Pause rather than expire when a trial straddles a holiday period. It costs nothing and removes an entire category of complaint.

## Measuring It

| Metric | Definition that survives scrutiny | Trap |
|---|---|---|
| Free-to-paid conversion | Paid conversions ÷ **activated** free users in a cohort, measured at a fixed age | Dividing by all signups mixes bots and abandoned accounts into the denominator |
| Time to convert | Median days from activation to first payment | The mean is dragged by a long tail and hides the modal path |
| Limit-hit rate | Share of active free users who reach the limit within 90 days | If this is near zero, no conversion work will help |
| Cost per free user | Infrastructure + support ÷ active free users | Support cost is usually the larger half and is usually left out |
| Free-sourced paid revenue | Revenue from accounts whose first touch was free | The number that decides whether free stays |

Published benchmarks for free-to-paid conversion vary by an order of magnitude and are mostly incomparable because the denominator differs. Use them to sanity-check, never to set a target; your own cohort at a fixed age is the only figure that means anything.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| A free tier generous enough to be the product | Nothing ever hurts, so nothing ever converts | Limit on the success path; check the limit-hit rate |
| Crippling the free tier | It stops demonstrating value and the funnel dries up at the top | Full core job, fenced on scale and control |
| Counting signups as free users | Flatters every ratio and hides the real cost per active user | Activated users as the denominator, everywhere |
| Removing the free tier abruptly | Every free user is a public voice, and this is the change they organize around | Long notice, a migration offer, a grandfathered cohort with an expiry (`price-increase.md`) |
| Trial length copied from a competitor | Their time-to-value is not yours | Measure time-to-first-value, then add margin |
| Free plan with no upgrade prompt at the limit | The one moment of maximum intent goes unused | An in-context offer at the limit, naming what unlocks |
| Treating free users as a cost centre only | Ignores referral and content value, and the tier gets killed on a partial number | Add `k × m$ × L` to the ceiling and test the referral rate |

**Write the outcome**: the free tier and its limits go into `price-book.md`; the design rationale, the conversion assumption and the cost ceiling to `artifacts/decision-free-tier.md`; the measured conversion at each cohort read to `## Experiments` if it came from a test, otherwise to `## Price History` (`memory-template.md`).
