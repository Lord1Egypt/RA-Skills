# Credit — Scores, Reports, and Freezes

**Before answering**, read `## Situation` in `~/Clawic/data/money/memory.md` (freeze status, any dispute in flight, last report pull) and the card and loan rows in `~/Clawic/data/finances/accounts.md`.

Credit scoring is the most jurisdiction-specific subject in this skill. The US-style single three-digit score does not exist everywhere: several countries run negative-only registries (a file exists only once something goes wrong), others have bureau-specific scores that lenders barely use, and a few have no consumer score at all. Establish `country` before quoting a number, a weight or a threshold. The mechanics below hold wherever a bureau-based score exists; the weights are FICO's published ones.

## What Actually Moves It

| Factor | Weight (FICO) | What moves it, in practice |
|---|---|---|
| Payment history | 35% | One 30-day late is the single most damaging routine event; it is reported only at 30 days, so a payment 5 days late costs a fee, not a score |
| Amounts owed (utilization) | 30% | Reported utilization is a **snapshot on the statement date**, not an average |
| Length of history | 15% | Average age of accounts; closing an old card removes its age from the average once it ages off the file |
| New credit | 10% | Hard inquiries, small and short-lived |
| Credit mix | 10% | Revolving plus instalment; not worth taking a loan to improve |

## The Utilization Snapshot

The highest-leverage and least-known mechanic: the bureau sees the balance the issuer reports on the statement date, and someone who clears the card in full every month can still show 80% utilization if they spend near the limit before the statement closes.

- **Pay before the statement closes**, not before the due date, in the month before an application. Same money, different reported number.
- Utilization matters per card and in aggregate; a single maxed card hurts even with low aggregate use.
- The "keep it under 30%" rule is folk arithmetic. Scores respond continuously and high-scoring files typically report single-digit utilization; there is no cliff at 30%, and 0% across every card scores marginally worse than a small reported balance.
- Utilization has **no memory**. It is recalculated each month, so a bad month repairs itself next month — unlike a late payment, which stays on the file for years.

## Applying for Credit

- **Rate shopping is protected within a window** — multiple mortgage or auto inquiries inside 14-45 days count as one, depending on the scoring model. Compress the shopping into two weeks and it costs one inquiry.
- Card applications get no such protection: each is its own inquiry.
- Apply for the smallest number of products, in the shortest window, and never in the 90 days before a mortgage application: new accounts change both the inquiry count and the average age at the worst possible moment.
- A refusal is not itself recorded, but the inquiry that preceded it is. Ask the lender for the reason codes; they are more useful than the score.

## Reading the Report

Pull the report, not the score. The score is the output; the report is the input, and it is what a lender actually reads.

| Check | Why |
|---|---|
| Accounts you do not recognise | Fraud, or a closed account still reporting as open |
| Balances and limits, per account | A missing limit makes some models treat the highest-ever balance as the limit, inflating utilization |
| Late markers and their dates | Disputable; and they age off, so know the date they drop |
| Addresses and identity data | A stranger's address linked to your file is how mail-based fraud starts |
| Financial associations (joint accounts, ex-partners) | In several jurisdictions another person's file affects yours until the association is formally broken — a divorce that leaves it in place is a live liability (`household.md`) |
| Searches | Unrecognised hard searches are an early fraud signal |

Dispute in writing, to the bureau **and** the furnisher, with the evidence attached. Most regimes require an investigation within a fixed window (commonly 30 days) and removal of anything unverifiable. Keep the correspondence, and put its dates and reference numbers in `~/Clawic/data/money/artifacts/identity-incident.md` if fraud is involved; recurring re-insertion of a removed item is a known failure mode.

## Freezes, Alerts, and Identity Theft

- **A freeze blocks new credit being opened in your name and does not affect your score.** In many jurisdictions it is free to place and lift. It is the strongest single control an individual has, and it is not a fraud alert — an alert asks lenders to verify, a freeze stops them.
- Freeze at every bureau operating in the country; freezing one is theatre.
- After a breach or a stolen wallet, the sequence is: freeze → report to the bank and card issuer → change the credentials, storing only the pointer (`keychain:...`) → file the police or national fraud report → pull all reports → document dates and reference numbers in an artifact.
- Lift for a specific application, then re-freeze. A permanent thaw defeats it.

## Building a File From Nothing

For a young adult, a recent immigrant or anyone with a thin file:

- Time is the ingredient that cannot be bought. Open the first line early, keep it forever, and never close the oldest account.
- A secured card or small credit-builder loan, used for one recurring small payment and cleared before the statement, builds history with near-zero cost.
- Authorized-user status on an established account transfers history in some scoring models and not others — check `country` before recommending it.
- Utility, rent and telecom reporting schemes exist in several markets and are the cheapest way for a thin file to gain payment history.
- Immigrant files do not transfer across borders. Assume a new arrival starts from zero regardless of a 20-year record elsewhere, and plan the first 12 months around that.

## Where the Score Actually Matters

It matters at exactly the moments credit is priced or access is screened: a mortgage or loan application, a card, sometimes a rental tenancy, sometimes employment screening, and in some markets insurance pricing. Outside those moments it is a vanity metric, and optimizing it costs real money — carrying a balance "to build credit" is paying interest for nothing, since the statement balance reports either way.

Order the work by the rate it unlocks: a scoring band worth 0.25 percentage points on a 200,000 mortgage over 25 years is roughly 8,000 in interest — worth six months of preparation. The same band on a phone contract is worth nothing.

**Write it down.** A freeze placed or lifted, a dispute opened and its outcome, and the date of the last report pull go to `## Situation` in `~/Clawic/data/money/memory.md`; the annual pull goes in the `## Due` table. An identity-theft incident — dates, reference numbers, who was notified — is an artifact at `~/Clawic/data/money/artifacts/identity-incident.md`, with its `## Boxes` line added in the same turn. Card limits and rates learned here update `~/Clawic/data/finances/accounts.md`. Format in `memory-template.md`.
