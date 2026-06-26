# Contract Red Flags Checklist

A categorized reference of common contract red flags. Loaded during Phase 2 (Systematic Analysis) to identify problematic clauses.

Each flag includes: the pattern to watch for, why it matters to a solo entrepreneur, and a suggested counter-position.

---

## Payment Red Flags

### Net-90+ Payment Terms
- **Pattern**: Payment due 90 or more days after invoice
- **Why it matters**: Solo entrepreneurs have no revenue buffer. Three months of unpaid work can threaten survival.
- **Counter-position**: Request net-30. Accept net-45 maximum. If net-60+ is unavoidable, negotiate a milestone-based payment schedule or upfront deposit.

### Pay-When-Paid / Pay-If-Paid
- **Pattern**: "Payment shall be made when Client receives payment from its end customer"
- **Why it matters**: Shifts the counterparty's collection risk entirely onto you. You have no relationship with their customer and no ability to collect.
- **Counter-position**: Reject outright. Payment obligation should be independent of counterparty's receivables.

### No Late Payment Consequences
- **Pattern**: No interest, penalties, or suspension rights for late payment
- **Why it matters**: Without consequences, counterparties deprioritize your invoices.
- **Counter-position**: Add late payment interest (1-1.5% monthly) and right to suspend work after 15 days overdue.

### Ambiguous Payment Triggers
- **Pattern**: "Payment upon satisfactory completion" without defined acceptance criteria
- **Why it matters**: Subjective triggers allow indefinite payment delays.
- **Counter-position**: Define specific acceptance criteria and deemed-acceptance after a review period (e.g., 10 business days).

### Right to Offset / Deduct
- **Pattern**: Counterparty can deduct amounts from payments for claimed damages or other contracts
- **Why it matters**: Creates unpredictable cash flow and dispute leverage for the counterparty.
- **Counter-position**: Limit offset to undisputed amounts only, with advance written notice.

---

## Liability & Indemnification Red Flags

### Unlimited Liability
- **Pattern**: No cap on total liability, or cap only applies to one party
- **Why it matters**: A single claim could exceed your total contract revenue by orders of magnitude.
- **Counter-position**: Cap liability at 1-2x total fees paid/payable under the contract. Ensure it's mutual.

### One-Sided Indemnification
- **Pattern**: You indemnify the counterparty but they don't indemnify you
- **Why it matters**: You bear all defense costs even when the counterparty's actions caused the issue.
- **Counter-position**: Make indemnification mutual. Each party indemnifies for their own breaches, negligence, and IP infringement.

### Personal Guarantee Requirements
- **Pattern**: Individual (not just the company) must guarantee performance or payment
- **Why it matters**: Pierces the corporate veil. Your personal assets are at risk.
- **Counter-position**: Reject personal guarantees. If unavoidable, cap the guaranteed amount and add a sunset clause.

### Indemnity Without Cap
- **Pattern**: Indemnification obligations excluded from the liability cap
- **Why it matters**: Effectively creates unlimited liability through the back door.
- **Counter-position**: Include indemnification within the overall liability cap, or set a separate indemnity-specific cap.

### Duty to Defend (not just indemnify)
- **Pattern**: Obligation to defend (not just reimburse) against third-party claims
- **Why it matters**: Legal defense costs are immediate and can be catastrophic for a small business, even if the claim is frivolous.
- **Counter-position**: Limit to indemnification (reimbursement after resolution) rather than duty to actively defend.

---

## IP Ownership Red Flags

### Broad IP Assignment (Background + Foreground)
- **Pattern**: Assignment of all intellectual property including pre-existing/background IP
- **Why it matters**: You could lose ownership of tools, frameworks, and code you built before this contract.
- **Counter-position**: Assign only project-specific deliverables. Retain all background IP with a license grant for the deliverables.

### No License-Back Provision
- **Pattern**: You assign IP but receive no license to use the work in your portfolio or for other clients
- **Why it matters**: You can't reuse your own methodologies, reducing your efficiency and competitive position.
- **Counter-position**: Include a non-exclusive, royalty-free license-back for non-confidential elements.

### Moral Rights Waiver
- **Pattern**: Waiver of all moral rights (attribution, integrity)
- **Why it matters**: In creative/consulting work, attribution builds your reputation as a solo practitioner.
- **Counter-position**: Retain moral rights or negotiate portfolio usage rights.

