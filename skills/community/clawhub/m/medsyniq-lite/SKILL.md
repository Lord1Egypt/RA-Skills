---
name: medsyniq-lite
description: "Free medical intelligence for AI assistants. 5 agents, 20 skills. Lite version of MedSynIQ Pro."
version: 1.0.0
license: MIT-0
author: ProFlow Labs AI
homepage: https://medsyniq.com
tags:
  - medicine
  - clinical-reasoning
  - evidence-based-medicine
  - pharmacology
  - biostatistics
  - medical-education
---

# MedSynIQ Lite

Free medical intelligence for AI assistants. 5 agents, 20 skills covering clinical reasoning, pharmacology, evidence-based medicine, biostatistics, and medical education.

> DISCLAIMER: All output is AI-generated educational content. It does not constitute medical advice, diagnosis, or treatment. Clinical decisions must be made by qualified healthcare professionals with direct access to the patient.

## Agents

MedSynIQ Lite includes 5 specialist agents. Each agent activates automatically based on context.

| # | Agent | Domain | Trigger |
|---|-------|--------|---------|
| 1 | clinical-reasoner | Differential diagnosis, Bayesian reasoning, decision rules | Symptoms, cases, diagnostic workup |
| 2 | pharmacologist | Drug interactions, dosing, pharmacokinetics | Medications, prescriptions, drug safety |
| 3 | evidence-appraiser | Critical appraisal, GRADE, evidence synthesis | Study evaluation, guidelines, research quality |
| 4 | biostatistician | Sample size, hypothesis testing, survival analysis | Statistics, study design, power calculations |
| 5 | medical-educator | Teaching cases, learning objectives, curriculum design | Teaching, assessment, clinical training |

## Skills (20 total, 4 per agent)

### Agent 1: Clinical Reasoner

**Skill 1.1 -- Differential Diagnosis**

Generate structured differentials using systematic frameworks.

Frameworks available:
- VINDICATE (Vascular, Infectious, Neoplastic, Degenerative, Iatrogenic, Congenital, Autoimmune, Traumatic, Endocrine)
- Anatomical (skin-to-core walk-through by organ system)
- Worst-first / threat-based (prioritize lethal and time-sensitive diagnoses)
- Pathophysiological (obstruction, perfusion, inflammation, metabolic, neoplastic, immune, structural)

Process:
1. Construct a problem representation using semantic qualifiers
2. Generate initial list using 2+ frameworks (aim for 5-10 diagnoses)
3. Assign pre-test probability tiers: high (>50%), moderate (10-50%), low but consider (1-10%), rare but cannot miss (<1%)
4. Identify key discriminating features between top diagnoses
5. Recommend targeted workup based on diagnostic yield

Cognitive debiasing: Flag anchoring bias, premature closure, availability bias, search satisfying, base rate neglect, and representativeness error. Apply the "rule of three" -- maintain at least three active diagnoses until one is confirmed.

Example -- `/differential 65yo male, acute chest pain, diaphoresis, HTN, DM, smoker`:

> Problem representation: "65-year-old male with multiple cardiovascular risk factors presenting with acute substernal pressure-like chest pain with diaphoresis."
>
> Cannot-miss: ACS (high), aortic dissection (low but must exclude), PE (low)
> Moderate: Hypertensive emergency, unstable angina
> Lower: Pericarditis, GERD, musculoskeletal
>
> Next steps: STAT ECG, serial hs-troponin, CXR, HEART score calculation

See: [references/clinical-reasoner.md](references/clinical-reasoner.md) for full frameworks, illness script template, and worked examples.

**Skill 1.2 -- Bayesian Reasoning**

Apply Bayesian probability updating to diagnostic decisions.

Core calculation:
1. Estimate pre-test probability (clinical prediction rules, prevalence, gestalt)
2. Convert to pre-test odds: odds = probability / (1 - probability)
3. Multiply by likelihood ratio: post-test odds = pre-test odds x LR
4. Convert to post-test probability: probability = odds / (1 + odds)

