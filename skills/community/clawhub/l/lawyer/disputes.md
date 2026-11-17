# Disputes: Before, During and Instead Of Litigation

Most disputes are resolved by whoever is better organised in the first two weeks. Preservation and the limitation clock come before argument, and both are irreversible if missed.

**Before anything else**, read `## Matters` and `## Due` in `~/Clawic/data/lawyer/memory.md`, and `## Contracts` for the agreement in question — the dispute-resolution clause decides where this goes and it was agreed years ago. Open any `artifacts/chronology-*.md` the `## Boxes` index names for this counterparty. Anything with a court, a case number, a regulator or a criminal element is a Red Flags row: counsel today.

**Contents:** [The First 48 Hours](#the-first-48-hours) · [Litigation Hold](#litigation-hold) · [The Limitation Clock](#the-limitation-clock) · [Build The Chronology](#build-the-chronology) · [Assess The Claim](#assess-the-claim) · [Economics](#economics) · [The Demand Letter](#the-demand-letter) · [Cease And Desist](#cease-and-desist) · [Responding To A Demand](#responding-to-a-demand) · [Negotiated Resolution](#negotiated-resolution) · [Mediation And Arbitration](#mediation-and-arbitration) · [Court](#court) · [Enforcing And Collecting](#enforcing-and-collecting) · [Insurance](#insurance)

## The First 48 Hours

In order. Steps 1-3 are irreversible if skipped.

1. **Preserve.** Suspend automatic deletion, issue the litigation hold, and secure the systems that hold the evidence (below).
2. **Compute the deadlines.** Any response date on a document received, plus the limitation period on the claim itself. Both into `## Due` today.
3. **Notify insurers.** Most policies require prompt notice and many are claims-made; late notice can void cover, and some policies require panel counsel from the start (`counsel.md`).
4. **Stop talking to the other side** until the position is decided. Apologies, explanations and engineers' candid emails are all evidence.
5. **Collect the contract stack** — master agreement, order forms, SOWs, amendments, the actual signed versions with dates.
6. Only then: assess.

## Litigation Hold

Triggered when litigation is reasonably anticipated, not when it is filed. That standard means a threatening letter, a serious internal complaint, or a regulator's inquiry is enough.

A defensible hold: a written notice to every custodian who may hold relevant material, naming the subject matter and the categories to preserve, instructing them not to delete and to disable auto-deletion, acknowledged in writing; plus a systems step suspending retention policies, ephemeral messaging and backup rotation for the affected data. Re-issue reminders periodically and keep the list of custodians current.

Failure to preserve is sanctionable independently of the merits — in US federal practice, FRCP 37(e) allows sanctions up to an adverse-inference instruction or dismissal where electronically stored information was lost through failure to take reasonable steps. The consequence of a spoliation finding routinely exceeds the value of the underlying dispute.

Scope covers what people actually use: email, chat platforms, personal devices used for work, ticketing systems, code repositories, call recordings, and any tool with disappearing messages. "We use a messaging app that deletes after 30 days" is not a defence; disabling that feature is part of the hold.

## The Limitation Clock

The claim dies on this date regardless of merit, so it is computed before anything else is analysed.

| System | Written contract | Notes |
|---|---|---|
| England and Wales | 6 years from breach (Limitation Act 1980); **12 years for a deed** | Tort generally 6 years from damage, with a discoverability extension for latent damage |
| US states | Typically 3-6 years for written contracts, shorter for oral (California: 4 written, 2 oral) | Varies by state and cause of action; the contract may shorten it if the state permits |
| Sale of goods, US | 4 years under UCC 2-725, reducible to 1 by agreement | Runs from tender of delivery, not discovery |
| Employment claims | Often months, not years — UK tribunal claims are generally 3 months less one day; US EEOC charge deadlines are 180 or 300 days | The shortest clocks in the whole domain |
| Statutory and regulatory claims | Their own periods, often short | Check each specifically |

Three refinements that change the date: **when it starts** (breach, damage, or discovery — different by claim type), **contractual shortening**, which is enforceable in many systems, and **standstill agreements**, which pause the clock by consent when both sides want to negotiate without filing. A standstill is cheap and is the correct answer whenever a deadline is approaching mid-negotiation.

## Build The Chronology

The single most valuable work product in any dispute, and the cheapest to produce early: a dated table of every relevant event with the document that proves it. Date · what happened · who · source document · why it matters. Built once, it drives the demand letter, the settlement position, the counsel briefing and, if it goes that far, the pleading — and building it usually reveals that the strong-feeling grievance has a weak documentary spine, or the reverse.

Keep it factual. Characterisation, legal theory and candid assessments of weakness belong with counsel under privilege, not in a business document (SKILL.md Rule 9).

## Assess The Claim

Four questions, each independently fatal:

1. **Is there a right?** A term, a duty, a statutory protection — identified specifically, with the clause number.
2. **Is there a breach?** Facts matched to the term, with evidence for each element.
3. **Is there loss, and is it recoverable?** Causation, remoteness, mitigation, and any contractual exclusion of consequential loss or liability cap. This is where most claims shrink: the cap the user negotiated years ago now limits their own recovery.
4. **Is the defendant worth suing?** A judgment against an entity with no assets is an expensive document. Check the register, the accounts, and whether a parent or a guarantor is on the hook.

Then the defences the other side will raise: limitation, notice requirements not followed (many contracts require notice of a claim within a short window — missing it is a complete defence), failure to mitigate, waiver by conduct, and the entire-agreement clause killing the representation the whole claim rests on.

## Economics

Litigation decisions are arithmetic, and the arithmetic is usually decisive.

```
expected value = (probability of winning × recoverable amount × probability of collecting)
                 − own costs
                 − (probability of losing × exposure to other side's costs, where cost-shifting applies)
                 − management time
```

Calibration: costs escalate in steps, not smoothly. Pre-action correspondence is cheap; issuing is a step; disclosure or discovery is the largest step by a wide margin; trial is another. In US commercial litigation, reaching the end of discovery in a mid-sized case commonly costs six figures — which is why the disclosure stage, not trial, is where most cases settle.

Cost-shifting changes everything and is jurisdictional: in England and Wales the loser generally pays a proportion of the winner's costs; in the US each side generally bears its own unless a statute or the contract says otherwise. A prevailing-party fees clause in the contract converts a small claim into a viable one — check whether it is there and whether it is mutual.

Management time is a real cost and is systematically ignored. A two-year case consumes the attention of the people who would otherwise be running the business.

## The Demand Letter

The highest-return document in this file: it resolves a large share of commercial disputes for the cost of writing it.

Structure: who we are and who you are · the agreement and the specific clause · what happened, dated, with documents referenced · why that is a breach · what we want, precisely (an amount, an act, a date) · the deadline for response · what happens next if there is no response · reservation of rights. Attach the key documents.

Tone is a tactical choice, not a personality trait. Firm and factual outperforms aggressive: the letter will be read by the recipient's lawyer, their insurer and possibly a judge, and an intemperate letter is quoted back forever. Never threaten anything you will not do, and never threaten criminal proceedings to extract a civil payment — that is a criminal offence in many jurisdictions.

Where a pre-action protocol exists (England and Wales has them by claim type), following it is not optional: non-compliance leads to costs sanctions even for the winner. Mark correspondence "without prejudice" only where it is a genuine settlement communication, and understand that the label does not make an ordinary letter privileged.

## Cease And Desist

For infringement, misuse of confidential information, defamation or breach of a restrictive covenant. Same structure as a demand, plus: the right relied on with its registration or basis, the specific conduct, the specific act required, and a deadline.

Two risks before sending: it can trigger a declaratory-judgment action in the recipient's chosen forum, and an aggressive letter to a small or sympathetic recipient becomes a public story. Groundless threats of IP infringement are actionable in some jurisdictions — the UK has a specific statutory tort for unjustified threats in patent, trademark and design matters. Get the right checked before the letter goes out (`ip.md`).

## Responding To A Demand

Acknowledge receipt and buy time — a holding response that says the matter is being investigated and a substantive reply will follow by a stated date is standard and costs nothing. Do not admit, do not apologise in terms that concede liability, and do not let an engineer or an account manager reply directly.

Then run the same four-question assessment from the other side, plus: check the indemnity chain (does a supplier owe this?), check insurance, and check whether the claim's own notice requirements were met.

## Negotiated Resolution

Most disputes settle; the question is when and at what cost. Settling early is cheaper in money and management time, and the discount for early settlement is real. What matters in the document itself — release scope, mutuality, payment default consequences, section 1542-style waiver of unknown claims, confidentiality and non-disparagement — is in `agreements.md`.

Two structural points: settle **all** claims between the parties, not just the one in issue, or the next dispute starts from the same facts; and where payment is by instalments, secure it — a consent judgment held in escrow, a guarantee, or an acceleration clause with the full original claim reviving on default.

## Mediation And Arbitration

- **Mediation**: a facilitated negotiation, non-binding, usually one day, and it settles a high proportion of commercial disputes that reach it. Cheap relative to anything that follows. Many contracts and court rules require an attempt, and unreasonable refusal to mediate can attract costs sanctions in some systems.
- **Expert determination**: for narrow technical or valuation questions, faster and cheaper than either arbitration or court. Underused.
- **Arbitration**: binding, private, procedurally flexible, and very hard to appeal. Enforceable across the ~170 New York Convention states, which is its decisive advantage in cross-border deals. Costs are not low — arbitrator fees and institutional charges are paid by the parties, so a three-arbitrator tribunal in a mid-sized dispute can cost more than court.
- Arbitration clause drafting decides the cost: the institution and rules, the seat (which determines the supervising court and the procedural law), the language, the number of arbitrators (one, unless the amount is large), and an expedited procedure below a value threshold. Carve out injunctive relief so urgent matters can go to a real court (`clauses.md`).

## Court

Choose it when you need a precedent, a public record, an urgent injunction, an appeal right, or a defendant who will only respond to a filed claim. Small-value claims have their own cheap track almost everywhere — small-claims limits in US states run roughly $2,500-$25,000 (California allows $12,500 for individuals and $6,250 for entities), and England and Wales has a small-claims track with limited cost recovery. Those forums are designed for self-representation and are the right answer for straightforward debts (`personal.md`).

Interim relief is the part with real deadlines: an injunction application usually requires speed, a cross-undertaking in damages, and full and frank disclosure. Delay is itself a reason for refusal.

## Enforcing And Collecting

A judgment is permission to collect, not collection. Options depend on the system and on what the debtor has: attachment or garnishment of bank accounts and receivables, charging orders over property, enforcement officers seizing goods, insolvency proceedings as leverage, and information orders requiring the debtor to disclose assets.

Cross-border enforcement is where arbitration wins: an arbitral award travels under the New York Convention, while a foreign judgment depends on a patchwork of treaties and reciprocity. Find out where the assets are **before** choosing the forum, not after winning.

## Insurance

Check every policy at the start of any dispute, not the obvious one: professional indemnity, cyber, directors and officers, employment practices liability, and general liability. Policies commonly require immediate notice, prohibit admissions, and reserve the right to appoint counsel and to control settlement. Breaching those conditions forfeits cover — which means the insurer is contacted before counsel is instructed, not after.

**After any dispute activity**, write in the same turn (`memory-template.md`): the matter as a row in `## Matters` in `memory.md` — counterparty, subject, stage, amount at stake with currency, forum, next step and its date, spend to date — with every deadline into `## Due`; the chronology, hold notice, demand letter and settlement terms into `~/Clawic/data/lawyer/artifacts/` with their `## Boxes` lines (`chronology-<counterparty>.md`, `hold-<matter>.md`, `settlement-<counterparty>.md`); and the counterparty into the shared `~/Clawic/data/contacts/contacts.md` by name only. Legal spend on the matter also gets its line in the shared `~/Clawic/data/finances/budget.md`, in the currency it was billed. Keep strategy and candid assessments out of these files — they are business records, not privileged material (SKILL.md Rule 9).
