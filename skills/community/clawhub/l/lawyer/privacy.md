# Data Protection and Privacy

Privacy work is four questions in order — what role are we in, what is the lawful basis, where does the data go, and what happens when it leaks. Answering them out of order produces a privacy policy that describes a company nobody works at.

**Before answering**, read `## Legal Context` in `~/Clawic/data/lawyer/memory.md` for the regimes in scope (`compliance_regimes`) and open any `artifacts/policy-privacy*.md` or `artifacts/ropa*.md` the `## Boxes` index names. Advice that contradicts the published policy is worse than no advice: the policy is a representation to regulators and to every customer.

**Contents:** [Role First](#role-first) · [Lawful Basis](#lawful-basis) · [Data Subject Rights](#data-subject-rights) · [The DPA](#the-dpa) · [International Transfers](#international-transfers) · [US State Laws](#us-state-laws) · [Sector Regimes](#sector-regimes) · [Cookies, Tracking And Consent](#cookies-tracking-and-consent) · [Breach](#breach) · [Records, DPIAs And Governance](#records-dpias-and-governance) · [Writing The Privacy Policy](#writing-the-privacy-policy) · [Retention And Deletion](#retention-and-deletion) · [Vendors And AI Tools](#vendors-and-ai-tools)

## Role First

Everything downstream depends on this and it is decided by facts, not by the contract label.

| Role | Test | Consequences |
|---|---|---|
| Controller | Decides the purposes and means of processing | Owes the transparency, basis, rights-handling and breach-notification duties |
| Processor | Processes only on documented instructions from a controller | Owes security, sub-processor and assistance duties; becomes a controller the moment it uses the data for its own purposes |
| Joint controllers | Two parties jointly determine purposes and means | Must have an arrangement setting out respective responsibilities, and the essence must be available to data subjects |
| Independent controllers | Each decides its own purposes on the same data | No DPA between them; a data-sharing agreement instead |

Common misfilings: an analytics vendor that improves its own product with customer data is a controller for that use, whatever the DPA says. A payroll provider is usually an independent controller for its statutory filing duties and a processor for the rest — a split-role DPA.

## Lawful Basis

Under GDPR (Art. 6) there are six, and consent is usually the worst available choice for a business relationship because it is withdrawable at any time.

| Basis | Good for | Watch |
|---|---|---|
| Contract necessity | Delivering the service the user signed up for | Only what is genuinely necessary, not everything convenient |
| Legitimate interests | Security, fraud prevention, direct B2B marketing, product analytics | Requires a documented balancing test (LIA) and an unconditional right to object |
| Legal obligation | Tax records, employment filings, KYC | Only the obligation that actually exists in law |
| Consent | Cookies and tracking, optional marketing, special categories | Freely given, specific, informed, unambiguous, withdrawable as easily as given; pre-ticked boxes are not consent |
| Vital interests / public task | Rare in commercial contexts | — |

Special-category data (health, biometrics, race, religion, sexual orientation, trade union membership, political opinion) needs an Art. 9 condition **in addition** to the Art. 6 basis, and criminal-offence data has its own rule. Processing employee health data on "consent" fails, because consent in an employment relationship is rarely free.

Changing the basis after the fact is not permitted — the basis must be chosen and disclosed before processing begins.

## Data Subject Rights

Access, rectification, erasure, restriction, portability, objection, and rights around automated decision-making. Operational reality matters more than the list:

- **One month to respond** under GDPR, extendable by two further months for complex requests with notice inside the first month. UK equivalent is the same. Free of charge except for manifestly unfounded or excessive requests.
- Identity verification is required, and must be proportionate — demanding a passport scan for an email-account request creates a new data problem.
- Erasure is not absolute: retention required by law, legal claims, and freedom of expression all override. Backups need a documented approach (mark for deletion, delete on restore cycle) rather than a false promise of immediate erasure.
- Access requests made in the middle of an employment dispute are a litigation tactic and remain fully valid; the response still has to redact third-party personal data.
- Build the request route into the product and log every request with its deadline in `## Due`. The deadline is where the breach happens, not the substance.

## The DPA

Required whenever a controller uses a processor. GDPR Art. 28 sets mandatory content: subject matter and duration, nature and purpose, types of data and categories of subject, controller instructions only, confidentiality of staff, Art. 32 security, sub-processor rules, assistance with rights and with Arts. 32-36, deletion or return at the end, and audit/information rights.

Negotiating positions and market landing zones are in `agreements.md`. Two things people get wrong: the processing-description annex is left blank or generic, which makes the whole DPA unusable as evidence; and the sub-processor list is not maintained, so the notice-and-object mechanism silently fails.

## International Transfers

Transferring personal data out of the EEA or the UK needs a mechanism, and the mechanism depends on the destination.

| Destination | Mechanism |
|---|---|
| Country with an adequacy decision (UK, Switzerland, Japan, South Korea, Canada for commercial organisations, and others) | No further mechanism needed for the covered scope |
| United States, recipient self-certified under the EU-US Data Privacy Framework (adequacy decision, 2023) and its UK extension | Certification covers the transfer; verify the recipient's current certification and the scope, including HR data |
| Anywhere else | Standard Contractual Clauses (EU Commission Implementing Decision 2021/914), with the correct module for the relationship, plus a transfer impact assessment. UK transfers use the IDTA or the UK Addendum to the EU SCCs |
| Intra-group, large organisation | Binding Corporate Rules, slow and expensive to approve |

The transfer impact assessment is a real obligation after *Schrems II* (2020): assess the destination's laws and add supplementary measures (encryption with keys held in the exporting jurisdiction is the strongest) where they undermine the clauses. Remote access from a third country counts as a transfer — a support engineer viewing EU data from outside the EEA needs a mechanism.

Data localisation is separate from transfer law and exists in several jurisdictions; check it as its own question.

## US State Laws

A patchwork rather than a regime. California (CCPA as amended by CPRA) is the deepest and the working reference: rights to know, delete, correct, opt out of sale and of sharing for cross-context behavioural advertising, and limit use of sensitive personal information; a Global Privacy Control signal must be honoured; contracts with service providers must contain specified terms; and there is a **private right of action for breaches of unencrypted personal information with statutory damages of $100-$750 per consumer per incident**, which is the number that makes California breaches expensive.

The other state laws (Virginia, Colorado, Connecticut, Utah and the growing set that followed) share a common shape — notice, opt-outs for targeted advertising and sale, data protection assessments for higher-risk processing, and processor contract terms — with differing thresholds and definitions. Build to the strictest applicable and map the differences; running a separate programme per state does not scale.

"Sale" under CCPA is broader than money changing hands: sharing identifiers with an ad network for valuable consideration counts, which is why so many sites have a "Do Not Sell or Share" link.

## Sector Regimes

- **HIPAA** (US health): covered entities and business associates; a Business Associate Agreement is mandatory before any protected health information flows; breach notification to individuals and HHS within 60 days, and immediately for large breaches.
- **PCI DSS** (card data): contractual rather than statutory, imposed by the card networks; scope reduction (never touching card data, using a hosted payment field) is worth far more than compliance effort.
- **COPPA** (US, under 13): verifiable parental consent before collection, with narrow exceptions. Getting age-gating wrong is a first-order regulatory risk for consumer products.
- **FERPA** (US education), **GLBA** (US financial), and equivalents elsewhere each add their own contract and notice requirements.
- Financial services, insurance and telecoms carry sector data rules on top of general privacy law in most countries.

## Cookies, Tracking And Consent

- In the EU and UK, cookie rules come from the ePrivacy regime, not GDPR: **consent is required before storing or accessing any non-essential information on a device**, regardless of whether personal data is involved. Analytics cookies are not essential under most regulators' guidance.
- A banner that only offers "Accept" is non-compliant; rejection must be as easy as acceptance, and consent must be recorded with proof.
- Tracking pixels, SDKs, fingerprinting and server-side tagging are the same rule as cookies. Moving tracking server-side does not remove the consent requirement.
- US law approaches the same conduct through "sale/share" opt-outs and, increasingly, wiretapping-statute claims against session-replay and chat tools. The exposure is real and litigation-driven rather than regulator-driven.
- Audit what actually loads before writing the banner. Most cookie policies describe a smaller set of trackers than the site deploys, and that gap is the enforcement hook.

## Breach

The clock starts at **awareness**, which is when the organisation has a reasonable degree of certainty that a security incident compromised personal data — not when the investigation finishes.

| Obligation | Trigger | Deadline |
|---|---|---|
| GDPR notification to supervisory authority (Art. 33) | Any personal data breach unless unlikely to result in risk to individuals | **72 hours from awareness**, with a phased notification permitted if details are incomplete |
| GDPR notification to individuals (Art. 34) | High risk to rights and freedoms | Without undue delay; not required if data was encrypted to an appropriate standard |
| US state breach laws | Varies by state; unencrypted personal information is the common trigger | Ranges from "without unreasonable delay" to fixed 30/45/60-day limits; several require notice to the state attorney general |
| HIPAA | Breach of unsecured PHI | 60 days to individuals and HHS; immediate for 500+ individuals |
| Contractual (processor to controller) | Any breach | Whatever the DPA says — negotiate 24-72 hours (`agreements.md`) |

First hour: contain, preserve logs and evidence, start a written incident timeline, notify insurers (cyber policies commonly require immediate notice and use of panel counsel, and using your own lawyer first can void coverage), and engage counsel so the forensic investigation can be run under privilege where that is available. Then assess, then notify. A breach is a Red Flags row.

Documentation duty applies even to breaches that are not notified: every breach is recorded internally with the facts, effects and remedial action, and a regulator will ask for that register.

## Records, DPIAs And Governance

- **Records of processing (Art. 30)**: required for most organisations; a spreadsheet of purposes, categories, recipients, transfers and retention. It is the first document a regulator asks for and the artifact everything else is built from.
- **DPIA**: required for high-risk processing — large-scale special-category data, systematic monitoring of public areas, automated decisions with legal effects, and whatever the national authority's list adds. Do it before the processing starts; a retrospective DPIA is evidence of failure.
- **DPO**: mandatory for public authorities and for organisations whose core activity is large-scale regular monitoring or special-category processing. Where not mandatory, name an owner anyway.
- **EU/UK representative**: required for organisations outside the EU/UK targeting people inside it and with no establishment there.
- Training and access controls are compliance evidence as much as security measures.

## Writing The Privacy Policy

Structure that satisfies Arts. 13-14 and is still readable: who we are and how to contact us · what data we collect and from where · why, with the lawful basis for each purpose · who we share it with, by category and named processors where practical · international transfers and the mechanism · retention periods or the criteria for them · the rights and how to exercise them · the right to complain to a supervisory authority · automated decision-making, if any · how changes are notified.

The rule that matters: **it must describe what actually happens** (SKILL.md Traps). Write it from the records of processing, not from a template, and re-check it whenever a new vendor or tracker is added. A policy promising deletion within 30 days while backups retain data for a year is a misrepresentation — and misrepresentation, not the privacy failure, is what consumer-protection regulators bring cases on.

## Retention And Deletion

Set a schedule per data category with the reason: statutory minimum (tax and employment records commonly 4-7 years, jurisdiction-specific), limitation-period cover for claims, and a defined business need. "As long as necessary" without criteria fails the transparency test. Then implement it — an unimplemented retention schedule is worse than none, because it is a documented, unmet commitment. Backups get a stated approach; legal holds override everything and must suspend automated deletion (`disputes.md`).

## Vendors And AI Tools

Before any new tool touches personal data: what data goes in, what role each party is in, is there a DPA, where is it hosted and what transfer mechanism applies, does the vendor use the data to train or improve its own products, what are the sub-processors, what security certifications exist and are they current, and what happens to the data at exit. Pasting customer data into a consumer-tier AI tool is a transfer, a possible sub-processor breach, and often a contract breach with the customer — three problems from one paste.

**After any privacy work**, write in the same turn (`memory-template.md`): the regimes and roles into `## Legal Context` in `memory.md`; every statutory clock (rights-request deadlines, breach notification, DPIA review, certification renewal) into `## Due`; a breach, complaint or regulator contact as a row in `## Matters` with its dates; and every durable document — the privacy policy version, the records of processing, a DPIA, a transfer impact assessment, a breach-response runbook — into `~/Clawic/data/lawyer/artifacts/` with its `## Boxes` line. Never copy the personal data itself into these files: record that a dataset exists, its categories and its controller, not its contents.