Likelihood ratio interpretation:
- LR >10 or <0.1: large shift, often conclusive
- LR 5-10 or 0.1-0.2: moderate shift
- LR 2-5 or 0.2-0.5: small but sometimes important
- LR 1-2 or 0.5-1.0: rarely important

Threshold approach: Test only when the result can shift probability across a decision threshold (test threshold or treatment threshold). If pre-test probability is very low or very high, testing may not change management.

Sequential testing: Post-test probability from test 1 becomes pre-test for test 2. Tests must be conditionally independent (D-dimer then CTPA: valid; CRP then ESR: correlated, invalid).

**Skill 1.3 -- Clinical Decision Rules**

Apply validated scoring systems to standardize risk stratification.

| Rule | Application | Components |
|------|-------------|------------|
| Wells (PE) | PE pre-test probability | Clinical signs DVT, PE most likely dx, HR>100, immobilization/surgery, prior VTE, hemoptysis, cancer |
| HEART | Chest pain risk stratification | History, ECG, Age, Risk factors, Troponin |
| CURB-65 | Pneumonia severity | Confusion, Urea >7, RR >=30, BP low, Age >=65 |
| CHA2DS2-VASc | Stroke risk in AF | CHF, HTN, Age, DM, Stroke/TIA, Vascular disease, Sex |
| HAS-BLED | Bleeding risk on anticoagulation | HTN, Abnormal renal/liver, Stroke, Bleeding, Labile INR, Elderly, Drugs/alcohol |
| PERC | PE rule-out without testing | Age <50, HR <100, SpO2 >94%, no hemoptysis, no estrogen, no surgery/trauma, no prior VTE, no unilateral leg swelling |
| Ottawa ankle/knee | Need for radiography | Bone tenderness, inability to weight-bear |
| Centor/McIsaac | Strep pharyngitis probability | Tonsillar exudate, tender anterior cervical nodes, fever, absence of cough, age |

Always report: the score, interpretation, and limitations of the rule for the specific patient.

**Skill 1.4 -- Illness Scripts**

Construct and compare illness scripts for pattern-based reasoning.

Template:
```
DIAGNOSIS: [Name]
EPIDEMIOLOGY: [Who gets this? Age, sex, risk factors, prevalence]
PATHOPHYSIOLOGY: [Mechanism in 1-2 sentences]
TIME COURSE: [Onset, duration, progression]
CARDINAL FEATURES: [3-5 most characteristic findings]
EXPECTED FINDINGS:
  History: [Key symptoms]
  Physical exam: [Key signs]
  Labs/Imaging: [Expected abnormalities]
COMPLICATIONS: [Major if untreated]
KEY DISTINGUISHING FEATURE: [Single feature separating from mimics]
```

Use illness scripts to: rapidly match presentations against known disease patterns, identify features that discriminate between competing diagnoses, and teach diagnostic reasoning through compare-and-contrast.

---

### Agent 2: Pharmacologist

**Skill 2.1 -- Drug Interactions**

Systematic interaction analysis by mechanism.

Pharmacokinetic interactions (CYP450 system):
- CYP3A4 (~50% of drug metabolism): Inhibitors -- ketoconazole, clarithromycin, ritonavir, grapefruit. Inducers -- rifampicin, carbamazepine, phenytoin, St. John's wort. Substrates -- statins (simvastatin, atorvastatin), cyclosporine, tacrolimus, CCBs, midazolam.
- CYP2D6 (~25%): NOT inducible. Polymorphic (7-10% poor metabolizers). Inhibitors -- fluoxetine, paroxetine, bupropion. Substrates -- codeine (prodrug), tamoxifen (prodrug), metoprolol.
- CYP2C19 (~5%): Inhibitors -- omeprazole, fluvoxamine. Key substrate -- clopidogrel (prodrug, poor metabolizers have reduced effect).
- CYP2C9 (~10%): Inhibitors -- fluconazole, amiodarone. Key substrates -- warfarin (S-isomer), phenytoin, sulfonylureas.
- CYP1A2 (~5%): Induced by smoking (PAHs). Inhibitors -- ciprofloxacin, fluvoxamine. Substrates -- clozapine, theophylline. Pearl: smoking cessation raises clozapine levels.
- P-glycoprotein: Efflux transporter. Inhibitors -- amiodarone, verapamil, ritonavir. Substrates -- digoxin, dabigatran.

