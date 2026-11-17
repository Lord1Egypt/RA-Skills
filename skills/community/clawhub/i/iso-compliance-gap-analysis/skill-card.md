## Description:

Perform ISO compliance gap analysis for ISO 27001, ISO 27701, and ISO 42001 standards for certification readiness, security compliance gaps, privacy management gaps, AI management compliance, and multi-standard audit preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security, privacy, AI governance, and compliance teams use this skill to collect ISO readiness details and receive standard-by-standard compliance scores, gaps, strengths, and prioritized remediation recommendations. It is intended for ISO 27001, ISO 27701, ISO 42001, and multi-standard audit preparation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ISO readiness details, control gaps, privacy-process status, and related evidence to ToolWeb for remote processing.

Mitigation: Use the skill only when organizational approval exists for sharing this information with ToolWeb, and avoid entering regulated or confidential details unless approved.

Risk: API use depends on a ToolWeb key and may consume quota or incur billing.

Mitigation: Use a scoped API key with quota limits and monitor usage before running repeated assessments.

Risk: The available evidence does not describe ToolWeb retention, minimization, or data-handling terms for submitted assessment data.

Mitigation: Confirm the provider's retention and privacy terms before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/iso-compliance-gap-analysis)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with compliance scores, per-standard findings, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls send assessment details to ToolWeb for remote processing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
