# Packaging — Tiers, Fences, and Add-Ons

Packaging decides who buys which thing. The price is the last step, and it is the easy one.

**Before packaging or repackaging**, read `price-book.md` (what exists and what each tier gates) and `## Competitors` in `~/Clawic/data/pricing/memory.md`. **After the decision**, write it to `artifacts/decision-packaging.md` with what was rejected, update `price-book.md`, and add the `## Boxes` line in the same turn (`memory-template.md`).

## Segments First, Tiers Second

A tier is not a size, it is a segment with a name. Build in this order:

1. **Name the segments** by what they cannot do without, not by headcount. "Needs SSO because IT owns procurement" is a segment; "50-200 employees" is a filter.
2. **Find the fence** each segment cannot cross: a capability the segment above must have and the segment below genuinely does not want. Real fences: SSO/SAML, audit log, SLA and support response time, data residency, retention window, API rate, role granularity, seats, environments, invoicing versus card.
3. **Only then set prices**, ordered so the anchor sits above the target.

If two tiers differ only by a quantity, you have one tier with a slider, not two tiers.

## How Many Tiers

Three public tiers plus a quoted enterprise door is the working default. Reasons, not fashion:

- Every additional tier adds a comparison the buyer must resolve before acting, and comparisons are where self-serve funnels lose people.
- Three positions let you place an anchor (top), a target (middle), and an entry (bottom) without inventing a segment.
- "Enterprise — talk to us" is a routing device, not a fourth tier: it has no published price precisely so scope can vary.

Go to four public tiers only when a real segment cannot be served by any of the three — a genuine free plan, or a distinct usage class with a different cost base. Two tiers is correct when the product serves one segment and the only variation is volume.

## The Anchor and the Target

- The **top tier anchors**: it makes the target's price legible. It must be a real product a real customer buys, not a decorative price. A top tier that nobody has ever bought is discovered by the first prospect who asks who uses it.
- The **middle is designed to be chosen** by the segment you want, which means its fences must fit that segment exactly. Do not rely on folklore about middle options being picked; rely on the fence.
- **Asymmetric dominance** (the decoy effect, Huber/Payne/Puto) is real and narrow: an option that is clearly worse than the target on every dimension and similar in price makes the target easier to choose. It is a presentation tactic for a comparison table, not a reason to ship a product nobody should buy.

## What to Gate, and What Never to Gate

| Gate upward | Never gate |
|---|---|
| Scale: seats, volume, environments, projects | Security basics: 2FA, encryption at rest, password policy |
| Control: SSO, SCIM, role granularity, audit log | Data export — gating the exit reads as a hostage arrangement and it is what gets screenshotted |
| Assurance: SLA, support response, uptime credits, named contact | Bug fixes, or a rate limit so low the product cannot be evaluated |
| Compliance: data residency, retention, BAA/DPA depth | Anything a customer already pays for today (removing it is a raise plus a downgrade) |
| Integrations that cost you to run and maintain | The core job the product exists to do |

Charging separately for SSO is the loudest of these debates. The defensible version: SSO belongs in the tier the *IT-governed* segment buys, priced as part of that segment's package, not as a 3× multiplier bolted onto a small plan.

## Add-Ons vs Tiers

| Use a tier | Use an add-on |
|---|---|
| The capability defines a segment | The capability is wanted by a minority of every segment |
| It correlates with willingness to pay across the board | It has its own marginal cost (extra storage, a paid third-party dependency, professional services) |
| Bundling it raises the tier price for everyone credibly | Bundling it would inflate the tier price for people who will never use it |

Cap the add-on count. Past roughly three or four, the quote becomes a configuration exercise and self-serve conversion drops; that is the moment the add-ons should have been a tier.

## Naming

- Name for the buyer, not for the size: `Starter / Team / Business` tells someone which one is theirs. `Bronze / Silver / Gold` tells them only that they are not gold.
- Never name a tier after a feature that will move between tiers later.
- Keep the seat noun consistent everywhere (`seat_word` in `config.yaml`): the pricing page, the invoice, and the in-product limit message must use the same word or every limit becomes a support ticket.

## Repackaging an Existing Product

1. Map current customers onto the proposed tiers using their actual usage and entitlements — not what they bought, what they use.
2. Count how many would lose something. Anyone who loses an entitlement they pay for today is a churn risk and a public complaint; leave existing entitlements intact and gate only new capability upward.
3. Price the new tiers, then run each affected cohort through the break-even of SKILL.md Rule 2.
4. Sell only the new packaging to new customers from day one; migrate existing ones at renewal (`price-increase.md`).
5. Record which cohorts stayed on which packaging, and until when, in `## Price History`.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Tiers that differ by quantity alone | Buyers pick the cheapest and grow into it for free; nobody upgrades on principle | One fence per boundary that a segment must cross |
| A decorative top tier | The first prospect who asks who buys it learns the whole page is theatre | The anchor must be a product someone actually buys |
| Feature lists twenty rows deep | The comparison stops being resolvable and the buyer leaves to "think about it" | Six to eight rows, differences only; details behind a link |
| Removing a feature to build a higher tier | Reads as a raise and a downgrade at once | Gate new capability upward, grandfather what exists (`price-increase.md`) |
| Add-ons for everything | Turns self-serve into configuration; discounting starts as a way to simplify the quote | Fold the popular add-on into the tier at the next price review |
| Copying a competitor's tier structure | Imports their segments, which are not yours | Fences from your own win/loss reasons (`research.md`) |

**Write the outcome**: the packaging decision and its rejected options go to `artifacts/decision-packaging.md`; the tiers, fences and prices go into `price-book.md`; any entitlement change becomes a row in `## Price History` (`memory-template.md`).
