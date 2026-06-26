---
name: medical-billing-coder
version: 1.0.3
description: "Use this skill when a clinician, biller, or practice manager needs to look up ICD-10 diagnosis codes, CPT procedure codes, or E&M visit level codes. Takes a clinical note, visit summary, or plain-language description and suggests the most appropriate billing codes with confidence scores and audit trail. Also validates code combinations, checks for common denials, and flags upcoding or undercoding risks. DO NOT use as the sole basis for claim submission — all codes must be reviewed and approved by a qualified medical coder or clinician."
tags: ["healthcare", "billing", "icd-10", "cpt", "coding", "revenue-cycle", "claims", "em-coding"]
author: "optimusprime19"
license: "MIT"
homepage: https://github.com/optimusprime19/medical-billing-coder
repository: https://github.com/optimusprime19/medical-billing-coder
optionalEnv:
  - CMS_API_KEY  # Optional: calls https://api.cms.gov/medicare-coverage-database/v2 for real-time NCCI edit validation. No clinical text is transmitted — only code pairs are sent for validation.
---

# Medical Billing Code Suggester

## Overview

This skill analyzes clinical documentation and suggests accurate ICD-10, CPT, and E&M codes — reducing coding errors, claim denials, and revenue leakage for medical practices.

**What it can do:**
- Suggest ICD-10-CM diagnosis codes from clinical notes or descriptions
- Suggest CPT procedure codes for documented services
- Determine correct E&M visit level (99202-99215)
- Validate code combinations for payer compliance
- Flag common denial triggers before submission
- Identify undercoding opportunities (lost revenue)
- Generate a coded superbill ready for billing

**Data sources:**
- **CMS ICD-10-CM** — official diagnosis code database (free, public domain)
- **CPT codes** — common procedure codes are referenced by number only; CPT is a proprietary code set owned by the AMA and requires a license for production use in claim submission. This skill does not include or distribute CPT code descriptions — it references codes by number and widely-known descriptions for educational/advisory purposes only.
- **CMS Fee Schedule** — RVU and reimbursement data (free, public domain)
- **CMS NCCI Edits** — National Correct Coding Initiative (free, public domain)

> ⚠️ **Disclaimer:** Code suggestions are AI-assisted and must be reviewed by a qualified medical coder or clinician before claim submission. Incorrect coding may constitute fraud.

> 🔒 **Privacy / PHI Warning:** Do not include patient-identifiable information (names, MRNs, DOBs, addresses) in any query. Submit de-identified clinical descriptions only (e.g. "58F with T2DM and HTN, diabetes follow-up"). If `CMS_API_KEY` is set, only billing code pairs are transmitted to the CMS API — no clinical text leaves your environment.

---

## Trigger Phrases

- "What ICD-10 code is this?" + description
- "Code this visit note"
- "What CPT code for [procedure]?"
- "Check my codes for this claim"
- "What E&M level is this visit?"
- "Generate a superbill for this visit"
- "Are these codes compatible?"
- "What's the reimbursement for CPT [code]?"
- "Find the ICD-10 for [diagnosis]"

---

## ICD-10 Code Lookup

### From plain language
```
"What's the ICD-10 for Type 2 diabetes with 
 diabetic neuropathy?"

"ICD-10 code for hypertensive heart disease 
 with heart failure"

"Code for acute appendicitis without peritonitis"
```

**Example output:**
```
ICD-10 CODE SUGGESTIONS

Query: "Type 2 diabetes with diabetic neuropathy"

Primary Code:
• E11.40 — Type 2 diabetes mellitus with 
  diabetic neuropathy, unspecified
  Confidence: 95%

More Specific Alternatives:
• E11.41 — T2DM with diabetic mononeuropathy
• E11.42 — T2DM with diabetic polyneuropathy ✓ 
  (most common for peripheral neuropathy)
• E11.43 — T2DM with diabetic autonomic neuropathy

Coding Tip: If polyneuropathy is documented, 
use E11.42 for higher specificity and fewer 
audit flags.

Additional codes to consider:
• Z79.4 — Long-term insulin use (if applicable)
```

### From a clinical note
```
"Code this note:
 Patient is a 58F with HTN, T2DM, and CKD stage 3.
 Here for diabetes follow-up. HbA1c improved.
 Refilling Metformin and Lisinopril."
```

**Example output:**
```
ICD-10 CODES — From Clinical Note

Primary Diagnosis:
• E11.65 — T2DM with hyperglycemia (if HbA1c 
  still elevated) OR
• E11.9  — T2DM without complications 
  (if at goal)

Secondary Diagnoses:
• I10    — Essential hypertension
• N18.3  — Chronic kidney disease, stage 3
• Z79.4  — Long-term use of oral hypoglycemic drugs

Sequencing Note: List the condition chiefly 
responsible for the visit first (T2DM for 
a diabetes follow-up).
```

---

## CPT Code Lookup

### Procedure coding
```
"What CPT code for an EKG with interpretation?"
"CPT for a 30-minute telehealth visit, established patient"
"Code for excision of a 1.5cm benign skin lesion on the back"
"What's the CPT for HbA1c lab test?"
```

**Example output:**
```
CPT CODE SUGGESTIONS

Query: "EKG with interpretation"

• 93000 — Electrocardiogram, routine ECG with 
  at least 12 leads; with interpretation and report
  
  2026 Medicare Rate: $20.18 (facility)
                      $26.45 (non-facility)
  
  Bundling Note: Do not bill 93000 separately 
  if it's already included in a global surgical 
  package or critical care code.
```

