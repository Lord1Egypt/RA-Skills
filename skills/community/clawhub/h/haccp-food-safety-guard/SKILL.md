---
name: haccp-food-safety-guard
slug: haccp-food-safety-guard
version: 1.0.0
description: Audit food safety plans, HACCP records, and inspection reports against Codex HACCP principles and ISO 22000 before release. Flags nonconforming hazard analyses, CCP limits, and verification records with fix suggestions.
tags:
  - compliance
  - haccp
  - food-safety
  - iso22000
  - codex
  - guardrail
  - international
---

# HACCP Food Safety Guard

## When to Use

Activate when reviewing, generating, or publishing any of:
- HACCP plans / food safety plans
- Hazard analysis documents
- Critical Control Point (CCP) monitoring records
- Corrective action records
- Verification / validation records
- Food inspection or audit reports
- Marketing claims about food safety certification

## Core Rules

1. **All 7 HACCP principles must be present (Codex CXC 1-1969).** Missing any principle = nonconforming.
2. **Every CCP must have a validated critical limit (Principle 3).** No limit or unvalidated limit = critical.
3. **Monitoring procedures must be defined for each CCP (Principle 4).** Missing monitoring = critical.
4. **Corrective actions must be pre-defined for each CCP (Principle 5).** Missing corrective action = critical.
5. **Hazard analysis must cover biological, chemical, physical, and allergen hazards.** Omitting a hazard category = major.
6. **Verification and validation are distinct (Principle 6).** Confusing them or omitting verification = major.
7. **Documentation and records must be maintained (Principle 7).** Missing record-keeping procedure = major.

## The 7 HACCP Principles (Codex Alimentarius)

| # | Principle | Requirement |
|---|-----------|-------------|
| 1 | Hazard analysis | Identify hazards, assess significance, list control measures |
| 2 | Determine CCPs | Use CCP decision tree or equivalent logic |
| 3 | Establish critical limits | Measurable, validated limits for each CCP |
| 4 | Establish monitoring | What/how/frequency/who for each CCP |
| 5 | Establish corrective actions | Predefined actions when a deviation occurs |
| 6 | Establish verification | Confirm the HACCP system is working effectively |
| 7 | Establish documentation | Records of all procedures and principles |

## Common Nonconformities to Flag

| Issue | Principle Violated | Severity |
|-------|--------------------|----------|
| Hazard analysis missing allergen hazards | P1 | Major |
| CCP without a critical limit | P3 | Critical |
| Critical limit not validated | P3 | Critical |
| No monitoring frequency defined | P4 | Critical |
| No corrective action for a CCP | P5 | Critical |
| Verification confused with monitoring | P6 | Major |
| No record-keeping procedure | P7 | Major |
| Decision tree not used for CCP determination | P2 | Minor |
| "100% safe" / "zero risk" claims | Advertising rules | Minor |

## Terminology Corrections

| Nonconforming Term | Correct Term | Basis |
|--------------------|--------------|-------|
| "sterile" (without validation) | "commercially sterile" / "pathogen-free" | Codex |
| "safe" (absolute) | "safe when handled/prepared as directed" | Codex |
| "CCP" for a non-control step | "Control Point" or "PRP" | ISO 22000 |
| "quality control point" as CCP | Distinguish quality from safety CCP | HACCP |

## Output Format

```
【HACCP / Food Safety Compliance Review】

Document type: xxx
Review date: xxx
Standard: Codex CXC 1-1969 / ISO 22000

✅ Conformant items: x
⚠️ Observations: x (recommend improvement, not blocking)
❌ Nonconformities: x (must be corrected before release)

--- Nonconformities ---
[1] Issue description
  → Principle/clause violated: xxx
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

For detailed Codex guidance and ISO 22000 clause mapping, see `references/haccp-codex.md`.
