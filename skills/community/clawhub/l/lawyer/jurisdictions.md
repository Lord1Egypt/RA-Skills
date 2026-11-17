# Where The Answer Changes

Legal answers are jurisdictional. The failure mode is not getting a rule wrong; it is applying a rule that is right somewhere else. This file lists the specific places where a confident answer stops travelling.

**Before any answer**, check `home_jurisdiction` in `config.yaml` and `## Legal Context` in `~/Clawic/data/lawyer/memory.md` for the entities, employing jurisdictions and customer territories already recorded. While `home_jurisdiction` is unset, state the law being assumed before answering (SKILL.md Rule 1) — a statement, not a question.

**Contents:** [Common Law Versus Civil Law](#common-law-versus-civil-law) · [Contract Doctrines That Do Not Travel](#contract-doctrines-that-do-not-travel) · [Employment: The Widest Gap](#employment-the-widest-gap) · [The US Is Fifty Jurisdictions](#the-us-is-fifty-jurisdictions) · [The EU Is Not One Jurisdiction Either](#the-eu-is-not-one-jurisdiction-either) · [Choice Of Law And Its Limits](#choice-of-law-and-its-limits) · [Choosing A Forum](#choosing-a-forum) · [Cross-Border Checklist](#cross-border-checklist) · [Language And Translation](#language-and-translation) · [How To Handle An Unfamiliar Jurisdiction](#how-to-handle-an-unfamiliar-jurisdiction)

## Common Law Versus Civil Law

| Dimension | Common law (US, UK, Ireland, Canada ex-Quebec, Australia, India, Singapore) | Civil law (most of Europe, Latin America, Japan, China, Quebec, Scotland in part) |
|---|---|---|
| Source of the rule | Statute plus binding precedent | Codes; case law is persuasive, not binding |
| Contract length | Long — the contract tries to be self-contained | Shorter — the code supplies defaults the parties do not need to write |
| Good faith | Limited or absent as a general duty in English law; recognised in US contract performance (UCC and Restatement) | A general duty, including in pre-contractual negotiation, often non-excludable |
| Consideration | Required for a simple contract; a deed substitutes | Not required; agreement plus cause or intent suffices |
| Penalties | Penalty clauses unenforceable; genuine pre-estimates of loss are | Penalty clauses generally enforceable, though courts may reduce a manifestly excessive one |
| Specific performance | Exceptional; damages are the default remedy | Often the primary remedy |
| Termination | Contractual mechanisms dominate | Statutory notice and judicial intervention may be required |
| Implied terms | Narrow, from statute or necessity | Broad, supplied by the code |

The practical consequence: a US-style 60-page contract governed by German or French law contains clauses that are void, redundant or reinterpreted, and omits protections the code would have supplied anyway.

## Contract Doctrines That Do Not Travel

| Doctrine | Where it works | Where it fails |
|---|---|---|
| Liquidated damages | Enforceable if a genuine pre-estimate of loss (common law), enforceable more freely in civil law | Void as a penalty in common law if punitive |
| Entire agreement clause | Strong effect in English law; effective in the US | Weaker in systems with a non-excludable pre-contractual good-faith duty |
| Exclusion of consequential loss | Standard and effective | Some systems limit or void exclusions for gross negligence or willful misconduct, however drafted |
| Termination for convenience | Freely enforceable | Distributor, agency and franchise relationships attract statutory compensation in many civil-law systems regardless of the clause |
| At-will termination of employment | Most US states | Essentially nowhere else |
| Non-compete without payment | Some US states | Void in California and restricted in several other states; requires payment in Germany, France, Italy, Spain and others |
| Waiver of statutory rights by employees | Limited even in the US | Generally void without a statutory procedure |
| Unlimited indemnities | Common commercial practice | Consumer and some B2B contexts restrict them; insurance may not follow |
| Contracts (Rights of Third Parties) exclusion | England and Wales specific | Meaningless elsewhere; other systems have their own stipulation-for-a-third-party rules |
| Deeds and the 12-year limitation period | England and Wales and related systems | No equivalent in most civil-law systems |

## Employment: The Widest Gap

The single area where importing an answer causes the most damage.

- **US**: at-will in most states, no statutory severance, employer-provided benefits, short notice, and litigation as the main enforcement mechanism. Federal floors with substantial state variation.
- **UK**: fair reason plus fair procedure required past the qualifying period, statutory notice and redundancy pay, tribunal claims on very short deadlines, TUPE transferring employees automatically on a business transfer.
- **Continental Europe**: dismissal generally requires cause or a negotiated exit, works councils with consultation and sometimes co-determination rights, statutory severance scales, long notice periods, and collective agreements that override individual contracts in whole sectors.
- **Latin America**: strongly employee-protective, with statutory severance formulas, mandatory profit sharing in some countries, and labour courts that presume in the employee's favour.
- Everywhere: hiring the first person in a new country triggers payroll registration, mandatory terms, social contributions and often a local entity or an employer of record (`employment.md`).

## The US Is Fifty Jurisdictions

Federal law sets floors; states do the rest, and the variance is large enough that "US law" is rarely a usable answer.

| Area | Variance |
|---|---|
| Non-competes | Void in California (Bus & Prof Code 16600, extended in 2024 to out-of-state agreements with a private right of action); heavily restricted in Washington, Colorado, Illinois, Minnesota and others; reasonable-restraint tests elsewhere |
| Worker classification | ABC test in California and a growing set of states; common-law control test federally |
| Privacy | California's CCPA/CPRA is the deepest; Virginia, Colorado, Connecticut, Utah and the rest of the wave differ in thresholds and rights (`privacy.md`) |
| Wage and hour | State minimums above the federal $7.25; California adds daily overtime and much higher exempt-salary thresholds |
| Limitation periods | Roughly 3-6 years for written contracts, state by state |
| Final pay | Immediate on involuntary termination in California; other states allow the next pay cycle, with penalties for lateness |
| Small claims limits | Roughly $2,500-$25,000 |
| Consumer auto-renewal | California's ARL is the strictest baseline; others follow with variations |
| Corporate law | Delaware for venture-backed companies; the operating state still requires foreign qualification |

## The EU Is Not One Jurisdiction Either

Regulations (GDPR, the AI Act) apply directly and are close to uniform. Directives (consumer rights, working time, collective redundancy, trade secrets) are implemented into national law with real differences in scope, thresholds and remedies. Member-state derogations under GDPR — employment data, national identifiers, age of consent for information-society services, which ranges from 13 to 16 — mean a compliant answer in Ireland may not be compliant in Germany.

Then there are national supervisory authorities with different enforcement postures, national procedural law for any dispute, and national employment law, which the EU barely harmonises.

## Choice Of Law And Its Limits

Parties can choose the governing law of a commercial contract in most systems, and that choice is normally respected. What it cannot do:

- **Mandatory rules of the forum and of closely connected jurisdictions still apply.** Employment, consumer, agency, competition, insolvency, real property, and data protection all carry overriding rules the parties cannot contract out of.
- **Consumers keep the protection of their home law.** In the EU, a choice of law cannot deprive a consumer of the mandatory protections of their habitual residence (Rome I, Art. 6). A US choice-of-law clause in a contract with an EU consumer does not remove EU consumer rights.
- **Employees keep the protection of the country where they habitually work** (Rome I, Art. 8), regardless of what the contract says.
- **Real property** is governed by the law where the property is, always.
- Choosing a law with no connection to either party is permitted in many systems but adds cost: both sides need advice on a law neither knows.

## Choosing A Forum

Governing law and forum are separate decisions and the forum is the expensive one (`clauses.md`). The question that decides it: **where are the counterparty's assets, and can a judgment from this forum reach them?**

- Arbitral awards are enforceable in the roughly 170 states party to the New York Convention. That is the strongest cross-border enforcement mechanism in existence.
- Court judgments travel unevenly. Within the EU, mutual recognition is strong. Elsewhere it depends on treaties, reciprocity and local exequatur procedures — the Hague Judgments Convention improves this between its parties, but coverage is far narrower than the New York Convention.
- Some jurisdictions will not enforce foreign judgments at all against local defendants, which makes local courts the only realistic option.
- An exclusive jurisdiction clause naming an expensive forum is a de facto immunity from small claims. That may be the point, in either direction.

## Cross-Border Checklist

Before signing anything with a foreign counterparty:

- Which law governs, and does it match the forum? A mismatch means paying for two sets of expertise.
- Where are their assets, and can the chosen forum reach them?
- Are there mandatory local rules that override the choice — consumer, employment, agency, distribution, data?
- Withholding tax on payments, and who bears it. A gross-up clause is a real cost line, not boilerplate (`accountant`).
- Currency of payment, who bears exchange risk, and whether exchange controls exist in the counterparty's country.
- Sanctions and export exposure on the counterparty, its owners and the destination (`compliance.md`).
- Data transfer mechanism if personal data crosses a border, including remote access (`privacy.md`).
- Language of the contract and which version prevails.
- Formalities: notarisation, apostille under the Hague Apostille Convention, or consular legalisation, any of which can add weeks to a signing timetable.
- Permanent establishment risk from staff, agents or servers in the other country.

## Language And Translation

Name one version as prevailing; a bilingual contract with two equally authentic versions creates an interpretation dispute in every ambiguity. Where local law requires a local-language version (employment contracts in France and Poland, consumer contracts in several countries, filings almost everywhere), the local version usually prevails as a matter of law regardless of the clause — so it must be a proper legal translation, not a convenience copy. Budget for certified translation where a court or registry will receive it.

## How To Handle An Unfamiliar Jurisdiction

1. State clearly that the jurisdiction is outside what can be answered reliably, and say what is known versus assumed.
2. Identify the **family** — common law, civil law, or mixed — and reason from the defaults above, flagging every inference as an inference.
3. Isolate the questions that are almost certainly local and non-negotiable: employment termination, consumer protection, real property, tax, licensing, and anything with a filing deadline.
4. Produce the brief for local counsel: the transaction, the specific questions, the documents, the deadline, and the budget (`counsel.md`). Local counsel answering five specific questions costs a fraction of local counsel asked to advise generally.
5. Record what comes back so it is not bought twice.

**After any jurisdictional work**, write in the same turn (`memory-template.md`): the entities, employing jurisdictions, customer territories and governing-law defaults into `## Legal Context` in `memory.md`; a jurisdiction-specific answer that took real work to obtain — local counsel's advice, the enforceability position on a clause, a local formality requirement — into `~/Clawic/data/lawyer/artifacts/memo-<jurisdiction>-<topic>.md` with its `## Boxes` line and a read condition naming the jurisdiction. The next contract in that country should start from this file, not from a fresh question.
