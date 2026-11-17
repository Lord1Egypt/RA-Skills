# Reviewing an Agreement Someone Sent You

The inbound review is the most common legal task and the easiest to do badly, because reading a contract front to back puts the cheapest words first and the expensive ones on page 14 when attention is gone.

**Before the first read**, check `## Contracts` in `~/Clawic/data/lawyer/memory.md` (or `contracts.md` if the `## Boxes` index points there) for an existing agreement with the same counterparty, and `## Positions` for what was conceded last time. Reviewing a renewal as if it were new re-opens battles already won and re-loses ones already lost.

**Contents:** [Triage First](#triage-first) · [The Read Order](#the-read-order) · [The Absence Review](#the-absence-review) · [Reading the Money](#reading-the-money) · [Redline Mechanics](#redline-mechanics) · [Reviewing a Document You Cannot Change](#reviewing-a-document-you-cannot-change) · [Comparing Versions](#comparing-versions) · [Time Budgets](#time-budgets) · [Delivering the Review](#delivering-the-review)

## Triage First

Five questions, answered before any clause is read. They decide how much review the document deserves.

| Question | Where the answer is | Why it changes the review |
|---|---|---|
| What is the total contract value? | Fees clause × term, plus auto-renewal terms | Above `signature_authority_usd` this needs a named approver and counsel (Output Gates) |
| How long are we locked in? | Term and termination clauses | A 3-year lock with no convenience exit is a different document from a 12-month rolling one |
| What is the worst case if this goes wrong? | Limitation of liability plus the indemnities | This is the number the whole review is about (SKILL.md Rule 2) |
| Whose paper is it, and how standard? | Header, defined-term style, whether clause numbers are sequential | Their standard paper has approved fallbacks; a bespoke draft was written for this deal and every word is deliberate |
| Is there a deadline on our side? | The email, not the contract | A contract reviewed after the customer's quarter-end closed is a contract nobody reads |

Then classify. Value under 10% of `signature_authority_usd` and standard paper → playbook pass, 20 minutes, cap and indemnity only. Anything above, or bespoke, or with a term over 24 months → full read order below.

## The Read Order

Read these seven in this order regardless of where they sit in the document. Everything else is context.

1. **Parties and recitals.** Exact registered names and entity forms of both sides; entity mismatch makes the rest moot (SKILL.md Rule 7). Recitals are not operative but are used to construe ambiguity, so a recital that misdescribes the deal is a liability.
2. **Term, renewal, termination.** How it ends, how long the notice is, whether either side has termination for convenience, and what survives. Termination for convenience for them and not for you is the single most asymmetric clause in commercial contracts.
3. **Fees, increases, and payment.** What is owed, when, what happens on late payment, whether prices can rise mid-term and by how much, and whether prepaid amounts are refundable.
4. **Limitation of liability and its carve-outs.** Both sentences as one clause. Compute the real exposure.
5. **Indemnities.** Who indemnifies whom, for what, who controls the defence, whether it sits inside or outside the cap.
6. **IP and data.** Who owns what is created, what happens to background IP, who is controller and who is processor, whether a DPA is attached (`privacy.md`).
7. **Governing law, forum, and dispute resolution.** Whether enforcing this contract is affordable from where the user sits.

Only after those seven: warranties, confidentiality, insurance, assignment, force majeure, notices, boilerplate. Boilerplate is where cheap wins live — notice addresses, precedence order, counterparts — and they are cheap because nobody fights them, not because they do not matter.

## The Absence Review

Half of a bad contract is what is not in it. The absent clause silently imports the governing law's default, which nobody has read.

| Missing | What fills the gap | Ask for |
|---|---|---|
| Limitation of liability | Unlimited damages, subject only to remoteness rules | A cap, even a generous one — the principle matters more than the number |
| Termination for cause with cure | Only repudiatory breach ends it, which is a litigation-grade test | 30-day cure, immediate for insolvency and non-payment |
| Order of precedence across documents | Interpretation fight when the order form contradicts the MSA | An explicit precedence clause (SKILL.md Rule 8) |
| Price-increase mechanism | Either no increases at all, or an unlimited one at renewal | Cap increases at a stated percentage or an index, with notice |
| Data protection terms where personal data flows | Statutory non-compliance for both sides, not just a gap | An Art. 28-compliant DPA (`privacy.md`) |
| Assignment restriction | Free assignment — the contract can end up with a competitor | Consent required, deemed given for a bona fide acquirer |
| Exit assistance / data return | No obligation to give your data back in usable form | Named format, named window, named cost |
| Insurance | No backing behind the indemnity that was so hard to win | Limits at least equal to the supercap (SKILL.md Rule 2) |
| Notices clause | Service rules of the governing law, which may require post | Email plus a named address, with a deemed-receipt rule |

## Reading the Money

Contract value is rarely the fees line. Build the number:

```
total commitment = base fees × term
                 + committed minimums or true-up obligations
                 + mandatory professional services and onboarding
                 + overage rates × realistic usage
                 + auto-renewal terms not yet counted
```

Then the exposure side: `worst case = cap + uncapped carve-outs + indemnity obligations + termination-for-convenience penalty`. Two numbers, stated in the review. A review that reports "the cap is 12 months of fees" without saying what 12 months of fees is has not done the work.

Overage and minimum-commitment clauses cause more disputes than caps do, because they are the only clause whose cost depends on the user's own behaviour a year later. Model the overage at 2× and 5× expected usage before signing.

## Redline Mechanics

- **Change the words, not the concept, in the comment.** A redline that deletes a clause with the comment "not acceptable" costs a round trip. Propose the replacement text and one sentence of why: "Cap at 12 months of fees paid — our insurance limit sits here."
- **Three tiers per issue.** Ideal, acceptable, walk-away. Send the ideal, know the acceptable, never reveal the walk-away (`negotiation.md`).
- **Number the issues.** A redline with an accompanying issues list of 6 numbered points closes faster than 40 inline edits, because the other side's approver reads the list, not the document.
- **Never accept a clean copy without comparing.** Ask for the redline against the last version you sent; if they only send clean, run your own comparison before signature (below).
- **Do not fix their typos and their grammar.** It adds noise to the diff and hides the substantive changes.
- **Keep the rationale out of the document.** Comments become discoverable and can be used as evidence of what the parties intended — usually against you (SKILL.md Rule 9).

## Reviewing a Document You Cannot Change

Click-through terms, marketplace agreements, employment paperwork at a large company, bank terms. The review still has value; the output is different.

1. Identify the three obligations that are actually operational: what the user must do, must not do, and must notify.
2. Identify the termination and data-exit mechanics, and record them in `## Due` — this is the only part that can be acted on later.
3. Identify anything that conflicts with an existing commitment (an exclusivity, a non-solicit, a data-residency promise made to a customer). This is the real find; contradiction between two contracts is a breach of one of them.
4. State the residual risk in one line and let the user decide. Advising against signing a document nobody can change is not advice.

## Comparing Versions

When a "clean" copy arrives, changes hide in three places: defined terms (a change to the definition of "Services" restructures the whole agreement without touching any operative clause), cross-references (clause 11.2 now points to a renumbered clause), and schedules (the price list is a separate file nobody diffs). Compare definitions and schedules explicitly, not just the body.

## Time Budgets

Calibrated for a competent reviewer, not for speed-reading. Anything materially faster is a triage, not a review — say which one you did.

| Document | Pages | Full review |
|---|---|---|
| Mutual NDA on standard terms | 2-4 | 15-30 min |
| SaaS order form against an existing MSA | 2-6 | 30-60 min |
| MSA or services agreement, first time with this counterparty | 15-40 | 3-6 hours |
| Enterprise customer paper with DPA, security exhibit and SLA | 40-100 | 8-15 hours |
| Employment agreement with equity and restrictive covenants | 8-20 | 2-4 hours |

## Delivering the Review

Structure, in this order: (1) the recommendation — sign, sign with changes, or do not sign; (2) the two numbers, total commitment and worst-case exposure; (3) the numbered issues list with ideal and acceptable positions; (4) the deadlines this contract creates; (5) what was checked and found acceptable, in one line, so nobody re-reviews it.

**After the review**, write in the same turn (`memory-template.md`): the agreement's row in `## Contracts` in `memory.md` — counterparty, type, side, value with currency, effective date, term, renewal and notice dates, governing law, cap, and where the executed copy lives — plus every computed date into `## Due`, and any position taken into `## Positions`. If the counterparty is new, its person row goes to the shared `~/Clawic/data/contacts/contacts.md` and is referenced here by name only. A review whose deadlines were never calendared has to be repeated in eleven months.
