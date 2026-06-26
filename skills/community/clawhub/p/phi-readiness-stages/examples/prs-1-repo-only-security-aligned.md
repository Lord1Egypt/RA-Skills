# Example Assessment: PRS-1 Repo-Only Security-Aligned Workload

## Scoped summary

- Workload: internal scheduling API under active development
- Environment: development and staging only
- Deployment boundary: repository, infrastructure-as-code, and design artifacts; no approval or live PHI operation shown
- Framework version used: PRS Framework v1.1
- Assessment date: March 18, 2026
- Reviewer: example calibration case

## Applicability and role

- PHI/ePHI in scope: planned later; not approved or shown live now
- Likely HIPAA role: unclear from available evidence; likely business associate if later deployed on behalf of covered entities
- Caveats: customer model and contract path are not shown, so role remains provisional

## Evidence reviewed

- E1 repo or design evidence: service architecture, IaC, access-control configuration, secrets-manager integration, TLS enforcement, logging configuration
- E2 process or governance evidence: lightweight issue tracker notes only
- E3 approval or contractual evidence: none shown
- E4 live operational evidence: none shown
- Freshness assessment: technical evidence is current; governance evidence is thin
- Missing evidence: risk analysis, procedures, approval path, vendor review, live ops records
- Repo-only note: yes
- Assessment evidence handling note: repo-only review; no PHI-bearing evidence requested

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
  - Title: Addressable versus required implementation specifications FAQ
  - URL: https://www.hhs.gov/hipaa/for-professionals/faq/2020/what-is-the-difference-between-addressable-and-required-implementation-specifications/index.html
  - Type: official guidance
  - Access date: March 18, 2026

## Crosswalk and policy basis

- Crosswalk rows relied on: access control, audit controls, transmission security, encryption and secrets handling
- Required versus addressable context: automatic logoff and some encryption specifications are addressable, but the repo still must show a documented reasonable-and-appropriate path when PHI use is pursued
- PRS policy versus HIPAA baseline notes: PRS treats encryption in transit and clear secrets handling as baseline expectations for PRS-1 even before formal approval exists

## Current stage assignment

- Stage: PRS-1 Security-Aligned - not approved for PHI
- Confidence: high
- Why the stage is not lower: the workload shows real technical alignment for future PHI use instead of a generic prototype
- Why the stage is not higher: repo-only evidence cannot justify PRS-2 because non-code governance artifacts are missing

## Domain findings

- Domain:
  - Status: met
  - Evidence: access controls, secrets management, logging path, deployment separation, encrypted transport configuration
  - Blockers: none for PRS-1
- Domain:
  - Status: missing
  - Evidence: no scoped risk analysis or approved procedures
  - Blockers: caps the workload below PRS-2

## Recommended actions

1. Action: complete a scoped risk analysis and remediation tracker
   - Why it matters: PRS-2 requires non-code governance evidence tied to the actual workload
   - Expected evidence artifact: risk analysis document and tracked remediation plan
   - Stage impact: unlocks PRS-2 review
2. Action: document incident, contingency, and vendor-review procedures for the target environment
   - Why it matters: technical alignment alone cannot support PHI readiness
   - Expected evidence artifact: procedure package or approved applicability record
   - Stage impact: unlocks PRS-2 review

## Caveats

- No legal determination.
- No certification claim.
- Scope limitations: repository and design evidence only; no contractual, approval, or live operational evidence reviewed.

## Regulatory boundary note

- Security Rule readiness scope: limited to future-state workload readiness
- Privacy Rule follow-up needed: yes if future workflow will use or disclose PHI
- Breach Notification follow-up needed: not for the current pre-live state
- State-law or other follow-up needed: possibly, depending on data types and customer model

## Safe public wording

- Public-safe statement: The reviewed internal scheduling API in the assessed development and staging boundary is currently PRS-1 Security-Aligned - not approved for PHI for the reviewed deployment boundary.

## Calibration appendix

- Nearest example: repo-only system being built for later PHI use
- Why this case is not lower: technical safeguards are materially implemented rather than merely planned
- Why this case is not higher: no E2, E3, or E4 evidence supports higher stages
- Disputed or judgment-heavy calls: strong IaC can look mature, but PRS still caps repo-only reviews