---

## E&M Visit Level Coding

This is where most practices lose money — undercoding out of caution or overcoding by mistake.

```
"What E&M level is this visit?
 New patient, 35 min face-to-face, 
 reviewed 3 chronic conditions, ordered 
 labs, updated medication list"

"Code this established patient visit:
 Follow-up HTN, reviewed BP logs, 
 adjusted Amlodipine dose, 5 minutes MDM"
```

**2021 E&M Guidelines (current standard):**

| Level | New Pt | Est. Pt | MDM | Time |
|-------|--------|---------|-----|------|
| 1 | 99202 | 99212 | Straightforward | 15-29 min |
| 2 | 99203 | 99213 | Low | 30-44 min |
| 3 | 99204 | 99214 | Moderate | 45-59 min |
| 4 | 99205 | 99215 | High | 60-74 min |

**Example output:**
```
E&M LEVEL ANALYSIS

Visit Type: Established Patient
Documentation reviewed:
✓ 3 chronic conditions addressed
✓ Prescription drug management
✓ Lab results reviewed
✓ Independent interpretation of tests

Medical Decision Making: MODERATE
→ Recommended Code: 99214

2026 Medicare Rate: $148.26
vs. 99213 (if undercoded): $93.12
Revenue difference: +$55.14 per visit

⚠️ Undercoding Risk: This visit qualifies 
for 99214 but is commonly billed as 99213. 
Ensure MDM is documented to support the 
higher level.
```

---

## Code Validation & Denial Prevention

```
"Check these codes before I submit:
 99214, E11.9, I10, Z79.4"

"Will these codes get denied?"
```

**What the agent checks:**
- NCCI bundling edits (procedures that can't be billed together)
- Diagnosis-procedure compatibility (does the dx support the CPT?)
- Modifier requirements (is a modifier needed?)
- Common payer-specific denial patterns

**Example output:**
```
CODE VALIDATION REPORT

Codes submitted: 99214, E11.9, I10, Z79.4

✅ NCCI Bundling: No conflicts detected
✅ Dx-Procedure Match: E11.9 supports 99214
✅ Modifier Check: None required

⚠️ WARNING:
• Z79.4 (long-term oral hypoglycemics) with 
  E11.9 — payers may query if patient is 
  actually on insulin vs oral meds. Verify 
  correct code (Z79.4 = oral, Z79.4 ≠ insulin).
  If on insulin, use Z79.4 AND note insulin use.

Denial Risk: LOW
Audit Risk: LOW
Estimated Reimbursement (Medicare): $148.26
```

---

## Superbill Generation

```
"Generate a superbill for today's visit:
 Established patient, T2DM and HTN follow-up,
 reviewed labs, adjusted medications,
 moderate MDM, 35 minutes"
```

**Example output:**
```
SUPERBILL — [Date]

Provider: [Provider Name]
Patient: [Patient Name]
DOB: [DOB]
Insurance: [Payer]

VISIT CODE:
99214 — Office Visit, Established, Moderate MDM

DIAGNOSIS CODES:
1. E11.65 — T2DM with hyperglycemia (Primary)
2. I10    — Essential hypertension
3. Z79.4  — Long-term oral hypoglycemic use

PROCEDURE CODES:
93000 — EKG with interpretation (if performed)
83036 — HbA1c (if ordered today)

MODIFIERS: None required

TOTAL ESTIMATED REIMBURSEMENT (Medicare):
99214:  $148.26
93000:  $26.45
83036:  $14.82
─────────────────
Total:  $189.53

Ready for billing review ✓
```

---

## Common ICD-10 Quick Reference

| Condition | ICD-10 Code |
|-----------|-------------|
| Type 2 Diabetes, uncomplicated | E11.9 |
| Type 2 Diabetes, with polyneuropathy | E11.42 |
| Essential Hypertension | I10 |
| Hyperlipidemia, unspecified | E78.5 |
| CKD Stage 3 | N18.3 |
| Obesity, BMI 30-34.9 | E66.09 |
| Major Depression, moderate | F32.1 |
| Low back pain | M54.50 |
| GERD | K21.0 |
| Hypothyroidism | E03.9 |
| Atrial fibrillation | I48.91 |
| CAD, native vessel | I25.10 |
| COPD, unspecified | J44.1 |
| Asthma, mild persistent | J45.30 |
| Anxiety disorder | F41.9 |

---

## Common CPT Quick Reference

| Service | CPT | 2026 Medicare Rate |
|---------|-----|--------------------|
| New patient, moderate | 99204 | $191.12 |
| Est. patient, moderate | 99214 | $148.26 |
| Telehealth, est. moderate | 99214-95 | $148.26 |
| Annual wellness visit | G0439 | $173.00 |
| EKG with interpretation | 93000 | $26.45 |
| HbA1c | 83036 | $14.82 |
| Lipid panel | 80061 | $21.97 |
| Urinalysis | 81003 | $4.62 |
| Pneumococcal vaccine | 90732 | $112.00 |
| Influenza vaccine | 90686 | $28.48 |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.3 | 2026-03-29 | Corrected CPT licensing statement; added PHI warning; clarified CMS_API_KEY endpoint and data transmission scope. |
| 1.0.0 | 2026-03-29 | Initial release. ICD-10 lookup, CPT coding, E&M level determination, code validation, superbill generation. |
