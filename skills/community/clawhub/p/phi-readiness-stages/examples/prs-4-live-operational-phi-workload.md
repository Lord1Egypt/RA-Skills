# Example Assessment: PRS-4 Live Operational PHI Workload

## Scoped summary

- Workload: live care management platform
- Environment: production
- Deployment boundary: vendor-hosted application, managed cloud services, support function, and current PHI-bearing workflows in defined scope
- Framework version used: PRS Framework v1.1
- Assessment date: March 18, 2026
- Reviewer: example calibration case

## Applicability and role

- PHI/ePHI in scope: yes, live in the reviewed production boundary
- Likely HIPAA role: likely business associate
- Caveats: assessment remains scoped to the named workload and production environment only

## Evidence reviewed

- E1 repo or design evidence: architecture, IAM, logging, encrypted storage, data flows, infrastructure controls
- E2 process or governance evidence: current risk analysis, procedures, incident and contingency materials, vendor reassessment, workforce controls
- E3 approval or contractual evidence: signed BAA set, approval decision, defined scope, support ownership, go-live records
- E4 live operational evidence: recent access reviews, recent alert or monitoring review, recent vulnerability and patch records, current change-control evidence, restore confidence evidence, periodic evaluation
- Freshness assessment: current enough to support PRS-4
- Missing evidence: no blocker-level gaps identified in the assessed scope
- Repo-only note: no
- Assessment evidence handling note: PHI-bearing evidence was reviewed via approved internal records and redacted excerpts; the report stores pointers rather than duplicating raw records

## Official sources verified

- Source:
  - Title: 45 CFR Part 164 regulation text
  - URL: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C
  - Type: law
  - Access date: March 18, 2026
- Source:
  - Title: Security Rule safeguards and standards
  - URL: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: Risk analysis guidance
  - URL: https://www.hhs.gov/hipaa/for-professionals/security/guidance/guidance-risk-analysis/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: Addressable versus required implementation specifications FAQ
  - URL: https://www.hhs.gov/hipaa/for-professionals/faq/2020/what-is-the-difference-between-addressable-and-required-implementation-specifications/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: NIST SP 800-66 Rev. 2
  - URL: https://csrc.nist.gov/pubs/sp/800/66/r2/final
  - Type: implementation guidance
  - Access date: March 18, 2026

## Crosswalk and policy basis

- Crosswalk rows relied on: risk analysis and remediation, access control, audit controls, incident response, contingency and restore confidence, periodic evaluation, vendor management and BAA analysis, policies and documentation retention
- Required versus addressable context: addressable choices for session management, integrity mechanisms, and encryption are documented with workload-specific rationale and implemented controls
- PRS policy versus HIPAA baseline notes: PRS requires current operational proof rather than relying only on policy or approval artifacts

## Current stage assignment

- Stage: PRS-4 PHI-Operational - operating with PHI under ongoing controls
- Confidence: high
- Why the stage is not lower: the workload has current operational evidence, complete approval and contract coverage, and live PHI within the assessed boundary
- Why the stage is not higher: PRS-4 is the highest defined stage

## Domain findings

- Domain:
  - Status: met
  - Evidence: current operational control records across required live domains
  - Blockers: none

## Recommended actions

1. Action: maintain periodic reassessment and evidence retention discipline
   - Why it matters: PRS-4 can be lost if evidence becomes stale or architecture changes invalidate prior conclusions
   - Expected evidence artifact: next evaluation record and refreshed evidence index
   - Stage impact: preserves PRS-4

## Caveats

- No legal determination.
- No certification claim.
- Scope limitations: applies only to the reviewed production workload, environment, and deployment boundary.

## Regulatory boundary note

- Security Rule readiness scope: yes
- Privacy Rule follow-up needed: still may be relevant depending on workflow and customer obligations
- Breach Notification follow-up needed: yes as part of ongoing live operation governance
- State-law or other follow-up needed: may still apply depending on jurisdiction and data classes

## Safe public wording

- Public-safe statement: The reviewed live care management platform in the assessed production environment is currently PRS-4 PHI-Operational - operating with PHI under ongoing controls for the reviewed deployment boundary.

## Calibration appendix

- Nearest example: live PHI workload with current recurring evidence
- Why this case is not lower: the evidence set is live, current, and durable rather than aspirational
- Why this case is not higher: not applicable
- Disputed or judgment-heavy calls: high maturity in one environment does not automatically transfer to another boundary
