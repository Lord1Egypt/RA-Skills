# The Pricing Page and How Prices Are Shown

The page is where packaging either becomes obvious or becomes a support ticket. Everything here assumes the tiers and fences are already decided (`packaging.md`).

**Before writing a page**, read `price-book.md` (the prices, fences and effective date the page must match exactly) and `price_endings`, `currency` and `tax_display` in `config.yaml`. **After a page that measurably converted**, save it to `artifacts/pricing-page-<yyyy-mm>.md` with what changed and the result, and add its `## Boxes` line (`memory-template.md`).

## Structure That Works

1. **Prices visible without interaction.** A page that requires a toggle, a slider, or a form before showing a number loses the visitor who came to check whether you are in their range.
2. **Left to right, cheapest to most expensive**, with the anchor at the end. The buyer reads in one direction and the last number should be the largest.
3. **One highlighted tier**, and it is the one you want most buyers in. Highlighting the most expensive reads as a sales tactic; highlighting nothing wastes the strongest cue on the page.
4. **A comparison table of differences only** — six to eight rows. Everything shared across tiers goes in a single "everything includes" line above or below.
5. **Annual/monthly toggle with the saving stated in the toggle itself** ("Annual — 2 months free"). Defaulting to annual raises average contract value; defaulting to monthly raises trial starts. Pick deliberately and record which (`config.yaml`).
6. **FAQ under the table**, answering the objections sales actually hears: what happens when I exceed the limit, can I change plans, what happens to my data if I downgrade, do you offer invoicing.
7. **The enterprise door last**, with a qualifier so unqualified traffic self-selects out ("From X per year").

## Writing the Number

- `price_endings` governs the last digit everywhere. Charm endings (49, 99) signal value and are read as a lower magnitude because of the leading digit; round endings (50, 100) signal premium and quality. Mixing them across a page destroys both signals.
- **Consistency beats cleverness**: 19 / 49 / 99 reads as a system. 19 / 47 / 100 reads as three unrelated decisions.
- Show the unit and the period on every price: `49 / editor / month`. A number with no unit is the most common source of "that's not what the page said".
- **De-emphasize the currency symbol and any decimals** typographically; keep the digits dominant. Prices with unnecessary trailing zeros read as longer, and longer reads as more.
- Anchor with the comparison you want: crossed-out prior price only when it is a genuine prior price recently charged (`compliance.md`), or the annual equivalent alongside the monthly.
- **Per-day framing** ("less than 2 a day") is legitimate only next to the real billed amount, never instead of it.

## What to Show and What to Withhold

| Show | Withhold |
|---|---|
| Prices for every self-serve tier | Nothing that changes the total at checkout |
| What each limit is, in the unit the buyer counts | Internal metric names nobody outside recognizes |
| Whether tax is included, and for whom | — |
| What happens at the limit (soft cap, alert, overage rate) | — |
| Term, notice period, and how to cancel | — |
| A starting figure for enterprise | The full enterprise rate card, if scope genuinely varies |

**Fees revealed at checkout are the single most damaging pattern on this page**, commercially and legally: they raise abandonment and they attract enforcement in several jurisdictions (`compliance.md`). If a fee is mandatory, it is part of the price.

## Public Price or "Contact Us"

| Publish | Route to sales |
|---|---|
| Self-serve, uniform scope, small to mid ACV | Scope varies enough that a list price would be wrong for most buyers |
| The buyer is a practitioner who will not fill in a form | Procurement-led purchase where a conversation is required anyway |
| You want to filter out buyers you cannot serve | Deal value justifies the cost of the conversation |

The hybrid — publish the self-serve tiers, route enterprise — is the default because it does both. A fully hidden price costs top-of-funnel volume and is chosen for negotiating room; be honest about which reason applies.

## Cues That Earn Their Space

- **"Most popular"** on a tier that genuinely is. Placed on a tier nobody buys, it is discovered the first time someone asks.
- **A guarantee** with a stated window and a real process reduces perceived risk more than any copy on the page.
- **Trust marks** relevant to the buyer's actual objection: security certification for IT buyers, customer logos for peers, uptime figures for infrastructure buyers.
- **Live usage or seat calculators** where the metric is countable. A calculator that produces a number the buyer recognizes does more than any feature row.
- Everything else — badges, awards, unexplained statistics — is space the comparison table needed.

## Accessibility and Correctness

- The page and the invoice must agree. A price book with an effective date (`price-book.md`) and a page that was not updated is a refund conversation.
- State the effective date of a change on the page while a migration is running, so existing customers understand which number applies to them (`price-increase.md`).
- Comparison tables need real table semantics and a readable layout on a phone — the majority of first visits, and the layout where a wide feature grid becomes unusable.
- Localize the currency, the format and the tax treatment together (`international.md`). A local currency with foreign number formatting is worse than neither.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Twenty-row feature table | The comparison stops being resolvable; the visitor leaves to think about it | Differences only, details behind a link |
| Toggle or slider required before any price appears | The visitor who wanted a range leaves without one | Show a default state with real numbers |
| "Most popular" on a tier nobody buys | Found out immediately by anyone who asks | Label the tier that actually is |
| Mandatory fees at checkout | Abandonment plus enforcement exposure | All-in price on the page |
| Mixed price endings across tiers | Neither the value nor the premium signal survives | One convention, from `price_endings` |
| Page and invoice disagree | Refunds and lost trust, at scale | Page generated from, or checked against, `price-book.md` |
| Crossed-out price that was never charged | A prior-price claim with rules attached | Only genuine, recent, sustained prior prices (`compliance.md`) |

**Write the outcome**: the page that converted, with what changed and the measured result, to `artifacts/pricing-page-<yyyy-mm>.md`; the test behind it to `## Experiments`; any price shown to `price-book.md` first, never the other way round (`memory-template.md`).
