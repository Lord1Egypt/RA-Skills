# Willingness-to-Pay Research

Research narrows a range. It does not produce a price, and no method here outranks what somebody actually paid.

**Before designing a study**, read `## Research` and `## Competitors` in `~/Clawic/data/pricing/memory.md` — a study that repeats one run nine months ago is expensive. **After any study**, write the row (method, n, segment, date, resulting range) to `## Research` and the full write-up, questions and curves to `artifacts/wtp-study-<yyyy-mm>.md`, with its `## Boxes` line in the same turn (`memory-template.md`).

**Contents:** [Evidence Ranking](#evidence-ranking) · [Van Westendorp](#van-westendorp-price-sensitivity-meter) · [Gabor-Granger](#gabor-granger) · [Conjoint and MaxDiff](#conjoint-and-maxdiff) · [Interviews](#interviews-that-produce-numbers) · [Win/Loss](#winloss-the-cheapest-and-best-source) · [Competitor Tracking](#competitor-price-tracking) · [Choosing a Method](#choosing-a-method)

## Evidence Ranking

Strongest to weakest. Spend the research budget at the top of this list before buying a survey.

1. **Money that changed hands** — accepted quotes, discount depth at close, renewal and expansion behavior.
2. **Deals lost on price**, with the competitor and the number they took instead.
3. **Observed switching** — what they abandoned to buy you, and what it cost them.
4. **Choice-based studies** (conjoint) — a forced trade-off is closer to a purchase than a rating.
5. **Price-ladder surveys** (Gabor-Granger) — purchase intent at specific numbers.
6. **Perception surveys** (Van Westendorp) — a band of plausibility, not a demand curve.
7. **Direct questions** — "would you pay X". Stated intent overstates purchase behavior consistently; use it only to disqualify absurd prices.

## Van Westendorp Price Sensitivity Meter

Four questions about the same product, asked in this order, each returning a price:

1. At what price would it be **so expensive** you would not consider it?
2. At what price would it be **so cheap** you would doubt the quality?
3. At what price does it start to feel **expensive but still worth considering**?
4. At what price would it be a **bargain**?

Plot the four as cumulative curves and read the intersections:

| Point | Intersection | Meaning |
|---|---|---|
| PMC — point of marginal cheapness | "too cheap" × "expensive" | Below this, quality doubt costs you sales |
| PME — point of marginal expensiveness | "too expensive" × "bargain" | Above this, resistance rises steeply |
| OPP — optimal price point | "too cheap" × "too expensive" | Fewest people reject it in either direction |
| IPP — indifference price point | "expensive" × "bargain" | Often near the market's current reference price |

- **The output is the PMC-PME band.** Reporting the OPP as "the price" is the single most common misuse: it is the least-rejected point, which is not the revenue-maximizing point.
- **Sample**: a working floor of about 150 respondents per segment. Below roughly 75, a handful of extreme answers move the intersections, and the band is not stable enough to price against.
- **Segment before averaging.** Two segments with different budgets produce a smooth curve for a price that suits neither.
- **Screen respondents** to people who would actually buy the category. Panels answer confidently about products they have never needed.
- Show the product first — a description, a demo, or a real screen. Answers about an imagined product measure imagination.

## Gabor-Granger

Ask purchase intent at a specific price, then move up or down the ladder until intent collapses. Produces a demand curve and, multiplied by price, a revenue curve with a maximum.

- **It only knows the prices you asked.** Bracket wide enough that the top of the ladder gets refused; a ladder that stops before refusal returns your own ceiling.
- It has no competitive context: respondents are not choosing between you and an alternative, so it flatters.
- Best used *after* Van Westendorp: the band sets the ladder, the ladder finds the point.
- Randomize the starting rung. Starting high and walking down anchors differently from starting low and walking up.

## Conjoint and MaxDiff

- **Choice-based conjoint** presents packages with different features and prices and asks which one they would buy. Because respondents trade off rather than rate, it approximates a purchase and it can price individual features. Cost: design effort and a larger sample — segment-level utilities generally want several hundred respondents.
- **MaxDiff** ranks feature importance without pricing anything. It is the right tool for *packaging* (which fence goes in which tier, `packaging.md`), and the wrong tool for a price.
- Both fail the same way: attributes the researcher invented. Draw the feature list from win/loss reasons and support requests, never from the roadmap.

## Interviews That Produce Numbers

Ten well-run interviews beat a badly targeted survey of four hundred. Ask about the past, not the future:

- "What are you using today, and what does it cost you all-in — licence, people, workarounds?" — this is the reference price (`value-metric.md`).
- "What did you pay for the last tool you bought in this category, and who approved it?" — reveals budget authority and the threshold that triggers procurement.
- "What would have to be true for this to come out of a different budget line?" — a bigger budget is often a positioning change, not a price change.
- "Walk me through the last time you asked for money for something like this." — the process is the constraint more often than the number is.
- Never present your price and ask for a reaction. You will get politeness, and politeness has no predictive value.

## Win/Loss — the Cheapest and Best Source

- Ask every lost deal what they chose and what they paid. The number they name is a real transaction, which no survey produces.
- Track the **discount at close** on won deals: if the median close is 20% under list, list is 20% high or the fences are wrong (`discounting.md`).
- Track **price objections as a share of deals**. Objections are not a failure signal; their *absence* is (→ Signals in SKILL.md).
- Log every one of these in `## Deals` and `## Competitors` as it happens. Reconstructing a year of win/loss from memory produces the story, not the data.

## Competitor Price Tracking

- Record price, the value metric it is priced on, what it includes, the date observed, and where it was seen, as a row in `## Competitors`. A price without its metric is not comparable.
- Published price is a list price. Enterprise reality is the published price minus a discount you cannot see; treat public pages as a ceiling, and treat a number a prospect quotes you as a data point about *that* deal.
- Sweep on a cadence rather than on impulse, and write what changed. The row that says "unchanged since 2026-01" is worth as much as the row that moved.
- A competitor price under NDA is data, not a secret: record it with `source: under NDA — not for external use` and never repeat it in customer-facing material (`memory-template.md`).

## Choosing a Method

| Decision | Method | Typical effort |
|---|---|---|
| Nothing exists yet; need a plausible band | Van Westendorp on a screened segment, plus five interviews | Days |
| Band exists; need a point | Gabor-Granger on a ladder set by the band | Days |
| Which features belong in which tier | MaxDiff, or win/loss reasons if the sample is small | Days |
| Feature-level willingness to pay, or a share simulation | Choice-based conjoint | Weeks, and a specialist |
| Already selling | Win/loss, discount depth, cohort behavior — before any survey | Ongoing, free |
| Enterprise, low deal count | Interviews and quotes; surveys with n=12 are decoration | Ongoing |
| Anything else | Start with the highest item on the Evidence Ranking you can actually obtain | — |

**Write the outcome**: the row (method, n, segment, date, range) goes to `## Research`; the questions, curves and write-up go to `artifacts/wtp-study-<yyyy-mm>.md`; every competitor price observed goes to `## Competitors` with its date; the resulting price lands in `price-book.md` (`memory-template.md`).
