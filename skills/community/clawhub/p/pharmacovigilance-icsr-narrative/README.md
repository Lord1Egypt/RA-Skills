# Pharmacovigilance ICSR Narrative Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Pharmacovigilance / Drug Safety — ICH E2D · ICH E2B(R3) · GVP Module VI · 21 CFR 314.80 / 600.80 · MHLW PMSB/ELD-148

## Purpose

An Individual Case Safety Report (ICSR) narrative drafting partner for drug-safety case processors, pharmacovigilance scientists, medical reviewers, QPPV / EU-QPPV staff, US Safety Officers, and PV vendors. Turns a single adverse-event case (spontaneous, solicited, literature, clinical-study, or regulatory-authority source) into a structured DRAFT ICSR narrative aligned to ICH E2D, ICH E2B(R3), and EU GVP Module VI, with a reportability decision (Day 7 / Day 15 / non-expedited), seriousness / expectedness / causality assessment, MedDRA PT mapping prompts, dechallenge / rechallenge logic, and a follow-up question list — for licensed safety-physician / QPPV review before any transmission to FAERS / EudraVigilance / WHO VigiBase / PMDA.

## When to Use

- Drafting a Day 0 initial-case narrative from intake notes (call, web form, HCP letter, literature article, study CRF)
- Drafting follow-up narratives (with linked initial Worldwide Unique Case Identification number) when new information arrives
- Drafting nullification narratives when a case is identified as duplicate or invalid per ICH E2D §1.1.1 criteria
- Standardizing narrative quality across a case-processing team or PV vendor
- Pre-MAA / pre-NDA process design where ICSR narrative SOPs are being authored
- Audit / inspection remediation when narrative deficiencies (missing chronology, missing dechallenge, hedge language, MedDRA mismatch) have been cited

## What It Does

**Phase 1: Case authority and source**
1. Captures the Marketing Authorization Holder / Sponsor / Investigator, the role of the drafter, and the regulatory frame (FDA 21 CFR 314.80 / 600.80 IND/NDA/BLA, EMA GVP Module VI, ICH E2D, ICH E2B(R3) post-market, PMDA, Health Canada, TGA, NMPA)
2. Captures source of the report (spontaneous, solicited from patient-support program / market-research / digital-media monitoring, scientific literature with PubMed ID, clinical study with protocol ID, regulatory authority transfer), reporter qualification (HCP / non-HCP), country of occurrence, country of primary source
3. Captures the four valid-case minimum criteria (identifiable patient, identifiable reporter, suspect product, adverse event/reaction) and refuses to draft until all four are confirmed

**Phase 2: Clocks and reportability**
4. Captures Day 0 (the day any MAH personnel — including affiliates, licensees, contractors — first became aware of the minimum criteria) and computes the calendar-day clock
5. Routes to Day 7 expedited (life-threatening / fatal SUSAR from clinical study under FDA IND or ICH E6 / GVP), Day 15 expedited (serious unexpected post-marketing, fatal/life-threatening clinical-study expected), 90-day non-expedited (US non-serious foreign), PSUR/PBRER (periodic), or country-specific window
6. Flags clock restart triggers (new significant follow-up information) and Worldwide Unique Case ID continuation rule

**Phase 3: PHI-safe intake**
7. Captures patient using non-identifying initials / age / age group / sex / ethnicity (where reported and legally permitted) / weight / height / pregnancy / breastfeeding status
8. Captures relevant medical history, concurrent conditions, family history, lifestyle (alcohol, tobacco, substances) where relevant to the event
9. Captures concomitant medications, herbals / supplements, vaccines (with brand, batch, dose, route, dates)
10. Refuses to record full name, full DOB, full address, national ID, MRN, or insurance ID — those remain only in the source case file under the MAH's data-protection controls

**Phase 4: Suspect product(s)**
11. For each suspect drug / biologic / vaccine / device: brand name, INN / active substance, manufacturer / MAH, batch / lot number, expiration, formulation, strength, route, dose, dose regimen, therapy start and stop dates, indication coded to MedDRA, action taken with the drug (drug withdrawn / dose reduced / dose increased / not changed / unknown / not applicable)
12. Distinguishes suspect from concomitant from interacting
13. Captures product complaint / quality defect linkage and downstream notification to quality

