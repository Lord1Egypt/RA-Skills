## Description:

Use for Nager.Date Community API v4 public-holiday integration, country or holiday lookups, commercial-use eligibility checks, and direct read-only SDK or CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Nager.Date Community API v4 through Pontx discovery, SDK, and CLI workflows for public-holiday lookup and holiday-aware automation. It also guides users to check commercial-use eligibility before production or user-facing use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commercial use may require active provider sponsorship.

Mitigation: Confirm sponsorship or other provider entitlement before production reads, redistribution, or user-facing calendar features.

Risk: External CLI, SDK, and live API discovery can introduce unexpected commands, package behavior, or upstream availability issues.

Mitigation: Review package and CLI commands before running them, preview read-only requests with dry-run workflows, keep requests narrow, and surface upstream availability separately from application logic.

Risk: Holiday data can be misused if cached, redistributed, or filled in beyond provider terms and documented responses.

Mitigation: Cache only where provider terms and application policy permit, keep upstream responses in the caller's application, and treat empty successful responses as documented outcomes rather than inventing data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-nager-date)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and package names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only API integration guidance; official v4 contract does not require credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