Pharmacodynamic interactions:
- QT prolongation: Additive risk with multiple QT-prolonging drugs (amiodarone, sotalol, macrolides, fluoroquinolones, haloperidol, ondansetron, methadone). Risk factors: female sex, hypoK, hypoMg, bradycardia.
- Serotonin syndrome: MAOI + any serotonergic (most dangerous). SSRI + tramadol/linezolid. Hunter criteria: clonus is most discriminating feature.
- Nephrotoxic "triple whammy": ACEi/ARB + diuretic + NSAID.
- CNS depression: Opioid + benzo + gabapentinoid (FDA black box).

Severity: Contraindicated > Major > Moderate > Minor.

Example -- `/drug-check warfarin, amiodarone, simvastatin, CKD stage 3`:

> CRITICAL: simvastatin + amiodarone -- CYP3A4 inhibition, rhabdomyolysis risk. Max simvastatin 20mg/day with amiodarone, or switch to pravastatin/rosuvastatin.
> MAJOR: warfarin + amiodarone -- CYP2C9 inhibition, INR elevation. Reduce warfarin dose 30-50%, monitor INR closely for 6-8 weeks.
> MODERATE: CKD stage 3 -- verify renal dosing for all agents.

See: [references/pharmacologist.md](references/pharmacologist.md) for full CYP tables, TDM targets, and worked polypharmacy example.

**Skill 2.2 -- Dose Adjustment**

Individualize drug doses for organ impairment, body composition, and age.

Renal: Cockcroft-Gault for drug dosing (most FDA labels reference CrCl). Formula: CrCl = [(140-age) x weight x (0.85 if female)] / (72 x SCr). High-risk drugs: metformin (stop <30 eGFR), DOACs (agent-specific), digoxin, lithium, gabapentin, enoxaparin.

Hepatic: Child-Pugh score (bilirubin, albumin, INR, ascites, encephalopathy). Class A: usually no change. Class B: reduce 25-50%. Class C: avoid hepatically metabolized drugs. High extraction drugs (morphine, propranolol) have dramatically increased oral bioavailability in cirrhosis.

Obesity: IBW (Devine), AdjBW (IBW + 0.4 x excess), TBW. Aminoglycosides: AdjBW. Vancomycin: TBW. LMWH: TBW (cap 150kg). Chemo: actual weight BSA.

Pediatric: Weight-based (mg/kg), never exceeding adult max. Neonates: immature CYP, extended intervals. Ages 2-6: supranormal metabolism, may need higher mg/kg. Geriatric: start low, go slow. Apply Beers criteria and STOPP/START.

**Skill 2.3 -- Adverse Drug Reactions**

Classify and manage ADRs using the Rawlins-Thompson system.

- Type A (Augmented): Dose-dependent, predictable. 80% of ADRs. Example: bleeding from anticoagulants. Management: dose reduction.
- Type B (Bizarre): Dose-independent, immune/genetic. Example: anaphylaxis, SJS/TEN. Management: stop drug, never rechallenge.
- Type C (Chronic): Cumulative exposure. Example: steroid osteoporosis. Management: monitor, minimize duration.
- Type D (Delayed): Appear after prolonged use. Example: tardive dyskinesia, secondary malignancy.
- Type E (End-of-use): Withdrawal. Example: SSRI discontinuation, clonidine rebound HTN, benzo seizures.

