---
name: iso17025-report-guard
slug: iso17025-report-guard
version: 1.0.0
description: Validate test reports and calibration certificates against ISO/IEC 17025:2017 Clause 7.8 content requirements. Checks mandatory fields, uncertainty statements, conformity rules, and amendment handling before release.
tags:
  - compliance
  - iso17025
  - test-report
  - calibration-certificate
  - guardrail
  - international
---

# ISO/IEC 17025 Report Guard

## When to Use

Activate when reviewing, generating, or publishing any of:
- Test reports
- Calibration certificates
- Statements of conformity
- Sampling reports
- Amended / re-issued reports or certificates

## Core Rules

1. **Every report must contain all Clause 7.8.2 mandatory elements.** Missing any = nonconforming.
2. **Calibration certificates additionally require Clause 7.8.3 elements.** Missing any = nonconforming.
3. **Measurement uncertainty must be stated where required (7.8.2(l), 7.8.3).** Omission = critical.
4. **Statements of conformity must name the decision rule (7.8.6).** Missing decision rule = major.
5. **Opinions/interpretations must be clearly identified (7.8.5).** Unlabelled opinion = major.
6. **Amendments must follow 7.8.7 (re-issue or clearly marked supplement).** Improper amendment = major.
7. **Units must be SI or legally recognized.** Non-standard units without justification = minor.

## Mandatory Content Checklist (Clause 7.8.2)

Check each item. Mark ✅ / ❌. Any ❌ = nonconforming.

- [ ] Title: "Test Report" / "Calibration Certificate" / "Statement of Conformity"
- [ ] Laboratory name and address
- [ ] Unique report/certificate identification (number)
- [ ] Customer name and contact details
- [ ] Identification of the method used
- [ ] Description and unambiguous identification of the item
- [ ] Date of receipt of item AND date of performance
- [ ] Results, with units where applicable
- [ ] Name of person(s) authorizing the report
- [ ] Clear linkage of results to the specific item
- [ ] Statement of conformity (if applicable) with rules/standards
- [ ] Measurement uncertainty (where relevant to validity)

## Calibration Certificate Additions (Clause 7.8.3)

- [ ] Conditions (environmental) under which calibration was performed
- [ ] Measurement uncertainty of the result AND of the reference standard
- [ ] Metrological traceability statement
- [ ] Results before and after adjustment/repair (if applicable)
- [ ] Calibration interval or validity (if applicable / required)

## Amendment Rules (Clause 7.8.7)

When a report/certificate is changed after issue:
- Must be clearly identified as an amendment / re-issue
- Must reference the original report number
- A re-issued report gets a new unique identification
- "Amendment to report [original number], dated [date]"

## Common Nonconformities

| Issue | Clause | Severity |
|-------|--------|----------|
| Missing unique report ID | 7.8.2(c) | Critical |
| No measurement uncertainty | 7.8.2(l)/7.8.3 | Critical |
| No traceability statement (calibration) | 7.8.3 | Critical |
| Conformity statement without decision rule | 7.8.6 | Major |
| Unlabelled opinion | 7.8.5 | Major |
| Amendment without reference to original | 7.8.7 | Major |
| Missing date of performance | 7.8.2(g) | Major |
| Non-SI units without justification | 7.8 | Minor |

## Output Format

```
【ISO/IEC 17025 Report Content Review】

Document type: Test Report / Calibration Certificate
Report ID: xxx
Review date: xxx

Mandatory content (7.8.2): x/12 present
Calibration additions (7.8.3): x/5 present (if applicable)

✅ Conformant: x
⚠️ Observations: x
❌ Nonconformities: x

--- Nonconformities ---
[1] Missing/incorrect element
  → Clause: xxx
  → Correction: xxx

【Conclusion】: PASS / FAIL
```

## Usage

Run the mandatory content checklist first, then the clause-specific rules. Block release on any critical nonconformity. For full clause text, see `references/clause-7-8.md`.
