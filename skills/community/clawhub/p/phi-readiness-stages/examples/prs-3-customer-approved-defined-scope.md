# Example Assessment: PRS-3 Customer-Approved Defined Scope

## Scoped summary

- Workload: customer-hosted analytics module for a covered-entity deployment
- Environment: customer production environment approved for defined PHI use
- Deployment boundary: customer-managed infrastructure with vendor-managed application updates and limited support access
- Framework version used: PRS Framework v1.1
- Assessment date: March 18, 2026
- Reviewer: example calibration case

## Applicability and role

- PHI/ePHI in scope: approved for live PHI in a defined customer deployment boundary
- Likely HIPAA role: likely business associate, with some controls inherited by the customer environment
- Caveats: live operational evidence for the current production instance is still limited

## Evidence reviewed

- E1 repo or design evidence: shared-responsibility matrix, deployment architecture, access paths, logging design
- E2 process or governance evidence: risk analysis, customer-hosted operating model, procedures, vendor reassessment record
- E3 approval or contractual evidence: signed BAA, written internal approval, customer go-live checklist, approved scope statement
- E4 live operational evidence: onboarding records and partial monitoring enablement only; current recurring operational evidence is limited
- Freshness assessment: approval evidence is current; live ops evidence is too thin for PRS-4
- Missing evidence: recent access-review evidence, recent monitoring review record, recent patch/change evidence, periodic evaluation record
- Repo-only note: no
- Assessment evidence handling note: approval and contract records referenced by durable location; no raw PHI copied into the report

## Official sources verified

- Source:
  - Title: 45 CFR Part 164 regulation text
  - URL: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C
  - Type: law
  - Access date: March 18, 2026
- Source:
  - Title: Business associates guidance
  - URL: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: Cloud computing guidance
  - URL: https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html
  - Type: official guidance
  - Access date: March 18, 2026
- Source:
  - Title: NIST SP 800-66 Rev. 2
  - URL: https://csrc.nist.gov/pubs/sp/800/66/r2/final
  - Type: implementation guidance
  - Access date: March 18, 2026

## Crosswalk and policy basis

- Crosswalk rows relied on: physical safeguards, vendor management and BAA analysis, access control, audit controls, contingency and restore confidence, periodic evaluation
- Required versus addressable context: several facility and device controls are inherited, but retained responsibilities are still explicitly named and evidenced
- PRS policy versus HIPAA baseline notes: PRS requires a real live-operational evidence set before PRS-4 even when approval and contracts are complete

## Current stage assignment

- Stage: PRS-3 PHI-Approved - internally approved for PHI use in defined scope
- Confidence: medium
- Why the stage is not lower: the workload has explicit approval, defined scope, and required contract coverage
- Why the stage is not higher: recurring live operational evidence is not yet strong enough to support PHI-operational status

## Domain findings

- Domain:
  - Status: met
  - Evidence: approval decision, BAA, defined scope, go-live checklist, support ownership record
  - Blockers: none for PRS-3
- Domain:
  - Status: partial
  - Evidence: some live monitoring exists but recurring current evidence is incomplete
  - Blockers: caps the workload below PRS-4

## Recommended actions

1. Action: collect current live operational records for access review, alert handling, patching, and change control
   - Why it matters: PRS-4 requires durable evidence that the workload is operating with PHI under ongoing controls
   - Expected evidence artifact: dated live ops evidence pack
   - Stage impact: unlocks PRS-4 review
2. Action: complete a periodic technical and nontechnical evaluation after initial live operation
   - Why it matters: evaluation becomes critical once PHI is live
   - Expected evidence artifact: periodic evaluation record
   - Stage impact: unlocks PRS-4 review

## Caveats

- No legal determination.
- No certification claim.
- Scope limitations: approved customer-hosted boundary only; do not generalize to other customer deployments without separate review.

## Regulatory boundary note

- Security Rule readiness scope: yes, within the approved deployment boundary
- Privacy Rule follow-up needed: yes where customer workflows drive uses and disclosures
- Breach Notification follow-up needed: yes for the live deployment
- State-law or other follow-up needed: possibly, depending on the customer's jurisdiction

## Safe public wording

- Public-safe statement: The reviewed customer-hosted analytics module in the assessed customer production boundary is currently PRS-3 PHI-Approved - internally approved for PHI use in defined scope for the reviewed deployment boundary.

## Calibration appendix

- Nearest example: approved PHI use with incomplete recurring live ops evidence
- Why this case is not lower: approval and contractual evidence are complete
- Why this case is not higher: the operational record is still too thin and too new
- Disputed or judgment-heavy calls: approval is not the same as operational maturity
