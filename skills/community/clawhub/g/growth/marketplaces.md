# Marketplaces — Liquidity, the Constrained Side, and the Cold Start

A marketplace has two funnels that must be solved together, and one metric that matters more than either: **liquidity** — the probability that a listing transacts, and that a searcher finds something. Growth work that ignores which side is constrained produces spend on the side that was already fine.

**Contents:** [Liquidity Is the Metric](#liquidity-is-the-metric) · [Finding the Constrained Side](#finding-the-constrained-side) · [The Cold Start](#the-cold-start) · [Geography and Category as the Unit](#geography-and-category-as-the-unit) · [Matching Quality](#matching-quality) · [Take Rate and Disintermediation](#take-rate-and-disintermediation) · [Supply Growth](#supply-growth) · [Demand Growth](#demand-growth) · [Experimenting on a Marketplace](#experimenting-on-a-marketplace) · [Traps](#traps)

**Before proposing any marketplace tactic**, read `## Business` (which side is constrained and when it was last checked), `## Markets` (or `markets.md` if `## Boxes` points there), `## Funnel` (both sides) and `## Channels` in `~/Clawic/data/growth/memory.md`. The constrained side flips with season, category and city; acting on a stale answer spends money on the abundant side.

## Liquidity Is the Metric

Define both directions and measure both, always by market (city, category, or whatever the real matching unit is):

```
supply_liquidity = listings that transact within N days ÷ listings created
demand_liquidity = searches or requests that convert ÷ searches or requests
```

Set N from the category's natural expectation — hours for a ride, days for a rental, weeks for a house. GMV, listing count, and user count all rise while liquidity falls, which is exactly the failure mode: a marketplace that looks like it is growing while both sides' experience gets worse.

Two supporting numbers: **time to first transaction** for a new supplier (the number that predicts whether they come back) and **search-to-contact rate** (whether demand finds anything at all).

## Finding the Constrained Side

| Signal | Constrained side |
|---|---|
| Searches returning few or zero results; high search abandonment | Supply |
| Listings expiring unsold; suppliers churning after one listing | Demand |
| Both sides complain about price | Matching, not volume — the sides do not want the same thing |
| Fill rate high but repeat rate low | Quality, not liquidity |

Verify with a **spend test**, not an argument: add demand to one market and supply to a comparable one for two weeks, and see which moves transactions. Marketplaces flip sides by season and category, so the answer carries an expiry date; write it with one.

The rule that follows: **spend on the constrained side only.** Spending on the abundant side degrades its experience — more suppliers competing for the same demand means lower earnings per supplier and faster supplier churn.

## The Cold Start

Every marketplace begins with no liquidity anywhere. The plays that work are unscalable by design, and that is correct:

- **Constrain the market until it is dense.** One city, one category, one campus. Density in a tiny market beats presence in a large one — a marketplace is a local phenomenon even when the website is global.
- **Fake or own the constrained side.** Buy the inventory, employ the suppliers, or list on behalf of others (with permission). Cost of goods bought to create liquidity is a customer-acquisition cost, and should be budgeted as one.
- **Single-player value first.** Give one side a tool that is useful with zero counterparties — inventory management, scheduling, a portfolio page — so supply accumulates before demand exists (`activation.md`).
- **Piggyback an existing marketplace or community** for the first cohort of the constrained side, then give them a reason to stay.
- **Concierge the match.** Humans matching by hand teaches the matching rules the algorithm will need, and it is the only way to learn them early.

Exit the cold start per market, not globally: the second city starts at zero and needs the same playbook, faster.

## Geography and Category as the Unit

- Report liquidity, CAC, and retention **per market**, never blended. A national average hides three saturated cities and twelve empty ones, and it produces a national strategy that fits nowhere.
- Define the real matching unit: physical services match by travel time, not by city boundary; digital services may match nationally; some categories match only within a narrow segment.
- **Market maturity cohorts**: group markets by launch date and compare their liquidity curves. A new market that is behind the curve of its predecessors at the same age is a launch-playbook problem, not a marketing budget problem.
- Expansion decision: open a new market only when the current one has crossed the liquidity threshold, or the playbook being copied is a playbook for failure.

## Matching Quality

Liquidity is not enough if the matches are bad: bad matches produce refunds, disputes, and one-time users on both sides.

- Track **repeat rate by both sides** separately. A marketplace where suppliers repeat but buyers do not has a quality or expectation problem, not a supply problem.
- Ranking is the product. What ranks first determines earnings distribution, which determines supplier retention: a ranking that concentrates all demand on a few suppliers churns the rest, and a marketplace with only star suppliers has no capacity.
- Reduce **search friction on the constrained side's terms**: if supply is scarce, help demand accept alternatives (flexible dates, nearby, similar); if demand is scarce, help supply find it (alerts, saved searches, proactive matching).
- Trust mechanisms — reviews, verification, guarantees, escrow — are conversion features, not compliance features. They usually pay for themselves in first-transaction rate.

## Take Rate and Disintermediation

- Take rate is what the marketplace charges for the match. It is defensible in proportion to the value the platform adds *after* discovery: payments, trust, dispute resolution, scheduling, insurance.
- **Disintermediation risk rises with repeat frequency and transaction value.** A weekly high-value service between the same two parties will leave the platform; a one-off low-value match will not. Design accordingly: for high-repeat categories, sell the workflow (scheduling, invoicing, payments) rather than the introduction.
- Raising take rate is a price change with a two-sided blast radius: model the supply-side elasticity before touching it, and grandfather existing suppliers (`monetization.md`).
- Subsidies are a growth tool with an expiry: name the market, the amount, the duration, and the liquidity threshold at which it stops, before it starts. Subsidies without an exit condition become the business model by accident.

## Supply Growth

- Supply acquisition is usually **sales, SEO, and community**, not paid social — suppliers are looking for income and will respond to a channel that speaks to that.
- The supplier funnel is longer than it looks: signup → listing created → first transaction → second transaction. **First-transaction time** is the retention determinant; a supplier who waits weeks does not come back.
- Onboarding cost per supplier (verification, photos, training) is real CAC; count it (`acquisition.md`).
- Supply quality gates trade volume for liquidity: too loose and demand has a bad experience, too tight and there is nothing to buy. Set the gate by measured outcome (dispute rate, rating distribution), not by instinct.

## Demand Growth

- Demand is usually acquired on **intent channels** — search, marketplaces, comparison — because the need is explicit and timed.
- Programmatic pages per entity (city × category × attribute) are the highest-ceiling demand channel for most marketplaces, and the fastest to produce thin pages that never rank; each page needs unique value, usually the inventory itself (`seo`, `acquisition.md`).
- The first search is the moment of truth: an empty or poor result set on the first search costs the user permanently. Route new demand to dense categories and markets deliberately.
- Retention on the demand side is frequency-bound: for infrequent categories, the growth model is acquisition plus referral, not retention, and it should be planned that way (`retention.md`).

## Experimenting on a Marketplace

Standard user-level A/B tests are **biased by interference**: a treatment that helps some buyers win listings takes them from control buyers, so the measured effect overstates the true one.

- Use **market-level (cluster) randomisation** — treat whole cities or categories — or **switchback** designs that alternate treatment over time windows in the same market.
- Both cost statistical power, since the effective sample is markets or windows, not users. Plan for fewer, bigger tests (`experiments.md`).
- Never conclude from a user-level test that changes allocation of scarce supply; it is measuring redistribution, not creation.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Growing both sides at once from day one | Spreads a small budget over two funnels and achieves density in neither | Constrain the market; grow the constrained side |
| National launch | Liquidity is local; nowhere is dense | City by city, with a liquidity exit criterion |
| GMV as the north star | Rises while liquidity and experience fall | Liquidity per market, both directions |
| Spending on the abundant side | Lowers per-supplier earnings and accelerates their churn | Verify the constrained side with a spend test |
| Subsidy with no exit condition | Becomes the business model | Amount, duration, and threshold declared up front |
| Ignoring disintermediation in high-repeat categories | The platform becomes an introduction service people use once | Own the workflow, not the introduction |
| User-level A/B tests on allocation | Interference biases the result upward | Cluster or switchback designs |
| Blended national metrics | Hides three good markets and twelve empty ones | Everything per market |

**After any liquidity read or market launch**, write it back in the same turn: liquidity both directions, fill rate and time-to-first-transaction into `## Markets` in `~/Clawic/data/growth/memory.md` — one row per market, with its as-of date — and the currently constrained side **with the date it was checked** into `## Business`. Per-market rows never go into `## Funnel`: that section holds one row per funnel stage and splits to `funnel-history.md`, while `## Markets` splits to `markets.md`. Past ~15 markets, move the table to `markets.md` with the same columns and add its `## Boxes` line (`memory-template.md`). The market-launch playbook that worked is `artifacts/market-launch-playbook.md`, born as its own file; subsidy programs with their exit conditions go to the shared `~/Clawic/data/finances/budget.md` with currency and period.