### Work-for-Hire Overreach
- **Pattern**: Everything created "in connection with" the engagement is work-for-hire
- **Why it matters**: Overly broad "in connection with" language could capture independent projects you work on during the contract period.
- **Counter-position**: Limit work-for-hire to specifically enumerated deliverables in the SOW.

### No IP Warranty Carveout
- **Pattern**: You warrant that all IP is original with no carveout for open-source or third-party components
- **Why it matters**: Modern software almost always includes open-source dependencies. An absolute originality warranty is impossible to satisfy.
- **Counter-position**: Carve out disclosed open-source and third-party components. Provide a dependency list.

---

## Termination Red Flags

### One-Sided Termination for Convenience
- **Pattern**: Only the counterparty can terminate without cause
- **Why it matters**: They can cut your revenue at any time while you remain locked in. See `references/termination-for-convenience.md` for deep-dive.
- **Counter-position**: Make TFC mutual, add minimum notice period (60+ days), and require payment for WIP.

### No Cure Period
- **Pattern**: Immediate termination for any breach, no opportunity to fix
- **Why it matters**: Minor administrative oversights (late report, missed meeting) become termination events.
- **Counter-position**: Add 30-day cure period for non-material breaches. Immediate termination only for material breaches after written notice and failure to cure.

### Unreasonable Notice Requirements
- **Pattern**: You must give 90+ days notice to terminate, but they can terminate on 7 days
- **Why it matters**: Asymmetric notice periods lock you in while the counterparty stays flexible.
- **Counter-position**: Equalize notice periods. 30-60 days is reasonable for most commercial contracts.

### Survival of Onerous Obligations
- **Pattern**: Non-compete, exclusivity, or restrictive covenants survive termination indefinitely
- **Why it matters**: You remain constrained long after the business relationship ends.
- **Counter-position**: Limit survival to 12-24 months maximum for restrictive covenants. Only confidentiality should survive longer (3-5 years or tied to trade secret protection).

---

## Scope & Deliverables Red Flags

### Vague Deliverables
- **Pattern**: "Contractor shall provide services as reasonably requested by Client"
- **Why it matters**: Open-ended scope means unlimited work for fixed compensation.
- **Counter-position**: Define specific deliverables, milestones, and acceptance criteria in a SOW. Add a change order process for scope additions.

### Unlimited Revisions
- **Pattern**: "Revisions until Client is satisfied" or no revision cap
- **Why it matters**: Perfectionism or scope creep becomes infinite free labor.
- **Counter-position**: Cap revisions (e.g., 2 rounds) with additional rounds at hourly rates. Define what constitutes a revision vs. a new request.

### Scope Creep Enablers
- **Pattern**: "Including but not limited to" language around deliverables, or "other duties as assigned"
- **Why it matters**: Transforms a defined engagement into an open-ended commitment.
- **Counter-position**: Use "limited to" language. All additions require written change orders with separate pricing.

---

## Non-Compete & Exclusivity Red Flags

### Overly Broad Non-Compete
- **Pattern**: Cannot work in the "industry" or "field" for 12+ months, regardless of geography
- **Why it matters**: For a solo entrepreneur, a broad non-compete can shut down your entire livelihood.
- **Counter-position**: Limit to specific named competitors, narrow geography, and 6 months maximum. Better yet, replace with a non-solicitation clause.

### Exclusivity Without Premium
- **Pattern**: You must work exclusively for the counterparty, but at standard rates
- **Why it matters**: Exclusivity eliminates your ability to diversify revenue, which is existential for a one-person company.
- **Counter-position**: Either reject exclusivity or demand a significant premium (2-3x standard rate) plus guaranteed minimum volume.

### Non-Solicitation Overreach
- **Pattern**: Cannot solicit any of the counterparty's clients, employees, or contractors
- **Why it matters**: In your industry, their clients may also be your natural client base.
- **Counter-position**: Limit to clients you directly worked with during the engagement, not the counterparty's entire client list.

---

## Auto-Renewal Red Flags

### Silent Auto-Renewal
- **Pattern**: Contract auto-renews unless written notice given 60-90 days before expiry
- **Why it matters**: Easy to miss the cancellation window and get locked into another term at potentially unfavorable rates.
- **Counter-position**: Require affirmative renewal (both parties must agree). If auto-renewal is unavoidable, demand a reminder notice obligation from counterparty and a short cancellation window (30 days).

