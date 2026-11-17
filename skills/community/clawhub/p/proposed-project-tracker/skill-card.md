## Description:

Finds and ranks early-stage project, procurement-intent, and expiring-contract opportunities by industry or region, with suggested follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business-development teams use this skill to discover Chinese proposed projects, upcoming procurements, and expiring contracts, prioritize leads, and plan outreach before tenders open.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill stores an API credential in a local configuration file.

Mitigation: Use a pre-provisioned API key where possible; confirm the local credential location and remove the file when no longer needed.

Risk: Optional account registration sends device-derived information to the service.

Mitigation: Require informed consent before registration, or provide an existing API key to avoid device-data collection.

Risk: Shareable reports contain signed links that can grant access to opportunity details.

Mitigation: Do not publicly share reports unless signed links have been removed or that access is intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/proposed-project-tracker)
- [API tool reference](references/api-quick.md)
- [Opportunity scanning workflow](references/workflow.md)
- [Report format and export](references/report-template.md)
- [Account registration guidance](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML]

**Output Format:** [Ranked Markdown opportunity list and, for full scans, a shareable HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes opportunity links, ranking rationale, and recommended next steps; full scans consume service credits.]

## Skill Version(s):

1.0.8 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
