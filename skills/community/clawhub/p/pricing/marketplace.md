# Two-Sided Pricing — Take Rate and Subsidy

A marketplace prices access to the other side. Which side pays, and how much, decides whether liquidity ever forms.

**Before setting or changing a take rate**, read `price-book.md` (current rate and fee structure) and `## Cost Inputs` in `~/Clawic/data/pricing/memory.md` (payments, trust and support cost per transaction). **After the decision**, update `price-book.md` and write the rationale — including which side is subsidized and why — to `artifacts/decision-take-rate.md` with its `## Boxes` line (`memory-template.md`).

## What the Take Rate Must Cover

`take × GMV per transaction ≥ payments + trust and support + (blended CAC of both sides ÷ transactions per cohort lifetime)`

The last term is the one that decides everything. A marketplace where each acquired pair transacts twice needs a take rate many times higher than one where they transact monthly for three years. This is why low-frequency, high-value categories (property, cars, weddings) cannot run on a 10% rate and why high-frequency ones can.

Worked shape: 60 average order value, payments 2.9% + 0.30 (2.04), trust and support 1.50 per transaction, blended CAC 40 across a cohort that transacts 8 times → `2.04 + 1.50 + 5.00` = 8.54, or **14.2% of GMV** just to break even. Every point above that funds product and profit.

## Who Pays

| Structure | Works when | Watch |
|---|---|---|
| Supply pays | Supply has margin and is constrained; demand is the scarce side | The fee is visible to supply and they will price it into their listing anyway |
| Demand pays | Demand values curation or trust and supply is abundant | A visible buyer fee at checkout is a conversion event and, in several jurisdictions, a disclosure obligation (`compliance.md`) |
| Split | Both sides need to feel invested; reduces the single visible number | Two fees to explain instead of one |
| Neither, at first | Bootstrapping liquidity | Retrofitting a fee onto a free marketplace is the hardest price change in this skill |

**Subsidize the hard side.** Whichever side is harder to acquire and easier to lose gets the better economics — usually supply at the start, sometimes demand in categories where supply is already online elsewhere. State which side you are subsidizing; a marketplace that has not decided subsidizes both and runs out of money.

## Setting the Number

- **Look at what the participant's alternative costs**, not at other marketplaces. If a supplier's alternative is paying 20% to an agency plus doing their own admin, a 15% take rate with the admin included is cheap.
- **Tiered take rates** reward volume and lock in the suppliers you most want to keep — the same volume-schedule logic as `discounting.md`, published and applied mechanically.
- **Fee caps** on large transactions prevent the biggest deals leaking off-platform. Above a certain value, a percentage fee stops looking like a service charge and starts looking like a reason to exchange phone numbers.
- **Non-take-rate revenue** — promoted listings, subscriptions for supply, payments margin, insurance, financing — usually carries a better margin than the take rate and is invisible to the participant's headline comparison.

## Disintermediation

Every marketplace leaks. The take rate is bounded by how easy it is to transact off-platform:

- Leakage rises with transaction value and with repeat frequency between the same pair. A high take rate on repeat, high-value pairs is a subsidy to whoever helps them meet.
- What holds a pair on-platform: payments and escrow, dispute resolution, insurance or guarantee, scheduling and records, discovery of the *next* counterparty, reviews and reputation that do not travel.
- Price the guarantee explicitly. A buyer protection scheme with a stated payout is the clearest justification a take rate can have.

## Raising a Take Rate

The most visible price change there is: every supplier sees it at once, and they talk to each other.

1. Model per-supplier impact from actual GMV, not averages. Identify the cohort whose economics break and decide in advance whether losing them is acceptable.
2. Add value in the same release, and name it — better payouts, a new protection, a new demand channel.
3. Tier it so growth is rewarded: many suppliers can end up paying less by growing, which changes the story from "a rise" to "a new schedule".
4. Give long notice and honor in-flight bookings at the old rate. Changing the rate on a transaction already agreed is what generates the screenshots.
5. Record the change, the cohort, and the observed supply churn at 30/60/90 days in `## Price History`.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Benchmarking against another marketplace's take rate | Their frequency, value and CAC are different; the rate is an output of those | Compute from the formula above |
| One take rate for every category | Category margin and frequency differ by multiples | Rate by category, published |
| No cap on high-value transactions | The largest deals leave the platform | A cap, or a flat fee above a threshold |
| Free forever to build liquidity, fee later | Retrofitting a fee is the hardest change in this skill | Charge something early, even nominally, so the fee exists |
| Hiding the buyer fee until checkout | Conversion damage plus a disclosure obligation in several jurisdictions | Show the all-in price up front (`compliance.md`, `pricing-page.md`) |
| Take rate that ignores payment costs on small baskets | Fixed processing costs dominate small transactions | Percentage plus a fixed component, or a minimum fee |
| Subsidizing both sides indefinitely | The subsidy has no end condition and no side ever pays | Name the subsidized side and the condition that ends it |

**Write the outcome**: the take-rate structure, caps and category rates to `price-book.md`; the subsidy decision and its end condition to `artifacts/decision-take-rate.md`; payments, trust and CAC inputs to `## Cost Inputs` with dates; every rate change and its supply-churn read to `## Price History` (`memory-template.md`).
