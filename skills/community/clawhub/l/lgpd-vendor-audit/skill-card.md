## Description:

Classify third-party privacy roles (operator, independent controller, joint controller) and conduct due diligence under LGPD Arts. 39 and 42.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy reviewers use this skill when onboarding or reviewing external SDKs, APIs, cloud, payment, and analytics providers. It inventories integrations, classifies each provider's privacy role and risk tier, and prepares due diligence assessments and remediation items.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: Some referenced project files or report locations may be missing or differ from the current workspace, leaving parts of the vendor review unsupported.

Mitigation: Confirm referenced paths exist in the project and review the relevant files before relying on an assessment.

Risk: Vendor role and risk-tier assessments can be incomplete if the project inventory, data flows, or provider terms are incomplete.

Mitigation: Check each assessment against the actual integrations, data handled, contracts, and provider documentation, and track unresolved evidence in .lgpd/gaps.md.

## Reference(s):

- [Vendor due diligence checklist](assets/vendor-checklist.md)
- [GitHub source repository (server-resolved provenance)](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-vendor-audit)
- [ClawHub skill release](https://clawhub.ai/goul4rt/skills/lgpd-vendor-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown vendor assessments and remediation items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-provider role and risk-tier assessments in .lgpd/vendors/, with remediation items tracked in .lgpd/gaps.md.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
