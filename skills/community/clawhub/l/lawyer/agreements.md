# Agreements by Type

What each document is for, the two or three clauses that actually decide it, and the mistake that recurs. Clause-level positions live in `clauses.md`; this file is the map of which clauses matter where.

**Before drafting or reviewing a type**, read `## Contracts` in `~/Clawic/data/lawyer/memory.md` (or `contracts.md` per the `## Boxes` index) for an existing agreement of the same type with the same counterparty — most "new" agreements are renewals or amendments in disguise.

**Contents:** [NDA](#nda) · [MSA And SOW](#msa-and-sow) · [SaaS Subscription And Order Form](#saas-subscription-and-order-form) · [Professional Services](#professional-services) · [Independent Contractor](#independent-contractor) · [Employment](#employment) · [Software Licence](#software-licence) · [Reseller, Referral And Partnership](#reseller-referral-and-partnership) · [Data Processing Agreement](#data-processing-agreement) · [LOI And Term Sheet](#loi-and-term-sheet) · [Settlement](#settlement) · [Commercial Lease](#commercial-lease) · [Loan And Promissory Note](#loan-and-promissory-note) · [Supply And Purchase](#supply-and-purchase) · [Website Terms And Privacy Policy](#website-terms-and-privacy-policy)

## NDA

Purpose: allow a conversation without losing rights. It is the cheapest document to get right and the one most often signed unread.

Decides it: **definition of Confidential Information** (marking requirement or not), **duration** (3-5 years, perpetual for trade secrets), **permitted recipients** (does it cover advisers, investors, affiliates?), and **the residuals clause** if there is one.

- One-way when only one side discloses; mutual the moment the other side will foreseeably say anything about its own roadmap.
- A non-solicit or non-compete hidden inside an NDA is common in M&A contexts and is a substantive restriction, not confidentiality. Read to the end.
- An NDA does not stop independent development. If that is the actual worry, the answer is a different agreement, not a stronger NDA.
- Standstill provisions in an M&A NDA restrict buying shares; a seller wants one, a potential acquirer should resist a long one.

Recurring mistake: signing the counterparty's NDA that defines Confidential Information as marked-only, then disclosing verbally in a meeting. Nothing said in that room is protected.

## MSA And SOW

Purpose: separate the stable legal frame (MSA) from the volatile deal detail (SOW). The MSA is negotiated once and lives for years; SOWs are issued repeatedly under it.

Decides it: **what belongs in which document** (nothing in the SOW that changes risk allocation), **precedence** (SOW governs scope; MSA governs risk), **whether the cap is per-SOW or aggregate across all SOWs**, and **whether termination of the MSA kills in-flight SOWs or lets them run off**.

- A per-SOW cap in a long relationship multiplies exposure; an aggregate cap across a five-year relationship can be exhausted by an old project. State which, deliberately.
- SOW template fields: scope, deliverables, acceptance criteria, milestones, fees and rates, assumptions, dependencies on the customer, change-control procedure, and named key personnel.
- Change control is the clause that saves services businesses: any change to scope requires a signed change order stating the impact on time and fees. Without it, scope creep is free.
- Customer dependencies must be written as conditions, not hopes: if the customer's data is late, the timeline moves and the fees continue.

## SaaS Subscription And Order Form

Purpose: recurring access to a hosted product. The order form is where the deal is, and it is the least reviewed document in the stack.

Decides it: **the subscription metric and what happens on overage**, **auto-renewal and its notice window**, **price-increase mechanics at renewal**, **uptime and the escalation right**, and **data export on exit**.

- The subscription metric (seats, MAUs, API calls, GB) is the whole commercial model. Define it exactly, define how it is measured, and define whether it is a peak, an average or a high-water mark.
- Overage is the sleeper cost: model it at 2× and 5× expected usage (`review.md`).
- Free trials, pilots and PoCs need an end date and a default: does it convert to paid, or expire? Silence produces an invoice.
- Exit: format of the export, window during which it is available, who pays, and whether the vendor can withhold it for unpaid fees (they usually can — negotiate an exception for undisputed export).
- Consumer-facing subscriptions have auto-renewal statutes on top of contract law: California's Automatic Renewal Law and equivalents elsewhere require clear disclosure, affirmative consent and an easy cancellation path. Regulator activity here is live; verify the current rule set before designing a flow (`compliance.md`).

## Professional Services

Purpose: people doing work for a fee. Consulting, agency, implementation, design, dev shops.

Decides it: **fixed price versus time and materials**, **acceptance**, **IP in deliverables versus background IP**, and **key personnel**.

- Fixed price transfers estimation risk to the supplier and requires airtight scope plus change control. T&M transfers it to the customer and requires a not-to-exceed and reporting. Say which, and never blend the two without saying how.
- Acceptance: criteria, test period, deemed acceptance if silent, number of correction cycles, and what happens if it still fails (fix, refund, or terminate).
- Background IP must be reserved explicitly by the supplier, or a broad "all work product" clause takes their framework (`clauses.md`).
- Key personnel clauses bind the supplier to named people with a replacement-approval right; the supplier should tie it to reasonable availability and add a substitution mechanic.
- Non-solicit of each other's staff, mutual, 12 months, with the advertising carve-out.

## Independent Contractor

Purpose: engage a person or a small company without employing them. The document is the second line of defence; the facts are the first (`employment.md`).

Decides it: **IP assignment in writing** (without it, in most systems the contractor owns the work), **classification-consistent terms**, **confidentiality**, and **who pays taxes and insurance**.

- The agreement must match reality: control over how the work is done, integration into the business, exclusivity and provision of equipment all point to employment regardless of the label.
- Do not put employment-flavoured terms in a contractor agreement: fixed hours, holiday entitlement, line management, performance reviews. Each one is evidence.
- IP: present assignment ("hereby assigns"), moral-rights waiver where waivable, further assurances, and — critically — the assignment must be tied to payment or it is worth arguing about when the invoice is unpaid.
- For contractors outside the user's country, an employer-of-record or a local entity may be required; a direct contract can create a permanent establishment and a tax presence.

## Employment

Purpose: hire someone. Content is heavily statute-driven and varies more by jurisdiction than any other agreement type.

Decides it: **what is contractual versus policy** (keep bonus schemes and handbooks non-contractual), **notice periods**, **IP and confidentiality**, **restrictive covenants**, and **equity terms if any**.

- Written particulars are mandatory in many jurisdictions within a set period after start — in the UK, on or before the first day.
- At-will employment exists in most US states and essentially nowhere else; drafting a European contract on a US template produces unenforceable terms and statutory penalties (`jurisdictions.md`).
- Restrictive covenants: enforceability turns on duration, geography, scope and consideration, and some jurisdictions void them entirely (`employment.md`).
- Equity is a separate document set — grant notice, plan, and (US) the 83(b) decision inside 30 days (`entity.md`).

## Software Licence

Purpose: grant rights in software without transferring ownership. Perpetual, subscription, on-premise, embedded, OEM.

Decides it: **the grant** (exclusive or not, transferable or not, sublicensable or not, territory, term, permitted users, permitted purposes), **the restrictions**, **audit rights**, and **escrow** if the licensee's business depends on it.

- Name the deployment model. A licence written for on-premise does not cover hosting the software to serve the licensee's own customers; that is a service-provider use and priced differently.
- Affiliate use: does the licence extend to subsidiaries, and what happens when one is sold?
- Source-code escrow with defined release conditions (insolvency, abandonment, failure to support) is the honest answer to key-person risk on critical software. It is only useful if the deposit is verified and current.
- Open-source components in licensed software: warrant compliance and disclose copyleft components (`ip.md`).

## Reseller, Referral And Partnership

Three different documents that get confused.

| Type | Who contracts with the end customer | Core clauses |
|---|---|---|
| Referral | Vendor | Commission rate, qualifying event, payment timing, term of the tail |
| Reseller | Reseller (buys and resells) | Margin or discount, minimum commitments, territory, exclusivity, end-customer terms flow-down, who supports |
| Agency / distributor | Varies | Authority limits, and in the EU commercial-agent regimes that can require compensation on termination regardless of the contract |

- Exclusivity always with a time limit and a volume condition (`clauses.md`).
- Flow-down: the reseller must impose the vendor's end-user terms on the customer, and the vendor needs the ability to enforce them — usually via a direct EULA click-through.
- Commission tails: how long after a referral does a commission accrue, and does it survive termination? This is the most litigated clause in referral agreements.
- Termination consequences: what happens to in-flight deals, existing customers and pipeline.

## Data Processing Agreement

Purpose: satisfy the statutory requirement that a controller instruct a processor in writing. Not optional where GDPR-equivalent law applies (`privacy.md`).

Decides it: **the processing description annex** (subject matter, duration, nature, purpose, data types, data subject categories), **sub-processor rules**, **the transfer mechanism**, and **audit and assistance obligations**.

- GDPR Art. 28 lists mandatory content; a DPA missing any of it is non-compliant even if commercially sensible.
- Sub-processors: general authorisation with notice and an objection right is the workable market position. A per-sub-processor consent right sounds strong and is unusable at scale.
- Audit rights in DPAs are usually satisfied by a current SOC 2 or ISO 27001 report plus a questionnaire; a physical audit right is standard text and rarely exercised.
- Assistance obligations (data subject requests, breach notification timing, DPIAs) create real operational duties on the processor. Notification to the controller should be "without undue delay and in any event within 24-72 hours" so the controller can meet its own 72-hour clock.

## LOI And Term Sheet

Purpose: agree the shape before spending money on the definitive documents.

Decides it: **which clauses are binding and which are not**. Mark every clause explicitly. Typically binding: confidentiality, exclusivity / no-shop, costs, governing law, and any break fee. Typically non-binding: price, structure, conditions.

- A document labelled non-binding can still bind if the language and conduct show intent — courts have enforced exclusivity and good-faith negotiation obligations out of "non-binding" LOIs.
- Exclusivity always with an end date. An open-ended no-shop hands the buyer free optionality.
- Good-faith negotiation obligations are enforceable in some systems and meaningless in others; know which before relying on one (`jurisdictions.md`).
- Investment term sheets carry securities-law consequences from the first conversation — Red Flags.

## Settlement

Purpose: end a dispute permanently. The single most important quality is finality (`disputes.md`).

Decides it: **the scope of the release** (which claims, which parties, known and unknown), **whether it is mutual**, **payment mechanics and what happens on default**, and **confidentiality and non-disparagement**.

- Release scope: name the parties (including officers, employees, affiliates, insurers, successors) and the claim period. In California, a general release does not cover unknown claims unless Civil Code section 1542 is expressly waived — the analogous trap exists in other systems under different names.
- Payment default clause: if the settlement sum is not paid on time, the full original claim revives or judgment can be entered. Without it, a settlement is just a new unsecured debt.
- No admission of liability, expressly stated.
- Employment settlements have their own formalities: US age-claim waivers need the OWBPA 21/7 timing, and UK settlement agreements require independent legal advice with the adviser named and insured (`employment.md`).
- Tax treatment of settlement sums differs by the type of loss compensated; allocate the sum between heads of claim in the agreement, and check the treatment (`accountant`).

## Commercial Lease

Purpose: occupy premises. Long, expensive and asymmetric; the largest fixed commitment most small companies sign.

Decides it: **term and break rights**, **the rent review mechanism**, **repairing obligations**, **service charge**, and **personal guarantees**.

- Full repairing and insuring (FRI) leases put the building's condition on the tenant; a schedule of condition agreed at the start caps that exposure to the state it was in.
- Break clauses are conditional and the conditions are strictly construed: rent paid up to date, vacant possession, no breaches. A break notice served one day late, or with rent outstanding, fails, and the tenant pays the remaining term.
- Service charge should be capped and the categories listed exhaustively.
- Personal guarantees on a company lease defeat the purpose of the company. Resist; if unavoidable, cap the amount and the duration, and negotiate release on a covenant test.
- Assignment and subletting rights determine whether the tenant can ever exit early.

## Loan And Promissory Note

Purpose: money now, repayment later.

Decides it: **the repayment schedule**, **interest and default interest**, **security**, **events of default and acceleration**, and **guarantees**.

- Interest: state the rate, the calculation basis (365 or 360 days, simple or compound), and check usury or consumer-credit limits, which are jurisdictional and criminal in some places.
- Events of default should include non-payment after a short cure, insolvency, breach of other agreements (cross-default), and a material adverse change if the lender has leverage.
- Security over assets needs registration in most systems to be effective against third parties, within short statutory windows — a charge registered late can be void against a liquidator.
- Convertible instruments (SAFEs, convertible notes) are securities and are priced in dilution, not interest (`cfo`, and Red Flags for the securities-law step).

## Supply And Purchase

Purpose: goods moving between businesses.

Decides it: **when title and risk pass**, **Incoterms**, **inspection and rejection windows**, **remedies for defective goods**, and **which side's standard terms won the battle of the forms**.

- Battle of the forms: where each side sends its own terms, the "last shot" usually governs in common-law systems while other systems apply a knock-out rule that voids the conflicting terms. Do not rely on your terms being on your invoice.
- Title and risk are separate: retention of title until payment protects the seller in the buyer's insolvency, but only if drafted and, in some systems, registered.
- Incoterms 2020 allocate cost, risk and customs duties in three letters — name the version year, or the reference is ambiguous.
- The UN Convention on Contracts for the International Sale of Goods (CISG) applies by default to cross-border sales between contracting states and is routinely excluded by an express clause. Decide deliberately rather than by inertia.

## Website Terms And Privacy Policy

Purpose: the contract with users, and the disclosure the law requires. They are different documents with different jobs — the privacy policy is not a contract and should not contain contractual terms.

Decides it: **how acceptance is captured**, **the licence to user content**, **the limitation of liability and its consumer limits**, **the change mechanism**, and **the accuracy of the privacy policy**.

- Clickwrap (an affirmative checkbox or button referencing the terms) is enforced far more reliably than browsewrap (a footer link). Capture and retain the acceptance record: user, timestamp, terms version.
- Consumer contracts limit what a limitation of liability can do; unfair-terms regimes strike out clauses that pass unchallenged in B2B contracts.
- Changing terms unilaterally requires a mechanism plus notice; for material changes to consumer terms, notice plus a right to exit is the defensible pattern.
- The privacy policy must describe what actually happens (`privacy.md`). A policy copied from another company is a misrepresentation waiting for a regulator.

**After any agreement is executed, amended or terminated**, write in the same turn (`memory-template.md`): its row in `## Contracts` in `memory.md` — counterparty, type, side, value with currency, effective date, term, renewal and notice dates, governing law, cap, where the executed copy lives — plus every date it creates into `## Due`. A reusable version of the document goes to `~/Clawic/data/lawyer/artifacts/template-<type>.md` with its `## Boxes` line. Recurring subscription-type agreements also get their cost row in the shared `~/Clawic/data/finances/subscriptions.md`, referencing this contract by name.
