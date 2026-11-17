# Post-Signature Life of a Contract

Signature is the middle of the process, not the end. Everything that goes wrong afterwards goes wrong on a date: a renewal that passed, a notice served the wrong way, a cure period that expired, a change of control that needed consent nobody asked for.

**Before answering any "what do we owe / when is it due" question**, read `## Due` and `## Contracts` in `~/Clawic/data/lawyer/memory.md` (or `contracts.md` per the `## Boxes` index). This file is the reason those two boxes exist: an obligation that is not in `## Due` will be discovered by the counterparty, not by the user.

**Contents:** [The Obligation Extract](#the-obligation-extract) · [Date Arithmetic](#date-arithmetic) · [Renewal And Termination Windows](#renewal-and-termination-windows) · [Serving A Notice](#serving-a-notice) · [Cure Periods](#cure-periods) · [Price Increases And True-Ups](#price-increases-and-true-ups) · [Assignment And Change Of Control](#assignment-and-change-of-control) · [Amendments And Change Orders](#amendments-and-change-orders) · [Performance Failures](#performance-failures) · [Exit Execution](#exit-execution) · [The Quarterly Sweep](#the-quarterly-sweep)

## The Obligation Extract

Do this once per contract, at signature, in the same session as the review. It takes fifteen minutes and it is the entire value of contract administration.

| Extract | From | Where it goes |
|---|---|---|
| Effective date, initial term end, renewal date | Term clause | `## Contracts` row |
| Notice window and the resulting alarm date | Termination clause + Rule 3 formula | `## Due` |
| Payment dates and amounts with currency | Fees clause | `## Contracts` row; recurring costs also to shared `finances/subscriptions.md` |
| Reporting or certification obligations | Anywhere — often in an exhibit | `## Due`, with cadence |
| Insurance certificates to provide or collect | Insurance clause | `## Due`, annual |
| Volume commitments and true-up dates | Order form | `## Due` |
| Audit windows | Audit clause | `## Due`, annual |
| Consent triggers (assignment, change of control, subcontracting, sub-processors) | Assignment and DPA clauses | `## Contracts` row, as a flag |
| Survival list | Termination clause | `## Contracts` row |

Anything with a date goes in `## Due` on the day of signature. Anything conditional goes in the contract row as a flag, because it is only checked when the condition happens.

## Date Arithmetic

The formula (SKILL.md Rule 3):

```
notice_deadline = renewal_date − notice_period
alarm_date      = notice_deadline − notice_lead_days
```

Counting rules that change the answer:

- **Business days versus calendar days.** A 30-day period is 30 calendar days unless the contract says business days, in which case it is roughly 42 calendar days. Over a 90-day notice period the difference is about five weeks, and more where public holidays fall inside it.
- **Whose holidays.** "Business day" in a cross-border contract must be defined by reference to a named place, or the parties count different days.
- **Inclusive or exclusive of the first day.** Most systems exclude the day of the triggering event; the contract may say otherwise.
- **Deemed receipt.** A notice clause commonly deems delivery on the day of hand delivery, one to two business days after courier, and two to five business days after post. Those days come out of the notice period, so a notice posted on the deadline arrives late.
- **Month-end anomalies.** "Three months from 30 November" ends 28 or 29 February. State the convention or use a fixed date.

Work backwards from the immovable date, never forwards from today.

## Renewal And Termination Windows

The auto-renewal trap: the window opens and closes months before the renewal, and the counterparty has no duty to remind anyone. A 12-month contract with a 90-day notice period gives nine months of freedom and three months of lock-in every year.

- Calendar the **alarm**, not the deadline. `notice_lead_days` defaults to 45 so there is time to decide, get approval, and serve properly.
- Decide at the alarm even when the decision is "renew". A recorded decision with a date beats rediscovering the contract next year.
- **Non-renewal notice is different from termination for convenience.** Non-renewal simply lets the term expire and is usually unconditional; termination for convenience ends the contract mid-term and may carry a fee. Serve the right one.
- Evergreen contracts with no end date usually allow termination on reasonable notice, and what is reasonable is a fact question nobody wants to litigate. Convert them to a fixed term at the first opportunity.
- Where the contract is a subscription the user pays for, the decision also updates the shared `~/Clawic/data/finances/subscriptions.md` row — cancelled subscriptions get the row deleted, not left in place.

## Serving A Notice

A notice served in the wrong way is not served. This is the most common technical failure in commercial contracts and it is fully avoidable.

Checklist:

- The right method — email, courier, registered post, or a combination the clause requires. "Email only if also sent by courier" means both.
- The right address and the right named recipient, taken from the notices clause, not from the account manager's signature block. Update the address if the counterparty moved; many clauses require the moving party to notify.
- The right sender: the contracting entity, not a group company.
- The right content: identify the contract by title and date, state the clause relied on, state what the notice does, and state the effective date.
- Sent within the window, allowing for deemed receipt.
- Proof kept: delivery receipt, courier tracking, read receipt, all filed with the contract.

Copy the counterparty's legal or contracts function as well as the commercial contact where the clause allows it. A termination notice sitting in a departed employee's inbox is a dispute.

## Cure Periods

A cure period is an opportunity, and it runs against whoever received the notice. When issuing: state the breach specifically, cite the clause, state what cure would look like, and state the date the period ends and what happens then. Vague breach notices restart the argument instead of the clock.

When receiving: calendar the end date immediately, decide within the first quarter of the period whether cure is possible, and if it is not, negotiate an extension in writing before the period expires rather than after. Silence during a cure period is the worst option — it concedes the breach and exhausts the remedy.

Failure to cure does not always terminate automatically; most clauses give a right to terminate, exercisable by a further notice. Serve it, or the right can be waived by continuing to perform (below).

## Price Increases And True-Ups

- Check the increase mechanism before accepting an invoice that went up: many contracts cap increases (a percentage or an index) and require notice a set period before renewal. An increase served late or above the cap is not payable.
- Where the contract ties increases to an index, name the index, the reference month and the publication used. Indices are revised, and disputes follow.
- True-ups on committed volumes are computed at a stated measurement date, from a stated data source. Get the counterparty's usage report before the true-up date and check it against internal numbers; the vendor's meter is the one that counts unless the contract says otherwise.
- Overage invoices arrive after the behaviour that caused them. Set an internal alert at a usage threshold, not at the invoice.

## Assignment And Change Of Control

Both sides' corporate events touch the contract stack.

- **The user is acquiring or being acquired**: extract every contract with a consent requirement or a change-of-control termination right. That list is a diligence deliverable and a deal risk, and gathering it late delays closings (`diligence.md`).
- **The counterparty is acquired**: check whether the contract now sits with a competitor, whether confidential information is now inside that group, and whether any change-of-control right can be exercised.
- Internal reorganisations frequently trip assignment clauses that have no affiliate exception. Check before moving contracts between group entities; a "novation by email" is not a novation.
- Novation versus assignment: assignment moves benefits, novation moves benefits **and** obligations and needs all three parties to sign. Assigning a contract that has ongoing obligations without novating leaves the original party liable.

## Amendments And Change Orders

- Every amendment recites the original by title and date, states clause-by-clause what changes, and confirms the rest continues (`drafting.md`).
- After the second amendment, restate. Three stacked amendments make the operative text unreadable.
- Change orders under a SOW follow the change-control procedure exactly: scope change, time impact, fee impact, signed by both. Work performed on an unsigned change order is usually unpaid work.
- A "letter of intent to continue" or performing past the expiry date creates an implied contract on uncertain terms. Either extend formally or stop.

## Performance Failures

- **Document contemporaneously.** SLA misses, late deliverables and quality failures are worth what the record is worth, and a record assembled at termination looks assembled.
- **Claim credits when they are due**, and note that most SLA clauses require the customer to request credits within a short window (often 30 days) or they are lost.
- **Do not waive by conduct.** Continuing to accept and pay for defective performance without reserving rights can waive the breach in some systems. Reserve rights explicitly in writing: "we continue to perform without prejudice to our rights under clause X".
- Escalate through the contract's own escalation ladder if it has one — some dispute clauses make the ladder a precondition to any claim, and skipping it costs the filing (`disputes.md`).

## Exit Execution

Terminating well is a project. Sequence:

1. Serve the correct notice, correctly, within the window.
2. Confirm what survives — confidentiality, IP, liability, indemnity, payment, data obligations.
3. Trigger data export and return within the window the contract gives, in the format it specifies; the window is often 30 days and rarely extended.
4. Settle final invoices, including any early-termination fee, and resolve prepaid amounts.
5. Revoke access in both directions on the effective date.
6. Confirm destruction or return of confidential material, with the backup carve-out.
7. Delete the shared `finances/subscriptions.md` row if it was a recurring cost, and update the `## Contracts` row with the termination date and outcome.

## The Quarterly Sweep

A recurring row in `## Due`. Fifteen minutes per quarter, and it catches everything this file exists to prevent:

| Check | Look for |
|---|---|
| Renewals in the next two quarters | Anything whose alarm date lands before the next sweep |
| Contracts with no `## Due` entry at all | An extract that was never done |
| Recurring charges with no contract row | Shadow procurement — a tool someone expensed |
| Insurance certificates expired | Both the user's and the counterparties' |
| Price increases applied since last sweep | Increases above the contractual cap |
| Counterparties acquired, renamed or dissolved | Change-of-control rights, and entities that no longer exist |
| Contracts past their term still being performed | Evergreen by accident |
| Unclaimed SLA credits inside their window | Money on the table |

**After any post-signature action**, write in the same turn (`memory-template.md`): the updated `## Contracts` row in `memory.md` with the new dates and status, every new deadline into `## Due` with its alarm date, and the notice actually served — its date, method, recipient and the proof of delivery — into `~/Clawic/data/lawyer/artifacts/notice-<counterparty>-<subject>.md` with its `## Boxes` line. A served notice with no record of how it was served is the same as no notice at all when it is challenged.
