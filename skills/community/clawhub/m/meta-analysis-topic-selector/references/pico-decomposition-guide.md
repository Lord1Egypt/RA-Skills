# PICO/PECO Element Decomposition Guide

This file guides how to decompose a vague research interest into an operational PICO/PECO structure. Load it when the user provides a research direction but has not specified population / intervention / comparator / outcomes.

## 1. Why explicit decomposition is required

PICO/PECO is the "constitution" of a meta-analysis topic:
- Defines the precise boundary of the search strategy
- Defines the operability of eligibility criteria
- Defines the data-extraction fields
- Defines the prespecified subgroups for heterogeneity analysis
- Defines the choice of effect size

A vague PICO (e.g., "efficacy of PD-1 in liver cancer") inevitably leads to messy searches, eligibility disputes, and uninterpretable pooling. **At the topic stage, PICO must be decomposed to a "protocol-ready" granularity.**

## 2. PICO four-element decomposition spec

### P — Population

Operational requirement: every qualifier must be expressible in a search string.

Required fields:
- Disease name (ICD-10 / standardized nomenclature)
- Disease stage/subtype (e.g., Barcelona Clinic Liver Cancer stage B)
- Age range (e.g., ≥18 years)
- Sex restriction (if any)
- Key comorbidities or prior therapy (e.g., "no prior systemic therapy")
- Excluded populations (e.g., "exclude active HBV/HCV, HIV")

Bad example:
- P: hepatocellular carcinoma patients

Good example:
- P: adults (≥18 years) with histologically or radiologically confirmed unresectable HCC, BCLC stage B–C, Child-Pugh A, no prior systemic therapy; exclude active HBV/HCV, HIV, other malignancy history.

### I/E — Intervention/Exposure

Operational requirement: specify dose, duration, route, follow-up window.

Required fields:
- Intervention/exposure name (INN generic name + trade-name note)
- Dose range (e.g., 200 mg q3w)
- Route (IV / PO / SC / topical)
- Duration (e.g., "until disease progression or intolerable toxicity")
- Combination regimen (e.g., "PD-1 + TKI" must specify the TKI and its dose)
- Follow-up window (primary outcome measurement timepoint, e.g., "12 months after treatment start")

Bad example:
- I: PD-1 inhibitor

Good example:
- I: PD-1 inhibitor (pembrolizumab 200 mg q3w, or nivolumab 240 mg q2w, or tislelizumab 200 mg q3w) combined with lenvatinib (12 mg qd if weight ≥60 kg; 8 mg qd if <60 kg), treated until disease progression, intolerable toxicity, or 24 months.

### C — Comparator

Operational requirement: specify comparator type and regimen.

Comparator-type enumeration:
- Placebo
- Active comparator (standard of care / SOC)
- Different dose
- Different route
- Different combination regimen
- No treatment / observation

Required fields:
- Comparator name
- Comparator dose/duration (matched to I in granularity)
- Crossover/switching allowed?

Example:
- C: lenvatinib monotherapy (12 mg qd if weight ≥60 kg; 8 mg qd if <60 kg), or sorafenib 400 mg bid, treated until disease progression, intolerable toxicity, or 24 months.

### O — Outcome

Operational requirement: specify primary and secondary outcomes; each outcome must specify measurement tool, timepoint, and effect-size type.

Required fields:
- Outcome name
- Measurement tool/definition (e.g., OS by date of death; ORR per RECIST 1.1)
- Measurement timepoint (e.g., "at least 12 months of follow-up after treatment start")
- Effect-size type (HR / RR / OR / SMD / RD / DOR, etc.)
- Is it a time-to-event outcome? (affects effect-size choice)

Recommended primary outcomes (by importance, 1–2):
- Overall survival (OS) — time-to-event — HR
- Progression-free survival (PFS) — time-to-event — HR