### Price Escalation on Renewal
- **Pattern**: Rates increase by CPI or a fixed percentage on renewal, with no cap
- **Why it matters**: Compounding increases can make the contract uneconomical.
- **Counter-position**: Cap annual increases (e.g., max 5%) or require rate renegotiation at renewal.

### Narrow Cancellation Window
- **Pattern**: Must cancel within a 15-day window, 90 days before expiry
- **Why it matters**: A 15-day window is easy to miss when you're running a business alone.
- **Counter-position**: Extend the cancellation window to 60+ days, or add email reminder requirements.

---

## Data Protection & Privacy Red Flags

### Broad Data Usage Rights
- **Pattern**: Counterparty can use your data or your clients' data for "business purposes" without limitation
- **Why it matters**: Your client relationships and business data could be monetized by the counterparty.
- **Counter-position**: Limit data use to contract performance only. Prohibit resale, aggregation, or use for competitive purposes.

### No Breach Notification
- **Pattern**: No obligation to notify you of a data breach affecting your information
- **Why it matters**: You need to notify your own clients if their data is compromised, and delay can create liability.
- **Counter-position**: Require notification within 48-72 hours. Include a cooperation obligation for breach response.

### GDPR/CCPA Non-Compliance
- **Pattern**: No data processing addendum, no mention of data subject rights, or conflicting processing terms
- **Why it matters**: You're liable for your vendors' data handling failures if you're the controller.
- **Counter-position**: Require a compliant DPA. Verify sub-processor lists and data transfer mechanisms.

---

## Dispute Resolution Red Flags

### Distant or Unfavorable Jurisdiction
- **Pattern**: Disputes must be resolved in counterparty's home jurisdiction across the country or internationally
- **Why it matters**: Travel costs for a solo entrepreneur make litigation practically impossible.
- **Counter-position**: Negotiate neutral or your home jurisdiction. For remote disputes, agree to virtual arbitration or mediation first.

### Mandatory Arbitration with Counterparty's Arbitrator
- **Pattern**: Arbitration required, with the arbitrator selected by counterparty or their preferred organization
- **Why it matters**: Structural advantage to the counterparty in dispute resolution.
- **Counter-position**: Use a neutral arbitration body (AAA, JAMS). Each party selects one arbitrator; they jointly select a third.

### Waiver of Jury Trial
- **Pattern**: Both parties waive right to jury trial
- **Why it matters**: Jury trials can favor smaller parties against large corporations. Waiving this right removes a potential strategic advantage.
- **Counter-position**: Understand the implications for your jurisdiction. Consider keeping jury trial rights as negotiating leverage.

### Fee-Shifting Only Against You
- **Pattern**: Losing party pays legal fees, but only if you lose — no reciprocal provision
- **Why it matters**: Creates asymmetric litigation risk. You bear all downside.
- **Counter-position**: Make fee-shifting mutual, or remove it entirely.

---

## Insurance Red Flags

### Disproportionate Coverage Requirements
- **Pattern**: $5M+ professional liability insurance for a $50K contract
- **Why it matters**: Insurance premiums could exceed your contract profit margin.
- **Counter-position**: Request coverage proportional to contract value (2-3x contract value). Negotiate requirements to match what you can reasonably obtain.

### Naming Counterparty as Additional Insured
- **Pattern**: Must add counterparty as additional insured on your policies
- **Why it matters**: Extends your insurance coverage to protect them, potentially increasing your premiums and reducing your available coverage.
- **Counter-position**: Limit additional insured status to specific claims arising from the contracted work, not blanket coverage.

---

## General Red Flags

### Amendment by One Party
- **Pattern**: "Company may amend these terms at any time by posting updated terms"
- **Why it matters**: The counterparty can change the deal unilaterally after signing.
- **Counter-position**: Require written agreement from both parties for any amendments. No unilateral modifications.

### Assignment Without Consent
- **Pattern**: Counterparty can assign the contract to any third party without your approval
- **Why it matters**: You chose to work with a specific company. Assignment could put you under a company you'd never choose to work with.
- **Counter-position**: Require written consent for assignment, except in the case of a merger or acquisition (and even then, add a termination right if the acquirer is a competitor).

### Entire Agreement Clause Excluding Representations
- **Pattern**: Entire agreement clause that excludes pre-contractual representations
- **Why it matters**: Verbal promises made during negotiation become unenforceable.
- **Counter-position**: Ensure all material promises are in writing within the contract. If relying on specific representations, add them as schedules or exhibits.
