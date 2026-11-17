# Employment and Work

The domain where the paperwork matters least and the facts matter most: labels lose to reality, and almost every rule is jurisdictional. US figures below are federal floors — states set higher ones, and non-US systems work on different principles entirely (`jurisdictions.md`). Verify the current figure before relying on it.

**Before answering**, read `## Legal Context` in `~/Clawic/data/lawyer/memory.md` for the entity, its jurisdictions and headcount, and open any `artifacts/policy-*.md` the `## Boxes` index names — an answer that contradicts the user's own handbook creates the claim it was meant to avoid. Anything in the Red Flags table (firing someone who complained, is on leave, or is in a protected category) stops here and goes to counsel.

**Contents:** [Employee Or Contractor](#employee-or-contractor) · [Hiring](#hiring) · [Pay And Hours](#pay-and-hours) · [Restrictive Covenants](#restrictive-covenants) · [IP And Confidentiality From Staff](#ip-and-confidentiality-from-staff) · [Performance And Documentation](#performance-and-documentation) · [Termination](#termination) · [Severance And Releases](#severance-and-releases) · [Collective Redundancy And Layoffs](#collective-redundancy-and-layoffs) · [Leave, Accommodation And Protected Categories](#leave-accommodation-and-protected-categories) · [Complaints And Investigations](#complaints-and-investigations) · [Hiring Across Borders](#hiring-across-borders) · [Policies Worth Having](#policies-worth-having)

## Employee Or Contractor

Misclassification is the most expensive routine mistake in this domain: back taxes, unpaid benefits, penalties and interest, often for several years, plus the contractor's own claim.

| Test | Where it applies | What decides it |
|---|---|---|
| Common-law control test | US federal (IRS), many others | Behavioural control, financial control, and the type of relationship. No single factor governs; the IRS Form SS-8 categories are the working checklist |
| ABC test | California and a growing set of US states | The worker is a contractor only if (A) free from control, (B) performing work outside the hiring entity's usual course of business, and (C) customarily engaged in an independent trade. Prong B fails most software contractors at software companies |
| Employment-status tests | UK and much of Europe | Mutuality of obligation, personal service, control, integration; the UK adds a third "worker" status between employee and self-employed with partial rights |
| Economic-reality test | US FLSA wage claims | Whether the worker is economically dependent on the business |

Observable evidence that a "contractor" is an employee: fixed hours set by the company, no other clients, company equipment and email, attendance at internal performance reviews, line management, integration into a team doing the same work as employees, and an engagement measured in years.

Fixing a misclassification is a project, not an edit: reclassify prospectively, take advice on the back period, and never re-paper history to look different from what happened (`counsel.md`).

## Hiring

- Offer letter versus contract: an offer letter that states salary, start date and at-will status is not a full contract in the US; elsewhere written particulars are mandatory (UK: on or before the first day). Say explicitly what is contractual and what is policy.
- Background checks and references are regulated: US FCRA requires disclosure and authorisation on a standalone document plus a pre-adverse-action notice with a copy of the report; several jurisdictions restrict criminal-history and salary-history questions.
- Right-to-work verification is mandatory and separate from the contract (US Form I-9 within three business days of start; UK share-code checks). Immigration sponsorship is Red Flags.
- Probationary periods exist as a statutory or contractual concept in most non-US systems and shorten notice during the period; in at-will states they add nothing legally but set expectations.
- Job adverts: pay-transparency laws in a growing number of US states and EU member states require a salary range in the posting.

## Pay And Hours

- US federal minimum wage $7.25/hour and overtime at 1.5× after 40 hours in a workweek (FLSA); states and cities set higher minimums and some require daily overtime (California: over 8 hours in a day, double time over 12).
- Exemption from overtime requires both a salary basis above a threshold and a duties test. The federal salary threshold is $684/week ($35,568/year) after the 2024 increase was vacated in litigation; California and New York require substantially more. Job title is irrelevant — the duties test decides.
- Unpaid interns, unpaid trials and "commission-only" arrangements are where wage claims concentrate. Wage claims carry liquidated damages, personal liability for officers in some states, and long lookback periods.
- Payroll deductions are restricted almost everywhere; deducting a laptop, a training cost or a cash shortfall from a final paycheque is usually unlawful without express written authorisation and sometimes even with it.
- Working-time rules outside the US (EU Working Time Directive and national implementations) cap average weekly hours, mandate rest breaks and daily rest, and require records.

## Restrictive Covenants

| Covenant | Typical enforceability | Drafting rule |
|---|---|---|
| Confidentiality | Enforceable nearly everywhere | Perpetual for trade secrets, definite for other information |
| IP assignment | Enforceable, but several US states void assignments of inventions made entirely on the employee's own time without company resources | Include the statutory carve-out notice where required |
| Non-solicit of customers | Usually enforceable if narrow | Limit to customers the employee actually dealt with, 6-12 months |
| Non-solicit of employees | Usually enforceable, narrower each year | Mutual, 12 months, general-advertising carve-out |
| Non-compete | Void in California (Business and Professions Code section 16600, extended by 2024 amendments that also reach out-of-state agreements); heavily restricted in Washington, Colorado, Illinois, Minnesota and others; enforceable if reasonable in most of Europe, often **only if paid** | Duration, geography and scope no wider than the legitimate interest; check whether compensation during the restraint is mandatory |

The FTC's 2024 rule banning most non-competes nationwide was set aside by a federal court before its effective date, so US enforceability remains a state-by-state question. In much of Europe (Germany, France, Italy, Spain among others) a post-termination non-compete requires payment during the restricted period — an unpaid clause is simply void, and a paid one is a real budget line.

Garden leave is the reliable alternative where it exists: keep paying, keep the employee out of the market during notice, and avoid the enforceability fight entirely.

## IP And Confidentiality From Staff

- Employees: work created in the course of employment generally vests with the employer by operation of law in common-law systems; some civil-law systems require an express assignment or additional compensation for inventions (Germany's Employee Inventions Act is the canonical example).
- Contractors: no automatic vesting. Written present assignment or the contractor owns it (`agreements.md`, `ip.md`).
- Open-source and side projects: a policy that pre-approves categories is better than a blanket ban nobody obeys. Blanket bans get ignored and then get litigated.
- Exit: written confirmation of return of property and continuing obligations, plus an access-revocation checklist executed the same day. The confidentiality clause is worth what the offboarding process is worth.

## Performance And Documentation

Termination defensibility is built months earlier. The record needs: contemporaneous written performance concerns, communicated to the employee, with a specific standard and a timeframe, and evidence they were given a chance to improve. A file assembled the week of the termination reads exactly like what it is.

Consistency is the second half: comparable employees treated comparably. Most discrimination claims are proved not by evidence of animus but by an inconsistency the employer cannot explain.

## Termination

- **At-will (most US states)**: dismissal without cause is lawful, but not for an unlawful reason — protected characteristic, retaliation for a complaint or a protected activity, exercising a statutory right, or whistleblowing. The exceptions do most of the work.
- **Everywhere else**: dismissal requires a fair reason and usually a fair process. Statutory notice periods, consultation steps and, in many systems, severance calculated by length of service. The UK requires a fair reason plus a fair procedure for employees past the qualifying period; much of continental Europe requires cause or a negotiated exit for any dismissal.
- Final pay timing is statutory in most US states (California: immediately on involuntary termination, within 72 hours on resignation without notice) with penalties measured in days of pay.
- Accrued holiday payout rules vary; in some jurisdictions untaken statutory leave must be paid out and "use it or lose it" is void.
- Never terminate during a live complaint, an active leave, or immediately after a protected act without counsel. That is the Red Flags row.

## Severance And Releases

Severance buys finality; a release that does not achieve it is a donation.

- **US age claims**: the ADEA as amended by the OWBPA requires 21 days to consider (45 days for a group termination programme, plus disclosure of the ages and job titles of those selected and not selected) and 7 days to revoke after signing. Those periods cannot be waived, and a release that omits them fails as to age claims while binding the employee on everything else.
- Some claims cannot be released at all: filing a charge with an enforcement agency, unemployment benefits, workers compensation in most states, unpaid statutory wages, and whistleblower rights. Confidentiality clauses that appear to prevent regulator contact are unenforceable and increasingly penalised — include an express carve-out.
- **UK**: a settlement agreement waiving statutory claims requires independent legal advice from a named, insured adviser; without it the waiver fails.
- Recent US state laws restrict non-disparagement and confidentiality in agreements covering harassment or discrimination claims; check before drafting either clause.
- Structure: consideration must be something the employee is not already owed. Paying out accrued but unpaid wages is not consideration for a release.

## Collective Redundancy And Layoffs

- **US WARN Act**: employers with 100 or more employees must give 60 days written notice for a plant closing or mass layoff (50+ employees at a single site, or 500+, with a percentage test). Several states have stricter mini-WARN statutes — California's applies at 75 employees with a 50-employee trigger.
- **EU collective-redundancy rules**: information and consultation with employee representatives before decisions are final, with notification to the authority and minimum waiting periods. Skipping consultation invalidates the process and creates protective awards.
- Selection criteria must be objective, documented, and applied consistently, and the resulting pool checked for disparate impact on protected groups before anyone is told.
- Every layoff over a handful of people is a Red Flags escalation: the sequencing errors are unrecoverable once notices go out.

## Leave, Accommodation And Protected Categories

- US FMLA: 12 weeks unpaid job-protected leave per year for eligible employees at employers with 50+ employees within 75 miles; state paid-leave programmes sit on top.
- Disability accommodation (ADA in the US, equivalents elsewhere) requires an interactive process — a documented conversation about possible adjustments. Failure to engage in the process is itself the violation in many cases.
- Pregnancy, parental and caring leave rules are statutory and generous outside the US; a US-drafted handbook applied to European staff is non-compliant on day one.
- Protected characteristics vary by jurisdiction and expand over time. Treat the list as jurisdictional, not universal.

## Complaints And Investigations

When a complaint arrives: acknowledge in writing, preserve documents immediately (`disputes.md`, litigation hold), select an investigator with no reporting line to anyone involved, and keep the process confidential without instructing the complainant to stay silent — a blanket gag on discussing the complaint is unlawful in several systems.

The investigation report is a factual document. Conclusions on legal liability belong with counsel and, written by anyone else, become the plaintiff's best exhibit (SKILL.md Rule 9).

## Hiring Across Borders

Options, in ascending order of cost and commitment: contractor (classification and permanent-establishment risk), employer of record (fast, compliant, ongoing per-head fee), local entity (slow, expensive, necessary above roughly 5-10 people in a country or where an EOR cannot operate).

Watch: permanent establishment created by a person with authority to conclude contracts in-country, mandatory local employment terms that override the chosen law, data transfer for HR records (`privacy.md`), and equity that is taxed differently or is unusable in the local system.

## Policies Worth Having

Small companies need fewer policies than vendors sell, and each one creates an obligation to follow it. The defensible minimum: equal opportunity and anti-harassment with a reporting route, health and safety where required, data protection and acceptable use, expenses, leave, and remote-work arrangements. Handbooks should state they are not contractual, except where local law makes them so.

**After any employment matter**, write in the same turn (`memory-template.md`): headcount, employing entities and jurisdictions into `## Legal Context` in `memory.md`; a termination, settlement or investigation as a row in `## Matters` with its outcome and cost in currency; statutory deadlines (consultation windows, revocation periods, filing dates) into `## Due`; and any policy, template contract, release or investigation procedure that will be reused into `~/Clawic/data/lawyer/artifacts/policy-<name>.md` with its `## Boxes` line. The individual's record, if the user tracks people, goes to the shared `~/Clawic/data/contacts/contacts.md` by name only — never their performance history or health information.