Always check: Is a new symptom actually an ADR before adding another drug (prescribing cascade)?

**Skill 2.4 -- Antimicrobial Stewardship**

Optimize antimicrobial use: right drug, right dose, right duration.

Principles:
1. Start Smart: Obtain cultures before antibiotics. Empiric therapy based on likely pathogens and local resistance patterns. IV-to-oral switch criteria: afebrile 24h, functioning GI, improving WBC/CRP.
2. Then Focus: Review at 48-72h with culture results. De-escalate to narrowest effective spectrum. Set a stop date or review date.
3. PK/PD optimization: Time-dependent killing (beta-lactams) -- maximize time above MIC via extended/continuous infusion. Concentration-dependent (aminoglycosides) -- maximize Cmax/MIC via high-dose extended-interval dosing. AUC/MIC-dependent (vancomycin, fluoroquinolones) -- optimize total drug exposure.

---

### Agent 3: Evidence Appraiser

**Skill 3.1 -- Critical Appraisal**

Appraise research using CASP checklists matched to study design.

Three fundamental questions:
1. Is the study valid? (Internal validity)
2. What are the results? (Effect size, precision)
3. Are the results applicable? (External validity)

RCT appraisal: randomization adequate? Allocation concealed? Blinded? Groups similar at baseline? ITT analysis? Follow-up >80%?

Systematic review: PICO defined? Comprehensive search (PubMed + Embase + CENTRAL minimum)? Dual screening? Quality assessed? Heterogeneity evaluated? Publication bias assessed?

Cohort: Exposure measured accurately? Confounders identified? Follow-up complete? Watch for immortal time bias.

Case-control: Cases/controls clearly defined? Recall bias addressed? Confounders controlled?

Diagnostic: Valid reference standard? Applied to all? Spectrum representative? Blinded interpretation?

See: [references/evidence-appraiser.md](references/evidence-appraiser.md) for full CASP checklists and worked DAPA-HF example.

**Skill 3.2 -- Evidence Levels**

Classify evidence using Oxford CEBM levels and GRADE certainty.

CEBM hierarchy (therapy): 1a (SR of RCTs) > 1b (individual RCT) > 2a-2b (cohort) > 3a-3b (case-control) > 4 (case series) > 5 (expert opinion). Note: optimal design depends on question type (therapy vs diagnosis vs prognosis).

GRADE certainty: High / Moderate / Low / Very Low. RCTs start High, observational starts Low. Downgrade for: risk of bias, inconsistency, indirectness, imprecision, publication bias. Upgrade observational for: large effect (RR >2), dose-response, residual confounding favoring null.

GRADE recommendation: Strong (benefits clearly outweigh risks) vs Conditional (balanced, uncertain, values-dependent). Strong recommendation CAN be based on low-certainty evidence (e.g., parachutes, insulin for T1DM).

**Skill 3.3 -- GRADE Assessment**

Apply the full GRADE framework to a body of evidence.

Steps:
1. Define the clinical question (PICO)
2. Rate each outcome's importance (critical, important, not important)
3. For each outcome, assess starting certainty (RCT = high, observational = low)
4. Apply downgrading factors: risk of bias (-1/-2), inconsistency (-1/-2), indirectness (-1/-2), imprecision (-1/-2), publication bias (-1)
5. Apply upgrading factors (observational only): large effect (+1/+2), dose-response (+1), residual confounding (+1)
6. Determine overall certainty across outcomes (limited by the lowest-rated critical outcome)
7. Formulate recommendation strength considering: certainty, balance of benefits/harms, patient values, resource use

Output as evidence profile table with each domain rated.

**Skill 3.4 -- Quantitative Evidence Synthesis**

Calculate and interpret key clinical metrics.

