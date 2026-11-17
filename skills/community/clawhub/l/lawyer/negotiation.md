# Negotiating Legal Terms

Legal negotiation is not commercial negotiation with jargon. The currency is risk allocation, the counterparty is usually a lawyer with a playbook and no economic stake in the deal, and the clock is owned by whichever side has a quarter-end.

**Before the first counter**, read `## Positions` in `~/Clawic/data/lawyer/memory.md` for the standing fallback set and anything already conceded to this counterparty, plus `## Contracts` for the existing relationship. `risk_posture` sets how far down each ladder to go; `default_side` sets the starting column in `clauses.md`.

**Contents:** [Who Is On The Other Side](#who-is-on-the-other-side) · [The Issues List](#the-issues-list) · [Trade Ladder](#trade-ladder) · [What Is Actually A Walk-Away](#what-is-actually-a-walk-away) · [Leverage And Where It Comes From](#leverage-and-where-it-comes-from) · [Moves That Work](#moves-that-work) · [Moves Used Against You](#moves-used-against-you) · [Escalation Without Losing The Deal](#escalation-without-losing-the-deal) · [Closing](#closing)

## Who Is On The Other Side

The right move depends on who is holding the pen, and this is knowable from the first email.

| Counterparty | Signal | What works |
|---|---|---|
| In-house counsel with a playbook | Fast, structured responses; "our position is" language | Ask which fallback exists — they usually have three approved positions per clause and will give you the second one for asking |
| Outside counsel billing hourly | Long redlines, every clause touched, slow turnarounds | Reduce the issue count; their client is paying for each round and will push for closure |
| Procurement, no lawyer | Focus on price, insurance certificates, and forms | Legal asks land easily; commercial asks do not |
| The founder or the account executive | Enthusiasm, no redline discipline | Get the agreement in writing quickly, before it reaches their lawyer with the deal already promised |
| A platform with click-through terms | No response channel at all | There is no negotiation; do the review that fits (`review.md`) |

## The Issues List

Never negotiate a document; negotiate a numbered list. Six or fewer issues close in one or two rounds; twenty-item redlines produce a call, then a delay, then a second redline.

Build it as a table the other side can approve line by line: issue, clause reference, our position, why (one sentence, commercial not legal), and fallback if they refuse. Sort by exposure, not by clause order — the reader stops caring after item four, so item four must not be the notices address.

Rank issues into three tiers before sending:

- **Tier 1, must have** — the ones where the answer decides whether to sign. Typically the cap and its carve-outs, the IP position, and the exit.
- **Tier 2, want** — real money but survivable. Payment terms, audit scope, insurance limits, price-increase caps.
- **Tier 3, free** — cheap for them to give and worth having. Notices by email, mutuality of a one-sided clause, precedence order, cure periods.

Send tiers 1-3 together in the first pass. Holding tier 3 back for a second round adds a week for nothing and looks like bad faith.

## Trade Ladder

Concessions are paid for, never given. Each of these costs the other side little and is worth something real:

| Give | Get |
|---|---|
| Longer term (24-36 months) | Price lock, a convenience exit at 12 months, a lower cap multiple |
| Annual prepayment | Discount, plus better leverage on the cap because "fees paid" is now the full year |
| Reference or case study rights | Almost anything legal — marketing wants this more than legal wants the clause |
| Faster payment terms (net 15) | Discount or a concession on audit scope |
| Narrower indemnity scope for them | Supercap for you |
| Their governing law | Your forum, or arbitration in a neutral seat |
| Accepting their template as the base | Your positions on the three tier-1 clauses |

The last row is the highest-value trade in the game: whose paper is the base is worth less than what is in it, and conceding the base buys goodwill for the clauses that matter.

## What Is Actually A Walk-Away

A walk-away is a term that makes the deal worse than no deal. That set is small, and inflating it burns credibility. Candidates:

- Uncapped liability with no exclusion of consequential damages, at a contract value that would not survive one claim
- An IP assignment that captures the user's own platform or background IP
- Exclusivity with no minimum volume and no time limit
- A personal guarantee, or security over personal assets, on a company obligation
- Indemnity for the counterparty's own negligence or their regulatory fines
- A term that directly contradicts a commitment already made to another counterparty (`review.md`, absence review)

`risk_posture` moves the boundary: `conservative` treats an uncapped confidentiality obligation as a walk-away; `commercial` treats it as a tier-2 trade backed by insurance. State which posture is being applied when a walk-away is declared.

## Leverage And Where It Comes From

Leverage is almost never legal. Sources, in rough order of strength: a real alternative (a second vendor in procurement, a second customer in the pipeline), timing (their quarter-end, your renewal date, a launch), switching cost accumulating on their side, information asymmetry about your actual constraints, and relationship capital with a person who wants this to happen.

The corollary: if the user has no alternative and their deadline is public, the correct advice is often to accept tier-2 and tier-3 positions quickly and spend all remaining capital on one tier-1 issue. Fighting every clause from a weak position produces a worse contract *and* a slower one.

## Moves That Work

- **Name the number, not the principle.** "Our cyber policy limit is $2M; we cannot indemnify above what we can insure" ends a discussion that "we need a cap" continues for two rounds.
- **Offer a mechanism instead of a position.** Deadlocked on price increases? Cap them at an index. Deadlocked on the cap? Tie the supercap to the insurance certificate. Mechanisms let both sides claim they held their line.
- **Reciprocity as the default frame.** Ask for mutuality on every one-sided clause. It is rhetorically hard to refuse and often reveals which clauses the other side actually cares about — they will fight mutuality only where they expect to be the breaching party.
- **Concede visibly and immediately on tier 3 items you were never going to fight.** It buys a round.
- **Put the deadline on the table honestly.** "We need this signed by the 28th" is information both sides can plan around; discovering it on the 27th is a concession extractor.
- **Ask what their approval path is.** A term the other lawyer cannot approve alone will take a week no matter how reasonable it is; knowing that reprioritises which fights to pick.

## Moves Used Against You

| Move | What it looks like | Counter |
|---|---|---|
| "That's our standard, we never change it" | Flat refusal on the first ask, no reason | Ask what the approved fallback is. Standard paper almost always has one |
| Deadline manufactured on their side | "Pricing expires Friday" | Pricing that expires is a discount, not a contract term. Ask for the discount to be held; if it cannot be, it was leverage, not a deadline |
| The late-stage addition | A new exhibit or policy appears in the "final" version | Diff every version (`review.md`); ask when it was added and why |
| Nibble at signature | One more small change while the pen is out | Everything reopens together, or nothing does |
| Escalation to your executive over legal's head | Their VP calls your CEO about "legal blocking the deal" | Give your executive the two-line version and the exposure number before the call happens, not after |
| Incorporation by URL | "subject to our standard policies at example.com/terms" | Pin to a dated version (SKILL.md Rule 8) |
| Volume of redlines as attrition | 60 tracked changes, most cosmetic | Answer with the numbered issues list; do not respond change by change |

## Escalation Without Losing The Deal

When two lawyers deadlock, the escalation is to the commercial owners, and it works only if it is framed in money and time. The message: here is the clause, here is the exposure in currency, here is what we asked for, here is what they offered, here is the cost of accepting and the cost of walking. Both business owners then decide, which is correct — risk allocation is a business decision that lawyers price, not one they make.

Escalate early rather than late. An issue escalated in week one gets a decision; the same issue escalated the day before signature gets accepted because the deal has momentum.

## Closing

- Confirm the final version in writing, by document hash or filename plus date, before signature. "Attached final" without a version reference is how the wrong draft gets signed.
- Re-run the Output Gates against the final version, not the version that was negotiated. Changes made during closing are the least reviewed changes in the document.
- Signature block, authority, and entity names checked one last time (SKILL.md Rule 7).

**After the negotiation closes**, write in the same turn (`memory-template.md`): every position taken and its outcome into `## Positions` in `memory.md`, the agreement row into `## Contracts` with all computed dates into `## Due`, and the counterparty's negotiating behaviour (playbook depth, who approves, what they traded) as one line in `## Pain Points` or the counterparty's `## Positions` entry. The second negotiation with the same company should start where the first one ended, not from the template.
