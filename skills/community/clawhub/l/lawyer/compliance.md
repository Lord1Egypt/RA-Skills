# Compliance Programs and Regulatory Calendars

Compliance is an inventory problem before it is a legal one. Most failures are not decisions to break a rule; they are obligations nobody wrote down, owned by nobody, checked never.

**Before building or answering**, read `## Legal Context` and `## Due` in `~/Clawic/data/lawyer/memory.md`, plus `compliance_regimes` in `config.yaml`, and open any `artifacts/policy-*.md` or `artifacts/compliance-register*.md` the `## Boxes` index names. A second policy on a topic that already has one is a contradiction, and contradictions are what auditors find.

**Contents:** [Build The Register First](#build-the-register-first) · [Which Regimes Apply](#which-regimes-apply) · [Consumer Protection And Marketing](#consumer-protection-and-marketing) · [Sanctions, Export And AML](#sanctions-export-and-aml) · [Sector Licences](#sector-licences) · [Accessibility](#accessibility) · [Environmental And Supply Chain](#environmental-and-supply-chain) · [Policies That Earn Their Place](#policies-that-earn-their-place) · [Evidence](#evidence) · [The Calendar](#the-calendar) · [When Something Is Already Non-Compliant](#when-something-is-already-non-compliant) · [Regulator Contact](#regulator-contact)

## Build The Register First

One table, one row per obligation. Everything else in this file feeds it.

| Column | Content |
|---|---|
| Obligation | The specific thing that must be done or not done |
| Source | Statute, regulation, contract, standard, or platform rule — with the citation |
| Trigger | What makes it apply (headcount, revenue, data type, territory, activity) |
| Owner | A named person, never a team |
| Cadence | One-off, annual, quarterly, on-event |
| Evidence | What proves it happened, and where that lives |
| Status | Met, gap, or not applicable with the reason |

"Not applicable with the reason" is the most valuable row type: without it, the same question gets re-researched every year and every diligence cycle.

Scope by trigger, not by fear. Most regimes have thresholds — headcount, turnover, number of data subjects, whether the activity is regulated at all — and a small company that maps its triggers honestly usually finds that a third of the scary list does not apply yet, with the threshold worth calendaring for when it will.

## Which Regimes Apply

Run this sweep against the business; each yes creates rows in the register.

| Question | Regime family |
|---|---|
| Do we hold personal data of anyone in the EU/UK, California, or another state with a privacy law? | Data protection (`privacy.md`) |
| Do we take card payments, or touch card data at all? | PCI DSS |
| Do we handle health, financial, education or children's data? | HIPAA, GLBA, FERPA, COPPA and equivalents |
| Do we sell to consumers rather than businesses? | Consumer protection, distance selling, auto-renewal, warranty and returns law |
| Do we advertise, make comparative claims, or use testimonials? | Advertising and unfair-practices rules |
| Do we sell or ship across borders, or serve customers in sanctioned regions? | Export control, sanctions, customs |
| Do we handle client money, lend, insure, or give financial or legal advice? | Sector licensing |
| Do we have employees, and how many, where? | Employment thresholds (`employment.md`) |
| Do we operate a website or app used by the public? | Accessibility, cookies, terms disclosure |
| Do we build or deploy AI systems with legal or significant effects on people? | AI-specific regulation, phased and jurisdictional |
| Do we hold a certification customers rely on (SOC 2, ISO 27001)? | The certification's own control set and audit cycle |
| Do we sell to government or to regulated customers? | Flow-down obligations from their regime into our contracts |

## Consumer Protection And Marketing

The most commonly breached area in small companies, because marketing moves faster than review.

- **Claims must be substantiated before publication.** "Fastest", "most secure", "#1" and any performance number needs evidence held at the time of the claim, not assembled after a challenge.
- **Endorsements and influencers**: material connections must be disclosed clearly and conspicuously, and the advertiser is responsible for what its affiliates say. Fake or incentivised reviews attract penalties in the US, UK and EU.
- **Dark patterns** — pre-ticked boxes, confirmshaming, hidden costs, obstructed cancellation — are now explicitly targeted by the EU Digital Services Act and by US state privacy and consumer laws, not merely bad practice.
- **Pricing**: drip pricing and misleading reference prices ("was £199") are enforcement staples. Any "was" price must have been the genuine selling price for a meaningful period.
- **Auto-renewal**: clear disclosure before purchase, affirmative consent, renewal reminders in some jurisdictions, and cancellation at least as easy as signup. California's Automatic Renewal Law is the strictest US baseline; the federal position has been through rulemaking and litigation, so verify the current requirement before designing the flow.
- **Email and SMS**: opt-in rules differ (US CAN-SPAM allows opt-out for email with an unsubscribe and a physical address; the EU generally requires prior consent with a narrow existing-customer exception; SMS is consent-based nearly everywhere and carries statutory damages in the US under the TCPA).
- **Distance selling / withdrawal rights**: EU and UK consumers get a 14-day cooling-off period on most distance contracts, with specific rules for digital content that require express consent to immediate performance and acknowledgment of the lost right.

## Sanctions, Export And AML

- Sanctions screening applies to every business, not just banks: dealing with a designated person or a comprehensively sanctioned territory is a strict-liability offence in most regimes. Screen customers, suppliers and payment counterparties against the applicable lists (US OFAC, UK, EU consolidated), and re-screen periodically, not just at onboarding.
- Export control reaches software and technical data, including by making it downloadable in a controlled territory or by giving a foreign national access to controlled technology. Encryption has its own classification rules.
- Anti-money-laundering obligations apply to regulated sectors and increasingly to others: customer due diligence, beneficial-ownership identification, source of funds, and suspicious activity reporting with tipping-off prohibitions.
- Anti-bribery law is extraterritorial and unforgiving: the US FCPA and the UK Bribery Act 2010 both reach conduct abroad, and the UK Act creates a corporate offence of failing to prevent bribery with "adequate procedures" as the only defence. Facilitation payments are lawful under narrow US exceptions and unlawful under the UK Act.
- These are the rows in the register most likely to be discovered by a bank or a payment processor rather than a regulator, and the consequence is account closure with no appeal.

## Sector Licences

If the activity requires authorisation, no contract can substitute for it. Common traps for technology companies: holding or transmitting client money (payments and e-money licensing), arranging insurance or credit as an add-on, providing investment or tax advice inside a product, operating a marketplace that touches funds, and offering anything that functions as a deposit. The "we are just a platform" position is a legal conclusion that regulators test on the facts.

Where licensing is uncertain, the cheap move is a regulated partner who holds the permission, with the arrangement documented. The expensive move is discovering the answer after launch.

## Accessibility

Public-facing digital services are covered by accessibility law in a growing number of jurisdictions: the ADA as applied to websites in the US (a litigation-driven exposure with high claim volume), the European Accessibility Act, and public-sector rules almost everywhere. The technical standard cited is generally WCAG at level AA. Treat it as a product requirement with a conformance record, not a legal opinion (`wcag-compliance`).

## Environmental And Supply Chain

Scale-dependent and expanding: packaging and waste registration (EPR), battery and electronics rules, product safety and CE/UKCA marking for physical goods, modern-slavery statements above turnover thresholds in the UK and Australia, and EU supply-chain and sustainability reporting duties that phase in by company size. For a small software company most of this is "not applicable, threshold X" — which is a register row, not a blank.

## Policies That Earn Their Place

A policy creates an obligation to follow it, and an unfollowed policy is worse evidence than no policy. The defensible core for a small company:

| Policy | Why it exists |
|---|---|
| Information security | Required by customer contracts, certifications and privacy law; the basis for the DPA's Art. 32 commitments |
| Data protection and retention | Implements the privacy programme (`privacy.md`) |
| Acceptable use and device | Makes monitoring and offboarding lawful and predictable |
| Anti-bribery and gifts | The "adequate procedures" defence needs a written procedure |
| Anti-harassment and equal opportunity with a reporting route | Employment defensibility (`employment.md`) |
| Incident response | The 72-hour clock cannot be met by improvisation |
| Vendor / third-party risk | The mechanism that stops shadow procurement of tools that process personal data |
| Sanctions and screening, where relevant | Strict-liability exposure |

Each policy names an owner, a review cadence, and where its evidence lives. Version and date every one; an undated policy cannot prove what was in force at the time of an incident.

## Evidence

Compliance is judged on evidence, not intent. For each control, decide what artefact proves it: a signed acknowledgment, a system log, a training completion record, a screening report, a board minute, a dated policy version, a completed checklist. Store the evidence where it can be retrieved by date, because the question is always "what was in place on the day it happened".

Certifications (SOC 2 Type II, ISO 27001) are evidence machines: their real value to a small company is that they force the register, the owners and the cadence into existence, and then satisfy most customer questionnaires in one document (`diligence.md`).

## The Calendar

Every recurring obligation becomes a row in `## Due` in `memory.md` with what, cadence, last run and next due. The minimum set for most companies: entity filings and tax deadlines (`entity.md`), policy review, privacy records and DPIA review, access review, sanctions re-screening, certification audit windows, insurance renewal, contract renewal sweep (`obligations.md`), and IP maintenance (`ip.md`).

Cadence discipline: check `## Due` against today's date at the start of a session and state any overdue item in one line. A calendar nobody checks is a list of things that will be discovered late.

## When Something Is Already Non-Compliant

1. Establish the facts and the exposure window before deciding anything, and preserve the records that show both (`disputes.md`).
2. Stop the ongoing breach where stopping is possible; continuing after discovery converts negligence into something worse.
3. Assess mandatory reporting: some regimes require self-reporting within a deadline, and voluntary disclosure often reduces penalties materially.
4. Take advice before self-reporting. Voluntary disclosure is a strategy with trade-offs, not an automatic good, and it is a Red Flags escalation (`counsel.md`).
5. Remediate with dates and owners, and keep the remediation record — regulators weigh the response more heavily than the original failure.

## Regulator Contact

Any letter, inspection notice or information request from a regulator: calendar the response deadline first, preserve everything, route to counsel before replying, and answer exactly what was asked with nothing volunteered. Informal calls from a regulator are not informal. This is a Red Flags row without exception.

**After any compliance work**, write in the same turn (`memory-template.md`): the regimes, thresholds and their applicability decisions into `## Legal Context` in `memory.md`; every recurring obligation into `## Due` with its owner and cadence; a regulator contact, audit or self-report as a row in `## Matters`; and the durable documents — the compliance register itself, each policy, the incident-response runbook, the evidence index — into `~/Clawic/data/lawyer/artifacts/` with their `## Boxes` lines. The register is the artifact that makes every future diligence questionnaire cheap (`diligence.md`), so it is written once and maintained, never rebuilt.
