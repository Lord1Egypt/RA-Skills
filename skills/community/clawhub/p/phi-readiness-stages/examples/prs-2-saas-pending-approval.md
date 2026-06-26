# Example Assessment: PRS-2 SaaS Pending Approval

## Scoped summary

- Workload: care coordination SaaS application
- Environment: production-ready hosted environment not yet approved for real PHI
- Deployment boundary: vendor-hosted application stack, managed database, support workflow, and vendor dependencies
- Framework version used: PRS Framework v1.1
- Assessment date: March 18, 2026
- Reviewer: example calibration case

## Applicability and role

- PHI/ePHI in scope: planned and technically supported, but not yet approved for live PHI in the reviewed environment
- Likely HIPAA role: likely business associate
- Caveats: approval and contract evidence are still incomplete

## Evidence reviewed

- E1 repo or design evidence: architecture diagrams, data-flow documentation, IAM, logging, encrypted storage, backup design
- E2 process or governance evidence: scoped risk analysis, remediation tracker, incident response procedure, contingency procedure, restore test, vendor review, workforce readiness plan
- E3 approval or contractual evidence: draft BAA and draft approval packet only
- E4 live operational evidence: pre-production operational checks only
- Freshness assessment: current enough for PRS-2
- Missing evidence: recorded approval decision, final contract path, live PHI operation evidence
- Repo-only note: no
- Assessment evidence handling note: evidence handled through internal document links and redacted screenshots; no raw PHI reviewed

## Official sources verified

- Source:
  - Title: 45 CFR Part 164 regulation text
  - URL: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C
  - Type: law
  - Access date: March 18, 2026
- Source:
  - Title: Risk analysis guidance
  - URL: https://www.hhs.gov/hipaa/for-professionals/security/guidance/guidance-risk-analysis/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: Business associates guidance
  - URL: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: NIST SP 800-66 Rev. 2
  - URL: https://csrc.nist.gov/pubs/sp/800/66/r2/final
  - Type: implementation guidance
  - Access date: March 18, 2026

## Crosswalk and policy basis

- Crosswalk rows relied on: risk analysis and remediation, security responsibility, access control, audit controls, security incident response, contingency and restore confidence, vendor management and BAA analysis, policies and documentation retention
- Required versus addressable context: the review documents addressable choices for automatic logoff and at-rest encryption through the risk analysis and architecture notes
- PRS policy versus HIPAA baseline notes: PRS requires a concrete restore-test record and a complete minimum artifact pack before calling the workload PHI-ready

## Current stage assignment

- Stage: PRS-2 PHI-Ready - pending internal approval
- Confidence: high
- Why the stage is not lower: required governance and technical artifacts for pre-approval PHI readiness are materially present
- Why the stage is not higher: no explicit approval decision or completed contractual path supports PRS-3

## Domain findings

- Domain:
  - Status: met
  - Evidence: scoped risk analysis, procedures, restore test, ownership matrix, vendor review
  - Blockers: none for PRS-2
- Domain:
  - Status: missing
  - Evidence: approval package is still draft and BAA is unsigned
  - Blockers: caps the workload below PRS-3

## Recommended actions

1. Action: obtain the explicit internal approval decision for PHI use in the reviewed environment
   - Why it matters: PRS-3 requires more than readiness; it requires actual approval
   - Expected evidence artifact: durable approval record with scope, approver, and date
   - Stage impact: unlocks PRS-3 review
2. Action: complete the required contract path with business associate and subprocessor coverage
   - Why it matters: the contractual assurance path is stage-critical before PHI approval
   - Expected evidence artifact: signed BAA set and current subprocessor record
   - Stage impact: unlocks PRS-3 review

## Caveats

- No legal determination.
- No certification claim.
- Scope limitations: pre-live and pre-approval state only.

## Regulatory boundary note

- Security Rule readiness scope: yes
- Privacy Rule follow-up needed: yes for use and disclosure workflows
- Breach Notification follow-up needed: yes before live operation
- State-law or other follow-up needed: possibly, depending on customer and state footprint

## Safe public wording

- Public-safe statement: The reviewed care coordination SaaS application in the assessed hosted environment is currently PRS-2 PHI-Ready - pending internal approval for the reviewed deployment boundary.

## Calibration appendix

- Nearest example: SaaS workload ready for PHI but still awaiting approval
- Why this case is not lower: the evidence pack is stronger than a repo-only or aspirational design review
- Why this case is not higher: explicit approval and final contract artifacts are still absent
- Disputed or judgment-heavy calls: draft approvals do not count as approval evidence
