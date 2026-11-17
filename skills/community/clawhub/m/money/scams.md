# Scams, Fees, and Bad Products

**Before answering**, read `## Pain Points` in `~/Clawic/data/money/memory.md` — a household that has been defrauded before responds differently, and repeating the analysis that already failed them is worse than useless. Re-targeting of previous victims is a documented pattern, so a past loss raises the prior on a new approach being fraudulent.

Three distinct problems live here and the responses differ: **fraud** (criminal, aims to take the money), **conflicted advice** (legal, aims to take a share of it), and **bad products** (legal, priced far above their value). Diagnose which one before responding.

## The Signals That Are Almost Never Wrong

| Signal | Why it works on people | Response |
|---|---|---|
| A deadline inside 24-72 hours | Removes the time in which the story falls apart | No legitimate opportunity expires over a weekend. The deadline **is** the evidence (SKILL.md Red Flags) |
| Guaranteed returns, especially above deposit rates | Guarantee and return are the two things that cannot be combined | Ask who guarantees it and with what capital; the answer ends the conversation |
| Returns that are steady month after month | Real assets are volatile; smooth returns usually mean the numbers are produced rather than earned | Smoothness is a stronger fraud signal than a high return |
| Pressure to keep it confidential | Isolates from the one person who would spot it | Any request for secrecy is disqualifying on its own |
| It came through someone trusted — a community, a congregation, a friend, a relative | Affinity fraud borrows credibility rather than building it | The introducer's sincerity is not evidence; they are often an earlier victim |
| Contact initiated by them — call, message, dating app, "wrong number", social media | The single most common vector | Never transact on inbound contact. Hang up and call back on a number you find yourself |
| Small withdrawal works, then a larger deposit is invited | Builds trust cheaply; the classic structure of long-form investment fraud | A successful test withdrawal is part of the design, not reassurance |
| A fee, tax or "release payment" required before the money can be released | Advance-fee fraud, including recovery scams targeting earlier victims | Legitimate proceeds are never gated behind a payment you make |
| Complexity presented as sophistication | Prevents evaluation; hides the fee | If it cannot be explained in three sentences, the answer is no |
| Urgency plus authority — tax office, bank fraud team, police | Panic suppresses verification | No real institution asks you to move money to a "safe account". That request is definitionally fraud |
| Crypto, gift cards, or an overseas transfer as the payment method | Irreversible by design | The payment method chosen tells you the intent |

## The Verification Sequence

Applied to every unsolicited financial approach, in order, and it costs ten minutes:

1. **Stop the clock.** State that no decision happens today. Everything that survives this step is fine; everything that does not was the answer.
2. **Verify the firm on the regulator's own register in `country`**, reached by typing the regulator's address yourself. Clone firms copy a real firm's name and registration number and change only the contact details.
3. **Check contact details against the register**, not against the ones supplied. This single step defeats clone fraud, which is otherwise very hard to spot.
4. **Search the name plus "scam", "review", "warning"**, and check the regulator's warning list.
5. **Ask how the person in front of you is paid.** Commission, a share of assets, a flat fee, or a spread. Anyone who will not answer plainly has answered.
6. **Tell one other person before moving money.** Isolation is the shared precondition of every large loss.
7. Never install remote-access software, share a screen, or read out a code sent to you. A code sent to you authorises something; reading it aloud authorises it for someone else.

## Conflicted Advice, Which Is Legal

Most money lost to advice is lost legally.

| Structure | The incentive it creates |
|---|---|
| Commission on product sales | Recommend the product that pays, and recommend switching |
| Percentage of assets under management | Discourage anything that reduces the assets: paying off a mortgage, buying an annuity, giving to family |
| Percentage plus underlying fund fees | Two layers, priced separately, presented as one. Ask for the all-in figure (`investing.md`) |
| Flat fee or hourly | Aligned on the advice; the client implements, which not everyone will do |
| "Free" review, seminar, or webinar | The product is the attendee |

The question that cuts through: **"What do you earn if I do nothing?"** An adviser who earns the same either way is giving advice. One who earns nothing is selling.

Two structural checks worth more than any credential: is the money held by an independent custodian, or by the same firm giving the advice (a single entity holding both is the structure behind the largest frauds in history), and is the adviser held to a fiduciary-equivalent standard in `country` or only to a suitability standard.

## Products That Are Legal And Usually Wrong

- **Investment bundled with insurance** — whole-of-life, unit-linked savings plans, endowment-style products. High costs, long lock-ins, exit penalties, and an opacity that hides both (`insurance.md`).
- **Structured products with capital "protection"** — the protection is only as good as the issuer, the upside is capped, and the fee is in the construction rather than on a statement.
- **Leveraged trading, CFDs, spread bets** — the retail loss rates disclosed on these firms' own marketing are the disclosure that matters; read the number on the page.
- **Anything paying for recruitment rather than for sales to outside customers.** That structure is a pyramid regardless of the product attached to it, and it fails arithmetically once the market saturates.
- **Timeshares, land banking, storage pods, carbon credits, fine wine and similar "alternatives"** sold by cold contact. The pattern is a real underlying asset, an unsellable retail slice of it, and no secondary market.
- **Tax schemes with a fee** — aggressive arrangements have a long record of being unwound years later with interest and penalties charged to the taxpayer, not to the promoter (`taxes.md`).
- **Debt-settlement and credit-repair firms charging up front** for things the individual can do free through statutory or non-profit routes (`debt.md`).

## If Money Has Already Gone

1. Contact the bank or card issuer immediately and ask them to attempt recall — the window is measured in hours for transfers and is longer for card payments, where chargeback rights may apply.
2. Report to the police or the national fraud reporting service, and to the regulator. Get reference numbers.
3. Freeze the credit file at every bureau if identity data was exposed (`credit.md`).
4. Change credentials on every account that shared a password, storing only pointers (`keychain:...`).
5. Document everything with dates: messages, names, account numbers used, amounts, times.
6. **Expect a recovery scam.** Victim lists circulate, and the follow-up approach offers to recover the loss for a fee. No legitimate recovery service asks for payment up front.
7. Reimbursement rules for authorised push-payment fraud differ by `country` and have tightened in several markets — check the current rule before assuming the loss is final.

## Protecting Someone Else

Financial abuse of an older or vulnerable relative is a Red Flags item. Warning signs: new "friend" or carer involved in the finances, sudden changes to a will or a power of attorney, unexplained withdrawals, isolation from family, secrecy about money that used to be open.

Available controls, all of them undramatic: a trusted-contact registration with the bank, a view-only account for a family member, transaction limits and confirmation calls, a credit freeze, and a power of attorney set up in advance while capacity is not in question. Then the local adult-safeguarding route (`household.md`).

**Write it down.** An approach identified, a product declined and the reason go as a row in `~/Clawic/data/money/decisions/<year>.md` — the same pitch comes back with a new name. A loss suffered, its circumstances and the household's resulting sensitivities go to `## Pain Points` in `~/Clawic/data/money/memory.md`. An active incident with dates, reference numbers and who was notified is an artifact at `~/Clawic/data/money/artifacts/fraud-incident.md`, with its `## Boxes` line in the same turn. An adviser being evaluated is a person: `~/Clawic/data/contacts/contacts.md`, with their fee structure recorded here, not there. Format in `memory-template.md`.
