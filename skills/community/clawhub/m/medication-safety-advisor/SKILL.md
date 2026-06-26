---
name: medication-safety-advisor
version: 1.0.3
description: "Use this skill when a clinician, pharmacist, or care coordinator needs to check drug-drug interactions, verify formulary coverage tiers, look up dosing guidelines, or flag contraindications for a patient's medication list. Uses the free OpenFDA API and RxNorm — no API key required. Supports single drug lookups, multi-drug interaction checks, allergy cross-checks, and payer formulary tier lookups. DO NOT use for prescribing decisions — this skill assists with safety checks and information only."
tags: ["healthcare", "pharmacy", "drug-interactions", "formulary", "rxnorm", "openfda", "medications", "safety"]
author: "optimusprime19"
license: "MIT"
homepage: https://github.com/optimusprime19/medication-safety-advisor
repository: https://github.com/optimusprime19/medication-safety-advisor
optionalEnv:
  - FORMULARY_API_KEY  # Optional: for real-time payer formulary lookups
---

# Drug Interaction & Formulary Checker

## Overview

This skill checks drug-drug interactions, allergy contraindications, formulary coverage, and dosing guidelines using free public APIs — no credentials required out of the box.

**What it can do:**
- Check interactions between 2 or more drugs
- Look up a full medication list for interactions
- Check formulary tier and coverage for a payer
- Flag allergy contraindications
- Provide standard adult dosing ranges
- Suggest therapeutic alternatives when a drug is not covered

**APIs used (all free, no key needed):**
- **OpenFDA** — drug interactions, adverse events, labeling
- **RxNorm API** (NLM) — drug name normalization and RxCUI lookup
- **NLM DailyMed** — official drug labeling and prescribing info

> ⚠️ **Clinical Disclaimer:** All output is informational only and must be reviewed by a licensed clinician or pharmacist before any prescribing or dispensing decision.

> 🔒 **Privacy / PHI Warning:** This skill sends drug names and allergy information to public APIs (RxNorm, OpenFDA, DailyMed). **Do not include patient-identifiable information** (names, MRNs, DOBs, addresses, or other PHI) in any query. Use drug names and clinical terms only. For production use with real patient data, ensure your deployment satisfies HIPAA requirements and that a BAA is in place with any third-party service.

---

## Trigger Phrases

- "Check interactions for [drug list]"
- "Is it safe to take [drug A] with [drug B]?"
- "Check this patient's med list for interactions"
- "What tier is [drug] on [payer] formulary?"
- "Is [drug] covered by BlueCross?"
- "What's the standard dose for [drug]?"
- "Are there any contraindications with [drug] for a patient allergic to [allergen]?"
- "Suggest an alternative to [drug] that's on formulary"

---

## Drug Interaction Checks

### Single pair check
```
"Check interactions between Warfarin and Aspirin"
"Is it safe to combine Metformin and Lisinopril?"
```

### Full medication list check
```
"Check this med list for interactions:
- Metformin 1000mg BID
- Lisinopril 10mg daily
- Atorvastatin 40mg daily
- Aspirin 81mg daily
- Omeprazole 20mg daily"
```

**What the agent does:**
1. Normalizes all drug names via RxNorm API
2. Queries OpenFDA drug interactions for each pair
3. Ranks interactions by severity (Major / Moderate / Minor)
4. Returns a structured interaction report

**Example output:**
```
DRUG INTERACTION REPORT
Patient Med List: 5 medications checked
Pairs checked: 10

⛔ MAJOR (1):
• Warfarin + Aspirin
  Risk: Increased bleeding risk. Combined antiplatelet 
  and anticoagulant effect.
  Action: Monitor INR closely. Consider GI protection.

⚠️ MODERATE (2):
• Lisinopril + Potassium supplements
  Risk: Hyperkalemia risk.
  Action: Monitor serum potassium.

• Atorvastatin + Clarithromycin
  Risk: Increased statin exposure, myopathy risk.
  Action: Temporarily hold statin if antibiotic needed.

✅ MINOR / NO INTERACTION (7):
  Remaining pairs — no clinically significant interactions found.

Source: OpenFDA + RxNorm | For clinician review only
```

---

## Allergy Contraindication Check