Recommended secondary outcomes (4–8):
- Objective response rate (ORR) — binary — RR
- Disease control rate (DCR) — binary — RR
- Serious adverse event rate (SAE) — binary — RR
- Quality of life (QoL) — continuous — SMD
- Grade 3–4 treatment-related adverse events (TRAE) — binary — RR

## 3. PECO variant (exposure studies)

Applies to meta-analyses of observational studies (e.g., environmental exposure, lifestyle, genetic association):

- **P** — Population: as above
- **E** — Exposure: exposure definition (exposure level, exposure window, exposure measurement method)
- **C** — Comparison: reference group (unexposed / low exposure / different genotype)
- **O** — Outcome: as above

Extra fields for observational studies:
- Study-design restriction (cohort / case-control / cross-sectional)
- Exposure measurement tool (questionnaire / biomarker / workplace monitoring)
- Adjustment variables (confounders to be adjusted in the statistical analysis must be listed)

## 4. PICO decomposition quality self-check list

After decomposing PICO, self-check item by item:

- [ ] Every P qualifier can be written into a search string (if a qualifier cannot be expressed → not operational enough)
- [ ] I/E dose, duration, follow-up window complete
- [ ] C and I are matched in granularity
- [ ] O includes at least one time-to-event outcome (OS or PFS recommended)
- [ ] O effect-size type is explicit
- [ ] Primary outcomes ≤2
- [ ] The PICO as a whole can be written as a one-sentence research-question statement

Research-question statement template:
> In [P], does [I] compared with [C] improve [O]?

Example:
> In adults with unresectable HCC (BCLC B–C, Child-Pugh A, treatment-naïve), does PD-1 inhibitor combined with lenvatinib compared with lenvatinib monotherapy improve overall survival and progression-free survival?

## 5. Common decomposition errors

1. **I and C unmatched in granularity**: I is detailed (PD-1 + lenvatinib), C is coarse ("standard of care") → the comparator cannot be subgrouped
2. **P too broad**: "solid tumor patients" → heterogeneity explosion, unpoolable
3. **P too narrow**: "BCLC B with ALBI grade 1 and Eastern-Asian population" → <5 included studies
4. **O missing timepoint**: "response rate" → RECIST version and measurement timepoint not specified
5. **Key exclusion missing**: did not exclude prior immunotherapy history → heterogeneity source unexplained
6. **Combination not decomposed**: I = "PD-1 + targeted" without specifying the targeted agent → dose-response not comparable

## 6. Complex-intervention decomposition spec

When the intervention is not "a single drug at a fixed dose", you must decompose per the spec below; otherwise subgroup and dose-response analyses cannot be executed later.

### 6.1 Combination therapy

Definition: I consists of ≥2 drugs used concurrently.

Decomposition spec:
- List each component drug + dose + route + duration
- Specify the temporal relationship of the combination (concurrent start / sequential addition / induction-then-maintenance)
- Specify what happens to the whole regimen when any component is stopped
- C must also be decomposed at the same granularity (avoid "I detailed, C coarse")

Required fields:
- Component 1: drug name + dose + frequency + route + duration
- Component 2: drug name + dose + frequency + route + duration
- Combination timing: [concurrent / component 1 first for X weeks then add component 2 / ...]
- Stop rule: [any component stopped → stop all / any component stopped → continue the other as monotherapy / ...]

Bad example: I = PD-1 + lenvatinib

Good example:
```
I = Combination regimen
  Component 1: pembrolizumab 200 mg q3w IV (or nivolumab 240 mg q2w / tislelizumab 200 mg q3w)
  Component 2: lenvatinib (≥60 kg: 12 mg qd PO; <60 kg: 8 mg qd PO)
  Combination timing: concurrent start
  Duration: treat until PD / intolerable toxicity / 24 months (whichever comes first)
  Stop rule: if any component is stopped for toxicity → the other may continue as monotherapy until PD
```

### 6.2 Titration scheme

Definition: I's dose is stepwise adjusted based on response or tolerability.

