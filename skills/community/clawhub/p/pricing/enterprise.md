# Enterprise and Sales-Led Pricing

A quoted deal is a price plus a set of terms, and the terms are where the money moves. Procurement negotiates the terms because the price is the part you defend.

**Before quoting**, read `price-book.md` (list, floor, approval authority), `## Deals` in `~/Clawic/data/pricing/memory.md` (what comparable accounts got — inconsistency is what procurement looks for), and `contacts.md` for who you are dealing with. **After the deal**, write the row to `## Deals` with discount, term, what was traded, and who approved; the customer goes to `~/Clawic/data/contacts/contacts.md`; the rate card sent goes to `artifacts/rate-card-<customer>.md` (`memory-template.md`).

## The Three Numbers Before the Call

Fixed before any conversation, written down, and not adjusted during it:

1. **List** — the published or reference price for the scope requested.
2. **Floor** — the lowest price you will accept for that scope, from the contribution margin (`elasticity.md`). It lives in `price-book.md`.
3. **Walk-away** — the point where the deal costs more than no deal: implementation load, support burden, custom commitments, opportunity cost of the team's time.

A negotiator without a floor concedes to whoever has more patience. The floor is also the honest answer to "is that your best price": yes, at this scope.

## Structure of a Quote

| Element | Default | Why it matters |
|---|---|---|
| Term | 12 months | Multi-year only with an uplift clause and a discount that reflects the risk transferred |
| Payment | Annual, in advance | Monthly billing on an annual contract is a financing service; price it or refuse it |
| Uplift | A stated annual increase for multi-year terms | Without it, year three is priced at year-one economics and the renewal is a fight |
| Auto-renewal | With notice, and a notice window the customer can actually use | Renewal traps are a compliance and reputation risk (`compliance.md`) |
| Scope | Enumerated: metric, allowance, environments, support tier | Undefined scope is a discount that grows after signature |
| Price protection | Capped and time-boxed if given at all | "Prices will not increase" with no end date is a permanent grandfather |
| Effective date | Explicit | SKILL.md Rule 6 |

For multi-year uplift, an index-linked clause (a published inflation index, with a floor and a cap) survives procurement scrutiny better than a flat percentage, because it is defensible as a rule rather than as your preference.

## What Procurement Will Ask For, and the Answer

| Ask | What it really does | Response |
|---|---|---|
| "What's your best price?" | Tests whether the first number was real | The floor for this scope, or a smaller scope at a lower price. Never a new number for the same scope |
| Most-favored-nation clause | Freezes your pricing freedom against every future customer | Refuse; if unavoidable, cap it by scope, term, and comparable-deal definition (SKILL.md, Legal Tripwires) |
| Unlimited users, unlimited usage | Removes the value metric from the contract | Price a very large commitment, never an unbounded one |
| Price protection for the life of the agreement | A permanent grandfather | Time-boxed, capped uplift instead |
| Payment terms of 90+ days | A loan at your expense | Trade against the discount: shorter terms buy a better price |
| Custom SLA with penalties | Real cost and real risk | Price it as a line item; a credit-based SLA is cheaper than a penalty-based one |
| Security review, DPA, custom contract | Weeks of somebody's time | Fine, but it is scope: it belongs in the tier that funds it |
| Signature at the end of your quarter | Your urgency, priced | Never discount for a date (`discounting.md`) |

## Trading, Not Conceding

Every concession is exchanged. The ledger, roughly:

- Longer term → discount, with uplift.
- Prepayment → discount worth the cash value.
- Larger committed volume → published volume-schedule rate.
- Reference, case study, or a customer advisory seat → one-off first-year concession.
- Faster procurement path or a lighter security review → nothing given; that is their saving, not yours.
- Reduced scope → a lower price on a smaller product. This is the concession that costs nothing and is used least.

If a concession has no counterpart, say what it costs: "I can do that; it moves us to a two-year term." That sentence is the whole discipline (`negotiate` covers the conversation itself).

## Multi-Year Deals

- Discount for a multi-year term reflects **risk transferred**, not term length. A two-year commit removes one renewal from risk; three removes two, and adds the chance that your product is mispriced by the third year.
- Always include the uplift, and state it in the first quote rather than introducing it after agreement in principle.
- Model the deal's net present value against the same customer renewing annually at list with your observed renewal rate. Many multi-year discounts are worse than the churn they insure against.
- Ramp deals (commit rising by year) are how a customer buys capacity they will grow into; each step goes into `## Due` so both sides see it coming.

## Renewals

- Start the renewal conversation before the notice window opens, not at it. A renewal negotiated under a deadline is negotiated by the party with less to lose.
- **Renewal price starts from list, adjusted by the uplift clause** — never from last year's discounted number. This is why the uplift belongs in the original contract.
- Expansion is easier than a raise: more seats, more usage, a higher tier fenced by something they now need. Sequence expansion first, price second.
- A customer who threatens to leave at renewal every year has learned that it works. The `## Deals` history is what makes that pattern visible.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Discounting before the scope is defined | The scope then grows into the discount | Scope, then price, then trade |
| No uplift clause on a three-year deal | Year three runs on year-one economics and the renewal starts from there | Index-linked uplift with floor and cap |
| Accepting an MFN to close | Constrains every future deal, invisibly and permanently | Refuse, or cap tightly |
| Inconsistent discounts across comparable accounts | Procurement teams talk, and the inconsistency becomes the negotiation | A published volume schedule applied mechanically |
| "Pilot pricing" with no exit price | The pilot price becomes the contract price by default | State the post-pilot price in the pilot agreement |
| Quoting without an expiry on the quote | The quote is used against you a year later | Every quote carries a validity date (SKILL.md Rule 6) |
| Letting the deal terms live only in the contract | Nobody pricing the next deal can see what was actually given | `## Deals` row in the same turn |

**Write the outcome**: the deal to `## Deals` (list, agreed, discount, traded, term, approver); any breach of the price-book floor to `## Floor Exceptions`; the customer to the shared `contacts.md` by key; the rate card or quote template to `artifacts/`; every ramp step, uplift date and renewal notice window to `## Due` (`memory-template.md`).
