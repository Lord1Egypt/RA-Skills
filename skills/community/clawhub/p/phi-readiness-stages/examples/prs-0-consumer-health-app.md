# Example Assessment: PRS-0 Consumer Health App

## Scoped summary

- Workload: personal symptom tracker mobile app
- Environment: production consumer app
- Deployment boundary: vendor-hosted mobile backend and app experience chosen by the individual for personal use
- Framework version used: PRS Framework v1.1
- Assessment date: March 18, 2026
- Reviewer: example calibration case

## Applicability and role

- PHI/ePHI in scope: not shown in HIPAA scope for the reviewed workflow; health data may exist, but current evidence shows an individual-directed consumer app with no covered-entity or business-associate workflow demonstrated
- Likely HIPAA role: likely outside HIPAA scope for the reviewed workflow
- Caveats: this would need reassessment if the product begins operating on behalf of a covered entity, takes provider-directed data, or intentionally accepts regulated PHI in support channels

## Evidence reviewed

- E1 repo or design evidence: mobile app data model, privacy-facing product description, architecture note showing consumer sign-up and no provider integration
- E2 process or governance evidence: explicit product statement that the app is not offered on behalf of a covered entity
- E3 approval or contractual evidence: none shown
- E4 live operational evidence: none required for the current non-PHI stage decision
- Freshness assessment: current enough for a PRS-0 scope decision
- Missing evidence: covered-entity contract path, provider integration design, support-ingress controls
- Repo-only note: not repo-only; limited product and workflow documentation was reviewed
- Assessment evidence handling note: no raw PHI requested; scope decision supported with product descriptions and architecture notes only

## Official sources verified

- Source:
  - Title: Resources for mobile health apps developers
  - URL: https://www.hhs.gov/hipaa/for-professionals/special-topics/health-apps/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: Consumer health information and FTC/HIPAA statements
  - URL: https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-ftc-act/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: Who must comply with HIPAA privacy standards
  - URL: https://www.hhs.gov/hipaa/for-professionals/faq/190/who-must-comply-with-hipaa-privacy-standards/index.html
  - Type: official guidance
  - Access date: March 18, 2026

## Crosswalk and policy basis

- Crosswalk rows relied on: none required for the stage assignment because the main decision is HIPAA applicability and role, not satisfaction of Security Rule control domains
- Required versus addressable context: not material to this example
- PRS policy versus HIPAA baseline notes: none

## Current stage assignment

- Stage: PRS-0 Non-PHI - out of PHI scope
- Confidence: medium
- Why the stage is not lower: the workload, environment, and consumer-directed boundary are explicitly scoped and intentionally outside the reviewed HIPAA workflow
- Why the stage is not higher: no evidence supports a current PHI-bearing workflow or a future-state PRS-1 build program tied to PHI use

## Domain findings

- Domain:
  - Status: met
  - Evidence: explicit non-PHI scope statement and consumer-directed use case
  - Blockers: none for PRS-0

## Recommended actions

1. Action: add a PHI-ingress safeguard review for support tickets, uploads, and free-text fields
   - Why it matters: unintended PHI ingress can change the scope decision
   - Expected evidence artifact: ingress-boundary note or support-channel control record
   - Stage impact: improves confidence in PRS-0; may trigger PRS-1 reassessment if scope changes

## Caveats

- No legal determination.
- No certification claim.
- Scope limitations: this example assumes no provider-directed workflow, no covered-entity contract path, and no routine PHI intake in support or app flows.

## Regulatory boundary note

- Security Rule readiness scope: limited because the reviewed workflow is outside HIPAA scope as currently shown
- Privacy Rule follow-up needed: not for this scoped PRS decision
- Breach Notification follow-up needed: not for this scoped PRS decision
- State-law or other follow-up needed: likely yes for consumer health privacy and FTC/state consumer-protection review

## Safe public wording

- Public-safe statement: The reviewed personal symptom tracker mobile app in the assessed production consumer environment is currently PRS-0 Non-PHI - out of PHI scope for the reviewed deployment boundary.

## Calibration appendix

- Nearest example: consumer health app selected by the individual
- Why this case is not lower: the boundary is explicit rather than implied
- Why this case is not higher: no future-state PHI-readiness program is evidenced
- Disputed or judgment-heavy calls: consumer health data alone does not establish HIPAA scope