Decomposition spec:
- List starting dose, adjustment condition, target dose, maximum dose
- Specify the adjustment time window (e.g., "assess every 4 weeks")
- Specify the dose-reduction rule (e.g., grade 3 toxicity → reduce by one level)

Required fields:
- Starting dose
- Adjustment condition (insufficient response / toxicity / both)
- Adjustment step (increase/decrease amount)
- Target dose (therapeutic window)
- Maximum dose ceiling / minimum dose floor

Bad example: I = lenvatinib gradually up-titrated

Good example:
```
I = lenvatinib titration scheme
  Start: 8 mg qd PO (regardless of weight)
  Adjustment condition: after 4 weeks, if well tolerated (≤grade 1 toxicity) and lesions have not shrunk → increase to 12 mg qd
  Reduction condition: grade 3 toxicity → reduce to 4 mg qd; grade 4 toxicity → permanently discontinue
  Maximum dose: 12 mg qd
  Minimum dose: 4 mg qd (below this → discontinue)
```

### 6.3 Sequential therapy

Definition: I and C are used in sequence over time; the comparison is "I then C" vs "C then I", or "I then C" vs "C throughout".

Decomposition spec:
- Specify each phase's drug + dose + start/stop condition
- Specify the transition trigger event (PD / time / toxicity / response)
- C must also match the sequential structure (avoid asymmetric comparators)

Required fields:
- Induction phase: drug + dose + duration + transition trigger
- Maintenance/consolidation phase: drug + dose + duration + transition trigger
- Handling when transition is not feasible

Example:
```
I = Sequential regimen
  Induction: TACE (1–3 sessions, every 4–6 weeks) + lenvatinib 12 mg qd, until maximal tumor shrinkage
  Transition trigger: radiographic PD or no further shrinkage at 4–6 weeks
  Consolidation: lenvatinib 12 mg qd + PD-1 inhibitor 200 mg q3w, until PD/toxicity
C = Sequential comparator
  Induction: TACE (same) + lenvatinib 12 mg qd
  Consolidation: lenvatinib 12 mg qd monotherapy, until PD/toxicity
```

### 6.4 Planned switch

Definition: I switches to another regimen at a fixed timepoint or after an event, compared with "no switch throughout".

Decomposition spec:
- Specify the switch timepoint (X weeks after treatment start / after X cycles) or switch event (CR / ORR reached)
- Specify the pre-switch and post-switch regimens
- Specify the handling when the switch condition is not met

Required fields:
- Pre-switch regimen: drug + dose + duration
- Switch condition: [fixed timepoint / response event / both]
- Post-switch regimen: drug + dose + duration
- Handling when switch condition not met: [continue pre-switch / switch to another / discontinue]

### 6.5 Complex-intervention PICO self-check (supplement)

In addition to the general self-check, after decomposing a complex intervention, also check:

- [ ] Combination: each component drug + dose + duration is explicit
- [ ] Combination: combination timing (concurrent/sequential/induction-then-maintenance) is explicit
- [ ] Combination: stop rule is explicit
- [ ] Titration: starting dose, adjustment condition, target dose, maximum dose are all explicit
- [ ] Sequential: each phase's drug, dose, transition trigger are all explicit
- [ ] Planned switch: switch condition + post-switch regimen + not-met handling are all explicit
- [ ] C and I are structurally matched (both combination / both titration / both sequential), or the difference is clearly explained
- [ ] Subgroup analyses for the complex intervention are prespecified (e.g., by component-1 dose, by whether the switch condition was met)

### 6.6 Complex interventions and meta-type

Complex interventions usually affect the meta-type choice:
- Combination + multiple comparators → favors NMA (network comparison across combination regimens)
- Titration + dose response → favors dose-response meta
- Sequential + complex timing → may need multivariate meta or scenario-based subgroups
- Planned switch + time-to-event → standard pairwise + time-dependent subgroup