- ARR (Absolute Risk Reduction): Control event rate minus treatment event rate
- RRR (Relative Risk Reduction): ARR / control event rate
- NNT (Number Needed to Treat): 1 / ARR. Always report with 95% CI and timeframe.
- NNH (Number Needed to Harm): 1 / ARI (absolute risk increase)
- OR vs RR: When outcome prevalence >10%, OR overestimates RR. Use log-binomial or modified Poisson for common outcomes.
- Hazard Ratio: Instantaneous rate ratio. Assumes proportional hazards (constant over time). Check Schoenfeld residuals.

Red flag: A 50% RRR from 0.2% to 0.1% = NNT of 1000. Always demand absolute numbers alongside relative measures.

---

### Agent 4: Biostatistician

**Skill 4.1 -- Hypothesis Testing**

Select and interpret the correct statistical test.

Framework:
1. Define H0 (no effect) and H1 (effect exists)
2. Identify data type: continuous, ordinal, categorical, time-to-event
3. Check assumptions: normality (Shapiro-Wilk, QQ plot), variance equality (Levene's), independence
4. Select test (see table below)
5. Report: test statistic, p-value, confidence interval, effect size

| Scenario | Parametric | Non-parametric |
|----------|-----------|----------------|
| 2 independent groups, continuous | Welch's t-test | Mann-Whitney U |
| 2 paired groups | Paired t-test | Wilcoxon signed-rank |
| 3+ independent groups | One-way ANOVA | Kruskal-Wallis |
| 3+ related groups | Repeated measures ANOVA | Friedman |
| 2 categorical variables | -- | Chi-square / Fisher's exact |
| Correlation | Pearson r | Spearman rho |
| Time-to-event | -- | Log-rank, Cox PH |

P-value: probability of data this extreme given H0 is true. It is NOT the probability that H0 is true. A p=0.04 is not fundamentally different from p=0.06. Always report exact values with CIs and effect sizes.

**Skill 4.2 -- Sample Size Calculation**

Calculate required sample size for study planning.

Core inputs: alpha (0.05), power (80-90%), effect size (MCID), variability (SD or event rate), dropout rate.

Formulas:
- Two means: n/group = 2(Z_a/2 + Z_b)^2 * sigma^2 / delta^2
- Two proportions: n/group = [(Z_a/2 * sqrt(2*p_bar*q_bar) + Z_b * sqrt(p1q1+p2q2))^2] / (p1-p2)^2
- Time-to-event: Events = 4(Z_a/2 + Z_b)^2 / [ln(HR)]^2, then N = events / P(event)
- Non-inferiority: one-sided alpha (0.025), delta_NI = margin
- Cluster-randomized: design effect = 1 + (m-1)*ICC

Example -- `/sample-size RCT, continuous, delta=5, SD=15, power=90%`:

> n/group = 2 * (1.96 + 1.28)^2 * 225 / 25 = 189.
> With 15% dropout: 189 / 0.85 = 223 per group.
> Total: 446 participants.

Adjustments: unequal allocation, covariate adjustment (multiply by 1-R^2), interim analyses (alpha spending).

**Skill 4.3 -- Regression Modeling**

Select and validate the right regression model.

- Linear regression: continuous outcome. Check residuals (normality, homoscedasticity), VIF for multicollinearity (<5), Cook's distance for outliers.
- Logistic regression: binary outcome. Report OR with 95% CI. EPV rule: minimum 10-20 events per predictor. Hosmer-Lemeshow for fit, C-statistic for discrimination.
- Cox proportional hazards: time-to-event. HR interpretation: instantaneous rate ratio. Check PH assumption (Schoenfeld residuals, log-log plots). When violated: stratified Cox, RMST, or time-varying coefficients.
- Poisson/negative binomial: count data. Negative binomial handles overdispersion. Zero-inflated models for excess zeros.

Model building: pre-specified clinical models preferred over stepwise selection (inflates Type I error, produces unstable models).

**Skill 4.4 -- Survival Analysis**

Analyze time-to-event data.

Kaplan-Meier: non-parametric survival curve. Handles right-censoring. Report median survival with 95% CI. Compare groups: log-rank test (optimal when PH holds), Wilcoxon/Breslow (weights early events).

Cox PH: Adjusted hazard ratios. Check PH assumption. When violated: RMST (restricted mean survival time), milestone analysis, weighted log-rank (Fleming-Harrington), landmark analysis.

Competing risks: When another event prevents the outcome of interest (e.g., non-CV death prevents CV death). Use cumulative incidence function (Aalen-Johansen), NOT 1 minus KM. Gray's test for comparison. Fine-Gray model for covariate effects on CIF.

Immortal time bias: In observational studies, misclassifying pre-treatment time as exposed. Fix with landmark analysis or time-varying covariates.

---

### Agent 5: Medical Educator

**Skill 5.1 -- Teaching Case Design**

Build clinical teaching cases that develop reasoning skills.

Structure:
1. Learning objectives (2-3 specific, measurable)
2. Clinical stem (realistic scenario with demographics, presentation, vitals)
3. Progressive disclosure (information released in stages mirroring real clinical workflow)
4. Decision points (what would you do next? what is the differential?)
5. Key teaching pearls (3-5 per case)
6. Debrief framework (what went well, what was missed, what to do differently)

Case complexity levels:
- Novice: classic presentation, single diagnosis, straightforward workup
- Intermediate: atypical features, 2-3 competing diagnoses, decision-making under uncertainty
- Advanced: multi-system, evolving presentation, ethical dilemmas, communication challenges

Cognitive integration: Embed cognitive debiasing (anchoring, premature closure, availability) into case design by including misleading cues that test whether learners maintain broad differentials.

**Skill 5.2 -- Learning Objectives**

Write objectives using Bloom's taxonomy mapped to clinical competence.

| Level | Verb Examples | Clinical Application |
|-------|--------------|---------------------|
| Remember | List, define, name | Recall normal lab values, drug classes |
| Understand | Explain, describe, compare | Describe pathophysiology, compare drug mechanisms |
| Apply | Calculate, demonstrate, use | Calculate CrCl, apply Wells score, use GRADE |
| Analyze | Differentiate, distinguish, examine | Generate differential, identify drug interactions |
| Evaluate | Appraise, justify, critique | Critically appraise an RCT, justify treatment choice |
| Create | Design, construct, develop | Design a study protocol, construct a management plan |

Rules: Each objective should be specific, measurable, achievable, relevant, and time-bound (SMART). Use one active verb per objective. Align objectives with assessment methods.

**Skill 5.3 -- Assessment Design**

Create valid clinical assessments across formats.

Multiple choice questions (MCQs):
- Stem: clinical vignette with sufficient context
- Lead-in: clear, focused question ("What is the most likely diagnosis?" not "Which of the following?")
- Options: one best answer + 3-4 plausible distractors. All options grammatically parallel. Avoid "all of the above" / "none of the above."
- Align with a specific learning objective and Bloom's level

Clinical reasoning assessments:
- Key Feature Questions: focus on critical decision points, not recall
- Script Concordance Tests: present ambiguous scenarios, compare trainee reasoning to expert panel
- OSCE stations: standardized patient encounters testing history, physical exam, communication

Written assessments:
- Case write-ups with structured reasoning (problem representation, differential, workup rationale)
- Evidence appraisal exercises (give a paper, ask for critical appraisal)

**Skill 5.4 -- Curriculum Mapping**

Design and organize medical curricula using competency frameworks.

Competency domains (derived from CanMEDS, ACGME, GMC):
- Medical Expert: clinical knowledge and reasoning
- Communicator: patient communication, shared decision-making
- Collaborator: interprofessional teamwork
- Scholar: evidence appraisal, teaching, lifelong learning
- Professional: ethics, accountability, wellness
- Leader/Manager: resource stewardship, quality improvement
- Health Advocate: social determinants, population health

Spiral curriculum: revisit topics at increasing complexity across training years. Map each session to competency domains and assessment methods. Identify gaps (topics not covered) and redundancies (excessive repetition without progression).

Integration strategies: horizontal (across disciplines within a year) and vertical (across training years). Use case-based learning to integrate basic science with clinical application.

---

## Quick Commands

| Command | What It Does | Agent |
|---------|-------------|-------|
| /differential [presentation] | Structured DDx with frameworks and probability tiers | clinical-reasoner |
| /drug-check [medications, context] | Drug interaction analysis with severity and management | pharmacologist |
| /evidence [PICO question] | Evidence search and appraisal framework | evidence-appraiser |
| /sample-size [design parameters] | Sample size calculation with formula and adjustments | biostatistician |
| /teach-case [topic, level] | Generate a clinical teaching case | medical-educator |

## Rules (Always Active)

1. **Evidence-based**: All clinical claims must reference evidence levels (CEBM or GRADE). Do not fabricate studies or statistics.
2. **Patient safety**: Always flag critical contraindications, cannot-miss diagnoses, dangerous drug interactions, and time-sensitive conditions.
3. **Disclaimer**: All output is AI-generated educational content. Not medical advice. Not a substitute for clinical judgment.
4. **Data privacy**: No patient-identifiable information in outputs. HIPAA/GDPR compliant by design.
5. **Research integrity**: Cite reporting guidelines (CONSORT, STROBE, PRISMA). Apply ICMJE authorship criteria. Disclose limitations.

## Red Flags (Automatic Escalation)

These findings demand immediate flagging regardless of context:

- Hemodynamic instability or shock
- STEMI criteria on ECG
- Contraindicated drug combinations (MAOI + serotonergic, simvastatin + strong CYP3A4 inhibitor at full dose)
- Serotonin syndrome triad (clonus, agitation, hyperthermia)
- QT prolongation with multiple QT-prolonging drugs plus electrolyte derangement
- Nephrotoxic triple whammy (ACEi/ARB + diuretic + NSAID)
- Supratherapeutic anticoagulation without monitoring plan
- Anaphylaxis or Type B ADR to current medication

## File Structure

```
medsyniq-lite-clawhub/
  SKILL.md              -- This file (skill definition)
  LICENSE               -- MIT-0 (ClawHub required)
  references/
    clinical-reasoner.md  -- Full agent: DDx frameworks, illness scripts, Bayesian analysis, worked examples
    pharmacologist.md     -- Full agent: CYP450 tables, TDM targets, polypharmacy worked example
    evidence-appraiser.md -- Full agent: CASP checklists, GRADE methodology, DAPA-HF worked example
    biostatistician.md    -- Full agent: test selection, formulas, SAP structure, CVOT worked example
    medical-educator.md   -- Full agent: case design, Bloom's taxonomy, assessment, curriculum mapping
  scripts/
    disclaimer-check.js   -- Ensures medical disclaimer on clinical outputs
    interaction-warning.js -- Flags dangerous drug combinations
  assets/
    skill-map.txt         -- Visual map of 5 agents and 20 skills
```

## Scope and Limitations

MedSynIQ Lite covers 5 of the 27 agents and 20 of the 142 skills available in MedSynIQ Pro. The Lite edition focuses on core clinical reasoning, pharmacology, evidence-based medicine, biostatistics, and medical education.

Not included in Lite:
- 35 clinical specialty agents (Cardiology, Neurology, Surgery, Pediatrics, Oncology, ICU, ER, etc.)
- Drug development and regulatory skills (15 skills)
- Pharmacovigilance and HEOR (9 skills)
- Epidemiology (6 skills)
- Systematic review and meta-analysis pipeline (5 skills)
- Digital health and precision medicine (8 skills)
- Multi-harness support (Codex, Cursor, OpenCode, Gemini)
- Backend API services (drug interaction database, evidence search)

MedSynIQ Lite -- 5 of 27 agents. Full version with 142 skills: medsyniq.com
