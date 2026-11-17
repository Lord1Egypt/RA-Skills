# The Rules That Bind a Price

Presentation, notice, and who you agreed the price with. A lawful price becomes unlawful through how it is shown, how it renews, and who you discussed it with.

Rules here change, and they differ by jurisdiction. **Everything in this file is a checklist of what to verify, not a substitute for the current text of the rule in the market you sell into** — the positions summarized were current as of 2026-07 and the direction of travel in every major market is toward stricter disclosure. Verify before a page ships.

**Before shipping a page, a renewal flow, or a promotion**, read `platform.markets` in `config.yaml` (which jurisdictions apply) and `price-book.md` (what is actually charged). **After confirming a jurisdiction's requirement**, write it to `artifacts/compliance-<market>.md` with the date checked and the source, and add its `## Boxes` line (`memory-template.md`).

## Auto-Renewal and Cancellation

The most enforced area in consumer subscriptions, and the one most often failed by accident.

| Requirement | What it means in the flow |
|---|---|
| Clear disclosure before purchase | Renewal term, amount, and frequency stated where the customer agrees, not in linked terms |
| Affirmative consent to the recurring charge | A separate, unbundled acknowledgement of the auto-renewal itself |
| Confirmation after purchase | The terms sent in a form the customer can keep |
| Cancellation as easy as signup | Sign up online, cancel online — no retention phone call as the only route |
| Advance notice before renewal | Commonly required for long terms, for free-to-paid conversions, and for any price change at renewal |
| Notice of a price change at renewal | Separate from the renewal notice, with the old and new amounts |

Practical defaults that satisfy most regimes at once: disclose at the point of sale, email a confirmation, send a reminder before any annual renewal and before any trial converts, and make cancellation reachable in the same number of clicks as signup. Retention offers are permitted; a retention offer that has to be declined before cancellation completes is where regimes diverge and where enforcement concentrates.

## Reference and "Was" Prices

- A struck-through prior price must be a price you genuinely charged, for a meaningful period, recently. The strictest common formulation is **the lowest price applied in the 30 days before the reduction**.
- Permanent "sales" and prices that were never charged are the pattern regulators pursue, because it is verifiable from your own site history.
- "From X" pricing requires a real, available quantity at X.
- Comparisons to a competitor's price must be to their actual current price for an equivalent product, and you should keep the evidence with the date you observed it — which is what `## Competitors` is for (`memory-template.md`).

## All-In Pricing and Mandatory Fees

- The direction in every major consumer market is that **mandatory fees must be in the headline price**. Service fees, booking fees, resort fees, and processing surcharges revealed at checkout are the specific target.
- Taxes are treated differently from fees: where prices are shown ex-tax by convention (US sales tax) that generally remains acceptable; a mandatory *fee* is not a tax.
- Optional add-ons may be added later, but the default state must not be pre-selected in a way that makes them functionally mandatory.
- The practical test: could a customer complete the purchase for the number shown at the top of the page? If not, that number is not the price.

## Personalized and Dynamic Pricing

- Prices that vary by **segment, geography, channel, or volume** are ordinary commercial practice.
- Prices that vary **by individual, derived from automated profiling**, carry disclosure duties for consumers in the EU, and reputational risk everywhere. Disclose, or price by segment instead.
- Dynamic pricing that responds to demand (travel, events) is accepted where the mechanism is understood; the same mechanism applied invisibly to a subscription is the case that generates complaints.
- Never vary price by a protected characteristic, or by a proxy that correlates with one. This is the failure mode of an unexamined model, not of a deliberate decision.

## Competition Law

The highest-consequence area in this file. The tripwires in SKILL.md, expanded:

- **Agreeing prices, discounts, or bids with a competitor** is unlawful in essentially every jurisdiction, with personal liability. There is no minimum company size and no informal-conversation exemption. Signalling future pricing publicly can also be treated as coordination.
- **Resale price maintenance** — dictating the price a reseller may sell at — ranges from per se unlawful to assessed case by case. An advertised-price policy announced unilaterally, with no agreement sought and no negotiation, is the usual lawful shape (`retail.md`).
- **Price discrimination between competing trade buyers** of the same goods is restricted in some jurisdictions. A published volume schedule, applied mechanically, is the standard defence and is also better commercial practice (`discounting.md`).
- **Most-favored-nation clauses** attract scrutiny and constrain you permanently; refuse or cap them tightly (`enterprise.md`).
- **Predatory pricing** — below-cost pricing to exclude a competitor — is only a risk with market power, but the internal document arguing for it is what makes the case.
- Trade association meetings and benchmarking exercises are the common setting for accidental exposure. Leave the room, and record that you left — the meeting, the date, and what was being discussed — in `artifacts/compliance-<market>.md`.

## Tax Display and Invoicing

Covered operationally in `international.md`; the compliance surface is:

- Consumer prices inclusive of VAT where required; business prices exclusive by convention with the tax added at invoice.
- Registration obligations can arise from sales volume alone, without physical presence; a merchant of record moves the obligation to the platform.
- Invoice content requirements (sequential numbering, tax identifiers, mandated e-invoicing formats) differ by market and stall deals when missing.
- B2B reverse charge inside the EU requires **validating** the customer's VAT number, not merely collecting it.

## Contract Terms That Bite Later

| Term | Risk |
|---|---|
| Price protection with no end date | A permanent grandfather that survives every future increase (`price-increase.md`) |
| "Prices may change at any time" with no notice mechanism | Unenforceable against consumers in many jurisdictions, and unusable in practice |
| Auto-renewal with a notice window shorter than the notice you must give | You cannot execute a lawful price change inside your own contract |
| Unlimited usage with no definition | Removes the value metric from the agreement (`usage-based.md`) |
| Most-favored-nation | Freezes future pricing freedom (`enterprise.md`) |

## Before a Page or Flow Ships

- Every mandatory fee is in the headline price.
- Renewal term, amount, frequency, and cancellation route are disclosed before purchase and confirmed after.
- Any "was" price is genuine, recent, and evidenced with its date.
- Cancellation takes no more steps than signup.
- Price-change notice periods meet both the contract and the local minimum, whichever is longer.
- Tax treatment matches the audience and the market (`tax_display`).
- No price was discussed with a competitor, and no reseller's resale price is being dictated by agreement.
- The jurisdiction check has a date and a source recorded in `artifacts/compliance-<market>.md`.

**Write the outcome**: each verified jurisdiction requirement, with the date checked and the source, to `artifacts/compliance-<market>.md`; notice periods and renewal-notice windows into `price-book.md` alongside the terms they govern; any recurring re-verification to `## Due` (`memory-template.md`).
