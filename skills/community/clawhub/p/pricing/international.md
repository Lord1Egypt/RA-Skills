# Currency, Purchasing Power, and Tax

Selling into a second country is a pricing decision before it is an operations decision. Three things change at the border: what the number is, what it includes, and who owes the tax.

**Before pricing a new market**, read `price-book.md` (existing markets and their prices), `## Competitors` in `~/Clawic/data/pricing/memory.md` for local alternatives, and `platform.markets` plus `tax_display` in `config.yaml`. **After the decision**, write the band table into `price-book.md` and the rationale to `artifacts/decision-market-<country-or-region>.md` with its `## Boxes` line (`memory-template.md`).

## Never Convert at Spot

Spot conversion produces prices like 47.13, ignores what the market will bear, and moves every time the exchange rate does. Use **bands** instead:

1. Group countries into three to five bands by purchasing power and by what local competitors charge — not by geography.
2. Set one price per band, in the local currency, at a **local price point** (the ending conventions differ: what looks natural in one market looks broken in another).
3. Fix the local price and let the exchange rate move underneath it. Review on the price-review cadence, not continuously.
4. Rebalance only when the drift exceeds a stated threshold — around 10-15% is a common trigger — and then as an announced price change, not a silent one.

Discounts for lower-income markets are usually deep: a 30-70% reduction against the home-market price is common where a full-price product would be unaffordable. The band, not the individual country, is what you defend.

## Arbitrage

Any price gap invites people to buy from the cheaper market. The rule that works: **the discount must be smaller than the friction of faking location**, or the friction has to be raised.

| Control | Strength | Cost |
|---|---|---|
| Billing-address and payment-method country | Moderate; the standard first line | Blocks legitimate travellers and expatriates |
| Local payment methods only in low-price bands | Strong — a local method usually requires a local bank account | Reduces conversion for everyone else in that band |
| Tie the price to the account's country, set once and rarely changed | Moderate; removes casual switching | Support load on genuine relocations |
| Regional feature or support differences | Weak as a control, honest as a rationale | Complexity |
| Nothing, and accept the leakage | Correct when the low-price band is small | Uncapped if the gap is large |

For business software, the leakage is usually small and the revenue from serving the market at all is larger. For consumer subscriptions with easy account creation, it is not.

## Tax: Inclusive or Exclusive

`tax_display` governs how every quoted price is shown, and the correct value is jurisdiction- and audience-dependent:

- **Consumers in the EU and UK** must be shown the total payable price including VAT. A price shown ex-VAT to a consumer is a compliance issue, not a presentation preference.
- **Business buyers** conventionally see prices excluding VAT, with the tax added at invoice, because they reclaim it.
- **The US has no VAT**; sales tax is added at checkout and varies by state and locality, so US prices are quoted excluding tax by convention.
- Selling to both audiences from one page means either two views (detected by country and business status) or a clearly labelled toggle. Showing one number and charging another is where the complaints start.

## Who Collects the Tax

| Setup | Who owes the tax | Practical effect |
|---|---|---|
| You sell directly | You register, collect, file and remit in each jurisdiction where you have an obligation | Registration thresholds differ; the obligation can arrive from volume alone, without any physical presence |
| Merchant of record | The platform is the seller and owns the tax obligation | Simplest; costs a percentage of revenue, which is a real input to `target_gross_margin_pct` |
| Marketplace facilitator | The marketplace collects on your behalf | Common for app stores and large marketplaces; check what remains yours |

For B2B sales inside the EU, a valid VAT number from the buyer usually shifts the liability to them (reverse charge) — which means validating the number, not just collecting it. Thresholds, rates, and registration rules change; verify the current position for each market before it goes into a model, and record the checked figure with its date in `## Cost Inputs`.

## Local Expectations Beyond the Number

- **Payment methods** are a conversion lever, not an afterthought: card penetration, bank transfer, direct debit, and local wallets vary enormously by market. A market where your only method is a card is a market where you are pricing against friction.
- **Billing cycle preference** differs; annual-first is normal in some markets and rare in others.
- **Formatting**: decimal separator, thousands separator, currency symbol position, and the digit conventions that read as "cheap" locally. A price written the wrong way looks like a foreign product, because it is one.
- **Invoicing requirements** — company registration number, tax ID, sequential invoice numbering, e-invoicing mandates — are a reason deals stall in some markets, and they are cheaper to solve before the first customer than after.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| One USD price for the world | Prices out entire markets and overcharges none of them profitably | Bands with local prices |
| Converting at spot and rounding to two decimals | 47.13 signals a foreign product and moves every month | Fixed local price points, reviewed on cadence |
| Showing ex-tax prices to consumers | A compliance problem in several jurisdictions and a trust problem everywhere | `tax_display: inclusive` for consumer markets |
| Ignoring registration thresholds until an accountant asks | Back taxes and penalties accrue from the date the obligation started | Record each market's threshold and the date it was checked in `## Cost Inputs`, or use a merchant of record |
| Deep regional discounts with no arbitrage control | The gap gets published and the cheap price becomes the global price | Match control strength to gap size |
| Rebalancing prices every time the rate moves | Every change is a communication event; customers stop trusting the number | A drift threshold, then an announced change |
| Assuming the low band is not worth serving | Volume markets fund development and produce reference customers | Price for the band, measure separately |

**Write the outcome**: band tables and local prices to `price-book.md`; the market decision, the arbitrage posture and the tax setup to `artifacts/decision-market-<country-or-region>.md`; merchant-of-record fees and tax-registration facts to `## Cost Inputs` with dates; the currency-drift review to `## Due` (`memory-template.md`).
