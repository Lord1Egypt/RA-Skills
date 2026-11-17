## Description:

Perform comprehensive IT risk assessments across infrastructure, data protection, access control, compliance, incident response, and vendor management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners, IT teams, and compliance stakeholders use this skill to collect IT control maturity inputs, call ToolWeb's assessment API, and receive an overall risk score, domain breakdown, critical gaps, and prioritized remediation roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends detailed IT security posture answers to ToolWeb's external API, which may include confidential company security details.

Mitigation: Use the skill only after confirming organizational approval to send the assessment data to ToolWeb and reviewing the provider's retention and handling practices.

Risk: Successful API calls may have billing implications for the configured ToolWeb account.

Mitigation: Confirm the intended ToolWeb subscription and API-key usage before running assessments.

Risk: The artifact requires an external API call and does not include a consent checkpoint before transmission.

Mitigation: Add an explicit user confirmation step before submitting assessment inputs, especially when handling sensitive security posture information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/it-risk-assessment-tool)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with risk scores, domain breakdown, critical gaps, and remediation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and TOOLWEB_API_KEY; successful API calls may be billed by ToolWeb.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
