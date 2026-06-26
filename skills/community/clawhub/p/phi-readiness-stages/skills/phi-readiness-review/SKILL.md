---
name: phi-readiness-review
description: Assess the current PHI Readiness Stage (PRS) of a workload, repository, system, or environment; determine HIPAA applicability and role; identify evidence gaps; and recommend the next actions using the PRS framework, official HHS/OCR and NIST sources, and conservative evidence caps.
---

# PHI Readiness Review

Use this skill when the task is to assess a system's PRS stage, check PHI-readiness gaps, audit evidence for PHI use, or recommend the next steps to advance a workload safely.

## Load order

Always read these first:

1. `framework/assessment-rules.md`
2. `framework/assessment-evidence-handling.md`
3. `framework/applicability-role-matrix.md`
4. `framework/stage-rubric.md`
5. `framework/evidence-levels.md`
6. `framework/evidence-freshness.md`
7. `framework/minimum-artifact-matrix.md`
8. `framework/regulatory-boundaries.md`
9. `framework/output-contract.md`

Then read only the references needed for the task:

- `skills/phi-readiness-review/references/triage.md` for HIPAA applicability and role
- `skills/phi-readiness-review/references/checklist.md` for the full review sequence
- `skills/phi-readiness-review/references/report-template.md` for the output layout
- `skills/phi-readiness-review/references/action-priority.md` for ordering recommendations
- `skills/phi-readiness-review/references/health-app-and-api-scenarios.md` for consumer health apps, provider-connected apps, patient-directed API access, customer-hosted products, or unintended PHI ingress
- `skills/phi-readiness-review/references/mobile-wearable-communications.md` for push notifications, outbound communications, local device storage, lock-screen exposure, wearables, or companion-device risks
- `mappings/hipaa-security-rule-crosswalk.md` when rule-level traceability, required-versus-addressable analysis, or `PRS policy` labeling is needed
- `examples/README.md` and the example assessments for calibration against common archetypes
- `controls/index.md` and specific control files for domain-level questions
- `controls/shared-responsibility.md` for cloud, SaaS, customer-hosted, or inherited-control reviews
- `controls/physical-safeguards.md` when facilities, devices, workstations, media handling, or retained physical responsibilities are in scope
- `references/source-registry.md` before making claims about current HIPAA rules

## Required workflow

1. Define the exact workload, environment, and deployment boundary under review.
2. Determine whether PHI or ePHI is in scope now, later, or explicitly excluded.
3. Determine the likely HIPAA role or say that it is unclear.
4. If the workflow involves health apps, provider APIs, customer-hosted software, or user-generated content, use `skills/phi-readiness-review/references/health-app-and-api-scenarios.md`.
5. If the workflow involves phones, tablets, wearables, email, SMS, push notifications, or offline device storage, use `skills/phi-readiness-review/references/mobile-wearable-communications.md`.
6. Apply `framework/assessment-evidence-handling.md` before requesting, copying, or quoting any evidence.
7. Inventory evidence and classify it using `framework/evidence-levels.md`.
8. Check evidence freshness using `framework/evidence-freshness.md`.
9. Verify that the minimum artifact set for the candidate stage exists using `framework/minimum-artifact-matrix.md`.
10. Verify current official sources live from `references/source-registry.md`.
11. Evaluate each required domain for the candidate stage using `framework/stage-rubric.md`.
12. Use `mappings/hipaa-security-rule-crosswalk.md` when the assessment needs rule-level traceability, required-versus-addressable reasoning, or a `PRS policy` note.
13. Use `controls/shared-responsibility.md` whenever controls are inherited or the deployment model changes the role analysis.
14. Use `controls/physical-safeguards.md` whenever physical controls are direct, partially inherited, or unclear.
15. When the case matches a common archetype, compare it to the nearest example in `examples/`.
16. Add a regulatory-boundary note using `framework/regulatory-boundaries.md`.
17. Apply conservative stage caps when evidence is missing, stale, indirect, or role-dependent.
18. Assign the highest defensible stage.
19. Recommend the next actions required to reach the next stage.
20. Return the assessment using `framework/output-contract.md`.

## Hard constraints

- Do not overrule the evidence cap with technical optimism.
- Do not infer approval, contracting, or live operations from code.
- Do not infer covered-entity, business-associate, or subcontractor status from branding alone.
- Do not treat a health-related app or device as automatically inside HIPAA scope just because it handles health data.
- Do not use proposed NPRM changes as current mandatory requirements unless asked for a forward-looking analysis.
- Do not use `HIPAA compliant`, `HIPAA certified`, or `HIPAA secure` as status labels.
- Do not place raw PHI into prompts, chat transcripts, tickets, or draft reports.
- If the review is repo-only, say so explicitly.
- If adjacent Privacy Rule, Breach Notification Rule, FTC, or state-law issues are implicated, flag them explicitly instead of silently folding them into the PRS stage.

## Escalation logic

- If the workload is clearly out of PHI scope, stop at PRS-0 unless the task explicitly asks for future-state readiness.
- If technical safeguards exist but governance evidence is missing, cap at PRS-1.
- If governance evidence exists but explicit approval is missing, cap at PRS-2.
- If approval exists but live PHI evidence is missing, cap at PRS-3.
- If live evidence is stale or controls appear lapsed, call for reassessment and possible downgrade.