**Phase 5: Adverse event(s) and seriousness**
14. For each reaction: reporter verbatim term, MedDRA LLT proposal with PT roll-up suggestion (the agent suggests; the medical coder confirms), onset date, latency from drug start, duration, outcome (recovered / recovering / not recovered / recovered with sequelae / fatal / unknown)
15. Seriousness per ICH E2A / E2D against the six ICH criteria: **Death**, **Life-threatening**, **Inpatient hospitalization or prolongation**, **Persistent or significant disability / incapacity**, **Congenital anomaly / birth defect**, **Other medically important condition** (and any region-specific criterion, e.g., FDA "important medical event")
16. Captures dechallenge (positive / negative / not applicable / unknown / not done) and rechallenge (positive / negative / not applicable / unknown / not done)

**Phase 6: Expectedness and causality**
17. Expectedness assessed against the Reference Safety Information (Company Core Data Sheet / Investigator Brochure / USPI / SmPC) — agent flags whether the event is **expected** or **unexpected**; medical reviewer confirms
18. Causality captured separately from reporter and from company / sponsor, using the agreed scale (WHO-UMC, Naranjo, sponsor-defined Definitely / Probably / Possibly / Unlikely / Unrelated)
19. Records relevant laboratory data, diagnostic tests, imaging, autopsy findings (where applicable) with units and reference ranges

**Phase 7: Narrative drafting**
20. Drafts a chronological Introduction → Body → Conclusion narrative per ICH E2D §6 and GVP Module VI guidance: patient context → relevant history → product exposure with dates → event onset with latency → dechallenge and outcome → rechallenge (if any) → relevant tests → reporter assessment → company assessment → action taken → outcome
21. Strips hedge / minimizing language ("may", "could be", "possibly suggests", "is unclear whether") from factual statements; reserves uncertainty language for the causality and assessment sections only
22. Produces a follow-up question list targeted to the highest-impact data gaps (case-validity-affecting, reportability-affecting, causality-affecting, outcome)

**Phase 8: Quality self-check**
23. Runs an explicit self-check against ICH E2D / GVP Module VI quality gates (chronology, source, dates, units, dechallenge / rechallenge, expectedness, action taken, outcome, no PHI leakage)
24. Lists residual gaps and reportability flags
25. Produces a DRAFT marked for safety-physician / QPPV review — agent never transmits the ICSR, never marks it "final", never signs off

## Output

A DRAFT narrative packet with:

- Case header (MAH / Sponsor, Worldwide Unique Case Identification number placeholder, country, source, report type, Day 0, reportability category and due date)
- Patient summary (de-identified)
- Medical history / concomitant medications table
- Suspect-product table with batch / dose / route / dates / action taken
- Event table with reporter term → MedDRA LLT proposal → PT proposal → seriousness criteria → outcome → dechallenge / rechallenge
- Free-text Introduction → Body → Conclusion narrative
- Expectedness and dual causality (reporter + company) assessment block
- Follow-up question list
- Unsigned safety-physician / QPPV review block
- Self-check rubric output
- Unresolved-information list

## Safety

This skill drafts a narrative, **not** a regulatory submission. Every output is labeled **DRAFT — SAFETY PHYSICIAN / QPPV MUST REVIEW BEFORE TRANSMISSION**. The agent never assigns the final MedDRA Preferred Term, never finalizes seriousness, never finalizes the company causality, never decides expectedness, never transmits the ICSR to FAERS / EudraVigilance / VigiBase / PMDA / Health Canada / TGA, and never closes a case. PHI is minimized — full patient name, full DOB, full address, MRN, national ID, and insurance ID are refused. Source-document text is summarized, not pasted verbatim. The skill refuses to draft if the four ICH E2D valid-case minimum criteria are not all met (identifiable patient, identifiable reporter, suspect product, adverse event), and instead returns a follow-up question list to recover the missing criterion.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
