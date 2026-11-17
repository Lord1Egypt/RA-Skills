# Clause Positions and Fallback Ladders

One clause per section: what it does, the market range, the ladder from ideal to walk-away, and what it is worth trading against. Positions are written for B2B software and services and shift with leverage — a startup selling to a bank does not get the vendor column.

**Before proposing a position**, read `## Positions` in `~/Clawic/data/lawyer/memory.md` and any `artifacts/clause-*.md` its `## Boxes` index names for this clause. A position conceded to one customer becomes the position every other customer's counsel will find in diligence.

**Contents:** [Limitation of Liability](#limitation-of-liability) · [Indemnities](#indemnities) · [IP Ownership](#ip-ownership) · [Warranties](#warranties) · [Confidentiality](#confidentiality) · [Term and Termination](#term-and-termination) · [Payment](#payment) · [SLA and Service Credits](#sla-and-service-credits) · [Insurance](#insurance) · [Assignment and Change of Control](#assignment-and-change-of-control) · [Audit Rights](#audit-rights) · [Non-Solicit and Exclusivity](#non-solicit-and-exclusivity) · [Force Majeure](#force-majeure) · [Governing Law and Forum](#governing-law-and-forum) · [Boilerplate That Is Not Boilerplate](#boilerplate-that-is-not-boilerplate)

## Limitation of Liability

Two components that must be read as one: the cap, and what escapes it.

| Position | Cap | Carve-outs from the cap |
|---|---|---|
| Vendor ideal | 12 months of fees paid in the 12 months before the claim; consequential damages excluded both ways | Fraud and willful misconduct only |
| Market landing zone | 12 months of fees, plus a supercap of 2-5× for data breach and IP indemnity | Fraud, willful misconduct, IP indemnity, death/personal injury, payment obligations |
| Customer ideal | Greater of total fees or a fixed sum; supercap for data at a fixed number matched to the incident cost | Everything above plus confidentiality and data protection, uncapped |
| Walk-away | Uncapped general liability with no exclusion of consequential damages | — |

Mechanics that decide the number:

- **Mutuality is cheap and worth asking for.** A one-sided cap protecting only the drafter is the most common asymmetry in vendor paper, and the least defended when challenged.
- **"Fees paid" versus "fees payable"**: on an annual prepay they are the same; on a monthly contract terminated in month two, "paid" is two months and "payable" is twelve. Say which.
- **Exclusion of consequential and indirect damages** removes lost profits, which in most commercial disputes *is* the loss. Excluding them is standard and mutual; carving lost profits back in for the confidentiality breach is the customer's reasonable ask.
- **Payment obligations must sit outside the cap.** Otherwise the cap becomes a ceiling on the invoice: a customer owing $500k against a $120k cap can decline to pay the difference.
- **Aggregate versus per-claim.** Aggregate across the contract term is standard; per-claim caps multiply silently.
- **The insurance test.** A supercap above the insurance limit is a promise the company cannot keep (SKILL.md Rule 2). Argue the insurance limit, and produce the certificate — it converts a negotiation into arithmetic.

## Indemnities

An indemnity is a promise to pay someone else's loss, and it usually escapes the cap, so it is the largest number in the contract.

| Indemnity | Who gives it | Standard scope | The fight |
|---|---|---|---|
| IP infringement | Vendor | Third-party claim that the product infringes | Whether it covers combination with customer systems and customer-directed modifications (it should not) |
| Data breach | Vendor | Breach caused by vendor's failure of its stated security obligations | Whether it is uncapped or supercapped, and whether it includes regulatory fines (many insurers will not cover fines) |
| Customer content / misuse | Customer | Claims arising from customer data and unlawful use | Whether the vendor gets it at all on their standard paper |
| Confidentiality | Mutual | Loss from unauthorised disclosure | Usually handled by carve-out from the cap instead |

Procedure is half the value: the indemnifying party gets prompt written notice, sole control of the defence, and cooperation; the indemnified party keeps a veto over any settlement that admits liability or imposes obligations on it. Without the settlement veto, the indemnitor can settle by promising the plaintiff something the indemnitee must then do.

The IP indemnity should include the remedy ladder: procure the right to continue, modify to be non-infringing, or refund a pro-rata amount and terminate. Refund-and-terminate as the *only* remedy leaves the customer with a migration and no product.

## IP Ownership

Three buckets, and the whole fight is about the boundary.

- **Background IP** — everything either side had before, plus generic tooling, libraries and know-how. Stays with its owner. Vendors must reserve this explicitly or "all work product" swallows their platform.
- **Foreground / deliverables** — created specifically under this contract. Customer ownership is market for bespoke services; vendor ownership with a broad licence is market for products.
- **Residuals** — unaided memory of the engagement. Vendor-friendly and heavily contested; customers with real trade secrets should refuse a residuals clause outright, because it legitimises reuse of exactly what confidentiality was meant to protect.

Assignment mechanics: in most common-law systems, an employee's work in the course of employment vests with the employer by default, but a **contractor owns what they create unless there is a written assignment** — US "work made for hire" only covers nine enumerated categories plus a signed writing, and software is not one of them unless it qualifies as a contribution to a collective work. Always take a present-tense assignment ("hereby assigns") plus a moral-rights waiver where waivable, and a further-assurances obligation (`ip.md`).

## Warranties

| Warranty | Vendor position | Customer ask |
|---|---|---|
| Services performed in a professional and workmanlike manner | Standard, give it | Add "in accordance with the Documentation" |
| Product conforms to documentation | 30-90 day remedy window, repair or refund | Continuous during the term |
| No open-source contamination of deliverables | Give it, scoped to copyleft licences | Full disclosure of all components (an SBOM) |
| Non-infringement | Give as an indemnity, not a warranty | Both |
| Uptime | Handle in the SLA with credits, never as a warranty | Termination right after repeated misses |

A disclaimer of implied warranties (merchantability, fitness for purpose) is standard in commercial contracts and often required to be conspicuous — in the US, UCC 2-316 requires the fitness disclaimer to be in writing and conspicuous, which is why those clauses are in capitals.

## Confidentiality

- **Duration**: 3-5 years post-termination is market; trade secrets should survive indefinitely, which needs its own sentence because a flat 3-year term extinguishes trade-secret protection by contract.
- **The four standard exclusions**: already known, publicly available through no fault, independently developed, rightfully received from a third party. A fifth is required by law, with a notice obligation so the disclosing party can seek protection.
- **Marking requirements are a trap for the disclosing side.** "Information marked confidential" means an unmarked disclosure is unprotected. Prefer "information that a reasonable person would understand to be confidential", with marking as an option not a condition.
- **Return or destroy on termination**, with a carve-out for backups and legal-hold copies, which cannot honestly be deleted.
- Include the injunctive-relief acknowledgment: damages are an inadequate remedy for disclosure, so the disclosing party can seek an injunction without posting a bond. This is one of the few clauses where the boilerplate does real work.

## Term and Termination

| Element | Market | Notes |
|---|---|---|
| Initial term | 12 months for SaaS; project length plus a tail for services | Multi-year gets a discount, but count the total commitment (`review.md`) |
| Auto-renewal | Common, 12-month periods | Notice window 30-90 days before the renewal date; calendar it the day of signature (SKILL.md Rule 3) |
| Termination for convenience | Customer: 30-90 days notice, often only at renewal. Vendor: rarely, and should be resisted | A vendor convenience right turns a dependency into a hostage situation |
| Termination for cause | Material breach, 30-day cure; immediate for insolvency, non-payment after notice, and confidentiality breach | Define "material" by example if the deal warrants it |
| Effect of termination | What is refunded, what survives, what data is returned | Prepaid fees refunded pro-rata on vendor default, forfeited on customer convenience — say which |
| Survival | Confidentiality, IP, liability, indemnity, payment, governing law | A survival clause that omits the liability cap makes post-term claims uncapped |

## Payment

Net 30 is the default; net 60 and net 90 are procurement policies, not laws, and they are negotiable in exchange for a small discount. Late-payment interest exists by statute in some jurisdictions and must be claimed in others — in the EU, the Late Payment Directive gives a statutory rate plus a fixed recovery amount unless the contract sets its own. Get a right to suspend service after notice plus a cure window; without suspension, non-payment is only a lawsuit. Disputed invoices: the payer must pay the undisputed portion and notify the dispute within a stated window, or the whole invoice becomes a hostage to one line item.

## SLA and Service Credits

Credits are a remedy, not compensation, and they are capped at a percentage of monthly fees, so a 99.9% SLA with a 10% credit prices an outage at 10% of one month. What actually matters:

- **The measurement definition**: what counts as downtime, whether degraded performance counts, what the measurement interval is (a monthly average hides a four-hour outage), and who measures.
- **The exclusions**: scheduled maintenance, third-party failures, customer-caused issues. Exclusions typically consume more availability than the SLA promises.
- **The escalation right**: after N consecutive months below target, the customer can terminate without penalty and get a refund. That is the clause with teeth; the credits are decoration.
- Uptime math: 99.9% = ~43 minutes per month; 99.95% = ~22 minutes; 99.99% = ~4.3 minutes. Ask what the vendor actually achieved last year before agreeing on a number.

## Insurance

Ask for what backs the indemnity, and check the certificate rather than the clause. Typical B2B requirements: commercial general liability $1-2M per occurrence, professional liability / errors and omissions $1-5M, cyber liability $1-5M scaled to the data held, workers compensation as required by law. Additional-insured status and a waiver of subrogation are cheap asks that make the policy usable. Claims-made policies (professional and cyber usually are) only respond if the policy is live when the claim is made — require the coverage to continue for the survival period, or a run-off / extended reporting period after termination.

## Assignment and Change of Control

Free assignment lets the contract move to a competitor. Consent required, not unreasonably withheld, is standard; the negotiated exception is assignment to an affiliate or a bona fide acquirer of all or substantially all assets. Add a change-of-control provision when it matters: a customer buying from a startup wants continuity, and a vendor selling to a customer's competitor wants an exit. Note the asymmetry: a consent-required clause with no acquirer exception is a veto over the other side's exit, which is worth real money in an acquisition and will be found in diligence (`diligence.md`).

## Audit Rights

Give them, bound them: once per 12 months, on 30 days notice, during business hours, at the auditor's cost unless the audit finds an underpayment above a threshold (5% is the usual trigger), subject to confidentiality, and never a competitor as the auditor. Unbounded audit rights are a denial-of-service on a small vendor.

## Non-Solicit and Exclusivity

Non-solicit of employees: mutual, 12 months, limited to people who worked on the engagement, with the standard carve-outs for general advertising and unsolicited applicants. Without those carve-outs, a job board post is a breach. Exclusivity: always with a time limit and a performance condition — exclusivity without a minimum-volume commitment gives away the market for nothing. Enforceability of restrictive covenants varies sharply by jurisdiction (`employment.md`, `jurisdictions.md`).

## Force Majeure

Post-2020 drafting: list events rather than relying on a general phrase, because civil-law systems and common-law systems construe the general words very differently. Include epidemics and government action explicitly; exclude economic hardship and non-performance by subcontractors (or the clause excuses everything). Mechanics: notice within a stated period, a duty to mitigate, suspension rather than excuse, and a right for either side to terminate if the event lasts beyond 30-90 days. Payment obligations are never excused by force majeure — say so.

## Governing Law and Forum

Two separate choices; people conflate them. Governing law decides what the words mean; forum decides where you argue about it, and forum is the expensive one. A contract governed by New York law with exclusive jurisdiction in New York is unusable for a claim worth less than the cost of appearing there — which is exactly why the drafter chose it.

- Enforceability across borders favours arbitration: an arbitral award is enforceable in the ~170 states party to the New York Convention, while a foreign court judgment often is not (`disputes.md`).
- Carve injunctive relief out of any arbitration clause so a confidentiality breach can be stopped in a real court.
- Neutral third-country law is a compromise that costs both sides local expertise; use it only when neither side will move.
- Exclusive versus non-exclusive jurisdiction: non-exclusive means you can be sued anywhere. Prefer exclusive, in a forum you can reach.

## Boilerplate That Is Not Boilerplate

| Clause | Why it earns its place |
|---|---|
| Order of precedence | Resolves the MSA-versus-order-form conflict before it happens (SKILL.md Rule 8) |
| Notices | Wrong address or wrong method invalidates a termination notice; require email plus a named person, with deemed receipt |
| Entire agreement | Kills the side emails — including the ones the user is relying on |
| Amendment in writing signed by both | Prevents "agreed on the call"; also blocks amendment by conduct in most systems |
| No waiver | One indulgence does not surrender the right permanently |
| Severability | One void clause does not take the contract with it |
| Counterparts and electronic execution | Makes signing in two places valid (SKILL.md Rule 7) |
| Third-party rights excluded | Stops a stranger enforcing a benefit — in England and Wales this is an express exclusion of the Contracts (Rights of Third Parties) Act 1999 |

**When a clause position is finally accepted**, write in the same turn (`memory-template.md`): the exact wording to `~/Clawic/data/lawyer/artifacts/clause-<topic>.md` — the accepted language, the date, who accepted it, and the two positions that were rejected — with its `## Boxes` line in `memory.md`, plus the one-line summary into `## Positions`. Deriving an acceptable indemnity costs several negotiation rounds; nobody should pay for it twice.
