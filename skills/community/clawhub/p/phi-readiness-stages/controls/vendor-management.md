# Vendor Management

Last reviewed: March 17, 2026.

Primary authority pointers:

- HHS business associates guidance
- HHS cloud computing guidance
- HIPAA Security Rule administrative requirements relevant to vendors and inherited controls

Read this with `controls/shared-responsibility.md` when the workload relies on cloud, SaaS, or central platform controls.

## Why this domain matters

Most modern workloads rely on cloud or SaaS services. PRS needs evidence that the team understands which vendors are in scope, what is inherited, and what remains the workload owner's responsibility.

## Review questions

- Is there a current inventory of in-scope vendors and subprocessors?
- For each vendor, is the data role and PHI exposure understood?
- Are inherited controls and customer responsibilities documented?
- Are vendor reviews refreshed when architecture changes?

## Minimum expectations by stage

- PRS-1: vendor inventory started
- PRS-2: vendor and subprocessor review completed
- PRS-3: contractual prerequisites are complete where required
- PRS-4: vendor reassessment is active

## Strong evidence

- vendor inventory
- security review records
- shared-responsibility analysis
- reassessment records

## Common blockers

- `we are secure because we use AWS`
- no workload-level inheritance analysis
- no vendor review for key PHI-path providers

## Recommended next actions

- inventory vendors by PHI exposure and function
- document inherited versus retained controls
- schedule reassessment triggers for vendor or architecture changes
