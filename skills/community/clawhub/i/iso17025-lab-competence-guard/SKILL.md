---
name: iso17025-lab-competence-guard
slug: iso17025-lab-competence-guard
version: 1.0.0
description: Audit test/calibration lab documents against ISO/IEC 17025:2017 before release. Flags nonconforming reports, certificates, and quality records with clause-level citations and fix suggestions.
tags:
  - compliance
  - iso17025
  - laboratory
  - accreditation
  - guardrail
  - international
---

# ISO/IEC 17025 Lab Competence Guard

## When to Use

Activate when reviewing, generating, or publishing any of:
- Test reports / calibration certificates
- Laboratory quality manual or procedure documents
- Method validation / verification records
- Equipment calibration or maintenance records
- Proficiency testing / interlaboratory comparison records
- Internal audit or management review reports
- Marketing claims about accredited capabilities

## Core Rules

1. **Every report/certificate must satisfy Clause 7.8 minimum content.** Missing any mandatory element = nonconforming.
2. **Traceability is non-negotiable (Clause 6.5).** Results must be traceable to SI units or agreed reference standards. Broken chain = critical.
3. **Personnel competence must be demonstrable (Clause 6.2).** Authorization records required for each activity.
4. **Equipment must be fit for purpose (Clause 6.4).** Calibration status, confirmation intervals, and records required.
5. **Opinions and interpretations must be clearly identified (Clause 7.8.5).** Unlabelled opinion in a report = nonconforming.
6. **Amendments follow Clause 7.8.7.** Post-issue changes require a new document or clearly marked supplement.
7. **Impartiality and confidentiality (Clauses 4.1, 4.2).** Any conflict-of-interest or data-disclosure risk = critical.

## Mandatory Report Content (Clause 7.8.2)

Each test report / calibration certificate must contain ALL of the following. Missing any one = nonconforming:

| # | Required Element | Clause |
|---|------------------|--------|
| 1 | Title ("Test Report" / "Calibration Certificate") | 7.8.2(a) |
| 2 | Laboratory name and address | 7.8.2(b) |
| 3 | Unique identification of the report/certificate | 7.8.2(c) |
| 4 | Customer name and contact | 7.8.2(d) |
| 5 | Identification of the method used | 7.8.2(e) |
| 6 | Description and identification of the item tested/calibrated | 7.8.2(f) |
| 7 | Date of receipt of item and date of performance | 7.8.2(g) |
| 8 | Results, with units where applicable | 7.8.2(h) |
| 9 | Name of person(s) authorizing the report | 7.8.2(i) |
| 10 | Clear identification of which results relate to the item | 7.8.2(j) |
| 11 | Statement of conformity (if applicable), with rules/standards | 7.8.2(k) |
| 12 | Measurement uncertainty (where relevant) | 7.8.2(l) |

## Calibration-Specific Requirements (Clause 7.8.3)

Calibration certificates additionally require:
- Conditions under which calibrations were performed
- Measurement uncertainty of the result AND the reference standard
- Traceability statement
- Results before and after adjustment/repair (if applicable)
- Calibration interval recommendation (if applicable)

## Common Nonconformities to Flag

| Issue | Clause Violated | Severity |
|-------|-----------------|----------|
| Missing measurement uncertainty | 7.8.2(l), 7.8.3 | Critical |
| No traceability statement | 6.5 | Critical |
| Unlabelled opinion/interpretation | 7.8.5 | Major |
| Report signed by unauthorized person | 6.2, 7.8.2(i) | Critical |
| Equipment past calibration due date | 6.4.4 | Major |
| Method not validated for intended use | 7.2.2 | Major |
| Amendment without proper re-issue | 7.8.7 | Major |
| Absolute claims ("most accurate", "100% precise") | 7.8, advertising rules | Minor |
| Confidential data exposed | 4.2 | Critical |

## Terminology Corrections

| Nonconforming Term | Correct Term | Basis |
|--------------------|--------------|-------|
| "accuracy" (as a number) | "measurement uncertainty" or "trueness + precision" | VIM / ISO 5725 |
| "error = 0" | Report actual uncertainty | 7.8.2(l) |
| "permanently valid" | State specific validity/interval | 7.8.3 |
| "certified" (without basis) | "accredited" (only if accredited) | ISO 17011 |
| "best in class" | Remove or substantiate | Advertising |

## Output Format

```
【ISO/IEC 17025 Compliance Review】

Document type: xxx
Review date: xxx
Standard: ISO/IEC 17025:2017

✅ Conformant items: x
⚠️ Observations: x (recommend improvement, not blocking)
❌ Nonconformities: x (must be corrected before release)

--- Nonconformities ---
[1] Issue description
  → Clause violated: xxx
  → Suggested correction: xxx

--- Observations ---
[1] Issue description
  → Recommendation: xxx

【Conclusion】: PASS / FAIL (correct and re-review)
```

## Usage

When the user submits a document for review, check it item-by-item against the rules above and produce the structured report.

- **Critical nonconformities (❌)** must block release.
- **Observations (⚠️)** get suggestions but do not block.

For detailed clause text and edge cases, see `references/iso17025-clauses.md`.