```
"Check if any of these meds are contraindicated 
 for a patient with penicillin allergy"

"Patient is allergic to sulfa drugs — 
 is Bactrim safe?"
```

**What the agent does:**
1. Looks up drug class and cross-reactivity data from OpenFDA labeling
2. Flags any drugs in the same class as the allergen
3. Suggests safe alternatives where available

---

## Formulary & Coverage Lookup

```
"What tier is Ozempic on BlueCross formulary?"
"Is Humira covered by Aetna?"
"Find a formulary-covered alternative to Jardiance"
```

**What the agent does:**
1. Looks up the drug's generic name and drug class via RxNorm
2. If `FORMULARY_API_KEY` is set: queries the real-time payer formulary API for tier and coverage data
3. If no key is set: instructs the agent to tell the user to verify tier directly with the payer's online formulary tool — no estimated or cached data is used
4. Suggests covered alternatives in the same drug class based on RxNorm drug class data

> Note: Without `FORMULARY_API_KEY`, this skill does **not** provide formulary tier estimates. Always confirm coverage with the payer's online formulary tool or pharmacy benefit line before clinical use.

**Example output:**
```
FORMULARY CHECK — Ozempic (semaglutide)
Payer: BlueCross BlueShield PPO

Tier: 4 (Non-Preferred Brand)
Est. Copay: $80-120/month (with standard benefit)
Prior Auth Required: Yes
Step Therapy Required: Yes (must try Metformin first)

Covered Alternatives (Tier 2):
• Trulicity (dulaglutide) — Tier 2, $45/month
• Victoza (liraglutide) — Tier 2, $50/month

Recommendation: Consider Trulicity as first-line 
if cost is a barrier. PA may be approved if 
patient has failed oral agents.
```

---

## Dosing Reference

```
"What's the standard dose for Metformin?"
"Dosing for Lisinopril in CKD?"
"Max dose of Acetaminophen per day?"
```

**Example output:**
```
DOSING REFERENCE — Metformin (metformin HCl)

Standard Adult Dose:
• Starting: 500mg BID or 850mg once daily with meals
• Titration: Increase by 500mg/week as tolerated
• Maximum: 2550mg/day (divided doses)

Renal Dosing:
• eGFR 30-45: Use with caution, max 1000mg/day
• eGFR <30: CONTRAINDICATED

Common Side Effects: GI upset, nausea (take with food)
Black Box Warning: Lactic acidosis (rare)

Source: FDA prescribing information via OpenFDA
```

---

## API Reference

### RxNorm — Drug Name Normalization
```
GET https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}
→ Returns RxCUI (standard drug identifier)

GET https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={id}
→ Returns interaction data for a drug
```

### OpenFDA — Interactions & Labeling
```
GET https://api.fda.gov/drug/label.json?search=openfda.brand_name:{name}
→ Returns full drug labeling including interactions section

GET https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{name}
→ Returns adverse event reports
```

### NLM DailyMed
```
GET https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={name}
→ Returns structured product labeling
```

---

## Example Workflows

### Quick interaction check before prescribing
```
Clinician: "Adding Clarithromycin for a patient 
            already on Atorvastatin — any issues?"

Agent: "⚠️ MODERATE INTERACTION DETECTED
        Clarithromycin inhibits CYP3A4, significantly 
        increasing Atorvastatin exposure. Risk of myopathy 
        and rhabdomyolysis.
        
        Recommendation: Temporarily hold Atorvastatin 
        during antibiotic course, or switch to Azithromycin 
        which has no significant statin interaction."
```

### Full med reconciliation on admission
```
Clinician: "Patient admitted with these home meds, 
            check for interactions:
            Warfarin, Amiodarone, Metoprolol, 
            Furosemide, Potassium Chloride, Digoxin"

Agent: [Checks all 15 pairs]
       "⛔ 2 MAJOR interactions found:
        • Amiodarone + Warfarin: Markedly increases 
          INR. Reduce Warfarin dose by 30-50%.
        • Amiodarone + Digoxin: Increases Digoxin 
          levels. Monitor levels and reduce dose."
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-29 | Initial release. Interaction checks, formulary lookup, dosing reference, allergy contraindication check. |
