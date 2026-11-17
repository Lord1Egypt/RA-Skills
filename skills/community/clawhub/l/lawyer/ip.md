# Intellectual Property

Four different rights with four different creation events, four different clocks, and one shared failure mode: doing the commercial thing first and the legal thing afterwards, by which time the right no longer exists.

**Before answering**, read `## Legal Context` and `## Due` in `~/Clawic/data/lawyer/memory.md` for the existing portfolio and its renewal dates, and open `filings/<year>.md` per the `## Boxes` index for what has already been filed. Filing a second application for a mark that is already registered is a real and common waste.

**Contents:** [Which Right Applies](#which-right-applies) · [Copyright](#copyright) · [Trademark](#trademark) · [Patent](#patent) · [Trade Secret](#trade-secret) · [Ownership: Who Actually Has It](#ownership-who-actually-has-it) · [Open Source](#open-source) · [AI-Generated Output](#ai-generated-output) · [Licensing In And Out](#licensing-in-and-out) · [Enforcement](#enforcement) · [Someone Says You Infringe](#someone-says-you-infringe) · [Portfolio Hygiene](#portfolio-hygiene)

## Which Right Applies

| Protects | Right | Exists from | Lasts |
|---|---|---|---|
| Expression: code, text, images, music, designs | Copyright | The moment it is fixed in a tangible form; no filing needed to exist | Life + 70 years in most systems; 95 years from publication for US works made for hire |
| Brand identifiers: names, logos, slogans, sometimes sounds and colours | Trademark | Use in commerce (common-law systems) or registration (most of the world) | Indefinite while used and renewed |
| Inventions: how something works | Patent | Grant, following a filing | 20 years from filing, subject to maintenance fees |
| Information with commercial value from being secret | Trade secret | The moment reasonable secrecy measures exist | As long as it stays secret |
| Product appearance | Design right / design patent | Registration (or unregistered rights in some systems, short-lived) | Typically 15-25 years registered |

The same product carries several: the code is copyright, the name is a trademark, the algorithm may be patentable, the customer list is a trade secret, and the UI may carry design rights.

## Copyright

- Automatic on creation; registration is a separate, jurisdictional layer that unlocks remedies. In the US, registration is a precondition to filing an infringement suit (*Fourth Estate v Wall-Street.com*, 2019), and **statutory damages and attorney's fees are available only if registration preceded the infringement, or occurred within three months of first publication** — a $65 filing that decides whether litigation is economically possible.
- Statutory damages range $750-$30,000 per work, up to $150,000 for willful infringement.
- Copyright protects expression, never ideas, methods or facts. Two independently written implementations of the same algorithm do not infringe each other.
- Moral rights (attribution, integrity) exist in most non-US systems, cannot be assigned, and are waivable in some jurisdictions and not others. A US-style assignment clause with no moral-rights waiver is incomplete for European contributors.
- DMCA safe harbour for platforms hosting user content requires a designated agent registered with the US Copyright Office, a repeat-infringer policy, and prompt takedown on notice. The agent registration must be renewed every three years or the safe harbour lapses.

## Trademark

- Search before adopting: identical and confusingly similar marks in the relevant classes, in every territory that matters, plus company registers, domains and app stores. Rebranding after launch costs more than any clearance search.
- Registration is by class (Nice Classification, 45 classes). File in the classes covering current and near-term goods and services; a software company usually needs class 9 and class 42, often 35 and 41.
- **Timing**: most of the world is first-to-file, so someone can register the user's brand in a market before they get there. The US is use-based, with intent-to-use applications that must be converted by filing a statement of use — extensions run in six-month increments up to a maximum of three years from allowance.
- **Maintenance (US)**: a Section 8 declaration of continued use between the fifth and sixth anniversary, a combined Section 8 and 9 renewal every ten years. Missing either cancels the registration. Most systems renew every ten years.
- Distinctiveness spectrum decides how much protection there is: fanciful (Kodak) > arbitrary (Apple for computers) > suggestive > descriptive (registrable only with acquired distinctiveness) > generic (never). A descriptive name is cheap to market and expensive to defend.
- Genericide is real (escalator, aspirin in some markets). Use the mark as an adjective on a generic noun, never as a verb or a plural, and police obvious misuse.
- Madrid Protocol allows filing in many countries from one application, based on a home registration — cheaper, but a "central attack" on the base registration in the first five years takes the whole family down.

## Patent

- Requirements: novel, non-obvious (inventive step), and useful, in a patentable category. Software and business methods are patentable in the US only within limits set by *Alice v CLS Bank* (2014); in Europe, software is excluded "as such" and needs a technical effect.
- **Absolute novelty outside the US**: any public disclosure before filing destroys patentability in Europe, China and most of the world. The US has a one-year grace period after the inventor's own disclosure. This is the deadline that gets missed at a launch or a conference talk.
- Provisional application (US) buys 12 months at low cost and establishes a priority date, but only for what it actually describes — a thin provisional protects nothing. The non-provisional must be filed within 12 months, no extensions.
- The Paris Convention gives 12 months from the first filing to file abroad with the original priority date; a PCT application extends the decision on which countries to roughly 30 months from priority, at which point national-phase costs arrive together and are substantial.
- Maintenance fees are due at intervals for the life of the patent; missing one lapses the right.
- Cost reality: a US utility patent from drafting through grant commonly runs into five figures with attorney fees, before foreign filings. Patents are a budget decision as much as a legal one.

## Trade Secret

Protection exists only while the information is secret **and** reasonable measures were taken to keep it so — that second half is what gets litigated. Evidence of reasonable measures: NDAs with everyone who sees it, access controls and least privilege, marking, exit interviews and access revocation, a written policy, and physical controls where relevant.

The US Defend Trade Secrets Act (2016) created a federal civil cause of action with seizure remedies, and requires an immunity notice in employee and contractor confidentiality agreements — omitting it forfeits exemplary damages and fees in a later case. The EU Trade Secrets Directive harmonised protection across member states on a similar "reasonable steps" standard.

Trade secret versus patent: a patent trades disclosure for a 20-year monopoly; a trade secret lasts forever but dies on independent discovery or reverse engineering, both of which are lawful. Choose by whether the invention is detectable in the shipped product.

## Ownership: Who Actually Has It

| Creator | Default owner | What to do |
|---|---|---|
| Employee, in the course of employment | Employer, in most common-law systems | Confirm in the contract; some civil-law systems need express assignment or extra compensation for inventions |
| Contractor or agency | **The contractor**, unless there is a written assignment | Present-tense assignment plus moral-rights waiver, tied to payment (`agreements.md`) |
| Founder, before incorporation | The founder personally | Assign into the company at formation — the single most common gap found in diligence (`diligence.md`) |
| Joint authors | Jointly, with rules that differ sharply: US co-owners can each license non-exclusively without consent; UK and most of Europe require consent | Agree ownership in writing before the collaboration |
| Commissioned agency work | Usually the agency | Check every logo and every website; brands routinely do not own their own marks |

US "work made for hire" for a non-employee applies only to nine enumerated categories plus a signed writing, and software is not one of them. Rely on assignment language, not on the phrase.

## Open Source

Every licence is a copyright licence with conditions; using the code without meeting the conditions is infringement, not a contract breach.

| Family | Examples | Obligation | Where it bites |
|---|---|---|---|
| Permissive | MIT, BSD, Apache 2.0 | Attribution, licence text, notice of changes (Apache) | Shipping without the notice file; Apache 2.0 also grants patent rights and terminates them on patent litigation |
| Weak copyleft | LGPL, MPL 2.0, EPL | Source for the licensed component and its modifications | Static linking under LGPL, which pulls in more than dynamic linking |
| Strong copyleft | GPL 2.0, GPL 3.0 | Source for the whole derivative work, on distribution | Distributing a binary; GPL 3.0 adds anti-tivoization and patent terms |
| Network copyleft | AGPL 3.0 | Source obligations triggered by **network use**, not distribution | SaaS — the licence most likely to be violated silently by a hosted product |
| Source-available, not open source | BSL, SSPL, Elastic Licence | Field-of-use restrictions | Commercial hosting; these are not OSI-approved and read as ordinary licences |

Practical programme: generate a software bill of materials in the build, block licences on a deny list at CI time, keep the attribution notice file generated rather than hand-written, and record the licence position for anything ambiguous in an artifact. Warrant open-source compliance in customer contracts only if this exists (`clauses.md`).

## AI-Generated Output

- **Authorship**: the US Copyright Office has consistently held that purely machine-generated output without human authorship is not registrable, while human-authored selection, arrangement and modification can be. Other offices have taken varying positions. Treat model output as unprotected unless a human contribution is documented.
- **Inputs**: training-data and output-similarity litigation is active in several jurisdictions and unsettled. Assume nothing is decided.
- **Contractual exposure**: customer contracts increasingly require warranties that deliverables are original and non-infringing. A deliverable produced by a model cannot honestly carry an unqualified originality warranty unless a human process verifies it — negotiate the warranty scope or build the verification (`clauses.md`).
- Vendor terms for AI tools differ on who owns output, whether inputs train the model, and what indemnity is offered. Check the tier: indemnities are often limited to paid enterprise plans and conditioned on using the safety filters.
- The EU AI Act phases obligations by risk category across 2025-2027 with prohibited practices already in force; whether it applies at all depends on role (provider, deployer) and use case (`compliance.md`).

## Licensing In And Out

Grant anatomy, every time: exclusive or non-exclusive · territory · field of use · term · sublicensable or not · transferable or not · royalty or fixed fee · improvements (who owns them) · termination and what happens to the licensee's existing customers.

Exclusive licences require care: an exclusive licence can leave the owner unable to use their own IP unless "sole" (owner plus one licensee) is specified. Field-of-use and territorial limits are the standard way to grant exclusivity without giving away everything.

## Enforcement

Escalation ladder, cheapest first: informal contact → cease-and-desist letter → platform takedown (DMCA for copyright, marketplace and app-store brand programmes for trademark, domain UDRP for cybersquatting) → opposition or cancellation proceeding at the registry → litigation.

Platform takedowns resolve most consumer-facing infringement in days at near-zero cost and are the correct first move for a copied listing, a cloned app or a stolen photo. Note that a bad-faith DMCA notice carries liability under 17 USC 512(f), so the claim must be genuine.

A cease-and-desist is a real legal act with real consequences: it can trigger a declaratory-judgment action in a forum of the recipient's choosing, and an aggressive letter to a sympathetic defendant becomes a public-relations event. Send it deliberately (`disputes.md`).

## Someone Says You Infringe

1. Preserve everything and stop deleting (`disputes.md`).
2. Do **not** admit, and do not have engineers write assessments in email — those become discoverable analyses of a known infringement, which is how willfulness and treble damages arrive.
3. Check the claim's basics: does the right exist and is it in force (registers are public), does it cover this territory and this class, and is the claimant the owner?
4. Route to specialist counsel before responding. Patent assertion, in particular, has economics of its own and general commercial reasoning does not apply.
5. Check the indemnity chain: if the infringing component came from a supplier, their IP indemnity is now live and they should be notified within the contractual window (`clauses.md`).

## Portfolio Hygiene

Annual pass: marks in use versus registered classes, renewal dates, domains and social handles matching the marks, assignment chain complete from every founder and contractor, open-source manifest current, and any expired or abandoned right that should be revived or dropped deliberately.

**After any IP action**, write in the same turn (`memory-template.md`): a filing, registration, assignment or renewal as a row in `~/Clawic/data/lawyer/filings/<year>.md` with the application number, class, territory and date; every renewal, statement-of-use and maintenance deadline into `## Due` in `memory.md`; the portfolio summary into `## Legal Context`; and any reusable output — an open-source policy, an IP assignment template, an infringement-response procedure — into `~/Clawic/data/lawyer/artifacts/` with its `## Boxes` line. Registration numbers are public identifiers and belong in the file; portal logins for the registry do not (SKILL.md, secrets).
