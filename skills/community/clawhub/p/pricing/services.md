# Pricing Time and Scope — Consulting, Agency, Freelance

Selling hours caps income at hours available. The progression out of that cap is the whole subject.

**Before quoting**, read `price-book.md` (the current rate card and its floor) and `## Deals` in `~/Clawic/data/pricing/memory.md` (what comparable clients pay — inconsistent rates between similar clients is discovered eventually). **After the quote**, write the rate card to `artifacts/rate-card-<client-or-year>.md`, the engagement to `## Deals`, and the client to the shared `contacts.md` (`memory-template.md`).

## The Floor: What Your Day Actually Costs

`day rate = target income × (1 + overhead) / (working days × utilization)`

Worked: 120,000 target, 30% overhead (tools, insurance, accounting, unpaid admin, equipment), 220 working days, 60% utilization → `156,000 / 132` ≈ **1,180 per day**.

- **Utilization is the term people get wrong.** Solo practitioners rarely bill above 60-70% of working days once sales, admin, and delivery gaps are counted; assuming 100% produces a rate that guarantees a shortfall.
- Add unpaid time explicitly: holiday, sick days, and the days spent winning the next engagement.
- This is a **floor**, not a price. It says what you cannot go below, which is a different question from what the work is worth.

## Four Pricing Models, in Order of Maturity

| Model | Charge | Right when | Fails when |
|---|---|---|---|
| **Hourly** | Time recorded | Scope genuinely unknowable; small tasks; support retainers | Rewards slowness, makes every efficiency gain a pay cut, invites time-sheet arguments |
| **Day rate** | Days booked | Ongoing embedded work | Same incentive problem, one level up |
| **Fixed scope** | A defined deliverable | Scope can be written down and defended | Undefined scope becomes free work (→ Scope Control) |
| **Value-based** | A share of the quantified outcome | The outcome is measurable and attributable to you | The client controls the measurement, or the outcome depends on their execution |

Moving up the table is a positioning change, not a pricing trick: fixed and value pricing require you to define scope precisely, which requires knowing the work well enough to bound it.

## Fixed-Scope Quoting

1. Estimate the days honestly, then add a contingency for the unknown — 20-30% on work you have done before, more on work you have not.
2. Price at day rate × estimated days, then check it against the value delivered. If value pricing gives a higher number and the outcome is attributable, quote that instead.
3. Write scope as **inclusions and exclusions**. The exclusions list prevents more disputes than the inclusions list.
4. Name the number of revision rounds and what a further round costs.
5. State the payment schedule: a deposit before work starts, milestones during, final on delivery — never all on completion, which makes you the client's lender.
6. Define what triggers a change order, and price change orders at a **higher** rate than the base. Mid-project changes cost more to absorb and the price should say so.

## Retainers

- **Access retainer** (a block of availability): predictable for both sides, and the model most likely to be paid for nothing and cancelled. Attach a deliverable.
- **Capacity retainer** (N days per month): the workhorse. State whether unused days roll over — no rollover is cleaner, partial rollover into the next month only is the usual compromise.
- **Outcome retainer** (a standing responsibility): highest value, requires trust, priced against what the responsibility is worth rather than against days.
- Price a retainer **above** the equivalent day rate divided across the month if it reserves capacity you cannot resell, and **below** it if it guarantees you volume. Decide which it is before quoting.
- Review every retainer on a fixed cadence, recorded in `## Due`. Retainers drift into either resentment or free work, and neither is visible without a review date.

## Raising Your Rate

- Raise on **new clients first**, always. It costs nothing and produces real evidence.
- Existing clients move at a natural boundary: contract renewal, a new project, or a stated annual review date. Mid-project raises are the one version that damages relationships.
- Notice of 60-90 days for ongoing clients is normal in services and costs nothing.
- Expect to lose the bottom of the client list, and plan for it: that is how the rate rise creates the capacity it needs. Compute the break-even from SKILL.md Rule 2 with `m` near 1, since a solo practitioner's variable cost per day is small — at `m = 0.9`, a 20% raise tolerates an 18% loss of billable days.
- Record the old and new rate, the date, and which clients moved in `## Price History`.

## Scope Control

- **Every unbilled favour is a rate cut.** Log each one on that client's row in `## Deals` as an unbilled concession, with the days it cost; the running total is usually a surprise.
- Answer scope creep with a price, not a refusal: "That's outside the scope — I can add it for X, or swap it for Y." A price makes the request a decision instead of an argument.
- The estimate is not the quote. Send estimates as ranges with the assumptions listed; send quotes as one number with a validity date.
- Say the number early in the conversation. Discovering a 5× mismatch in month two costs both sides more than an awkward first call.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Hourly billing on work you are good at | Expertise makes you faster, and faster means paid less | Fixed scope or value, once the work is bounded |
| Quoting from a target annual income with no utilization factor | Produces a rate roughly 40% too low | The formula above, with honest utilization |
| Discounting the first project "to get the relationship" | The first price is the anchor for every project after it | Reduce scope for a smaller first project at full rate |
| No deposit | You finance the client's project and carry the collection risk | Deposit before work starts, always |
| Unlimited revisions | Consumes the margin invisibly, and the last 10% takes 50% of the time | Named rounds, priced extras |
| One rate for every client and every kind of work | Rush work, unfamiliar domains, and difficult clients all cost more | Rate card with modifiers, written down |
| Rate never reviewed | Inflation alone cuts the real rate every year | Annual review date in `## Due` |

**Write the outcome**: the rate card to `artifacts/rate-card-<client-or-year>.md` and the current rates to `price-book.md`; each engagement, its discount and what was traded to `## Deals`; the client to the shared `contacts.md` by key; retainer and rate-review dates to `## Due`; every rate change to `## Price History` (`memory-template.md`).
