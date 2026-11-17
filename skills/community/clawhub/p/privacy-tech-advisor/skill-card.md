## Description:

Get AI-powered privacy technology recommendations with maturity assessment, capability roadmap, and tech stack advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Privacy, security, compliance, and procurement teams use this skill to assess privacy-program maturity, plan capability investments, and select privacy technology stacks for their organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization profile, revenue, compliance, and privacy-program details to a third-party hosted API.

Mitigation: Use it only when sharing those details with ToolWeb.in is acceptable, and avoid sending unnecessary confidential or regulated data.

Risk: Successful API calls are tracked for billing by the third-party service.

Mitigation: Confirm the configured API key, subscription, and expected usage before enabling the skill for routine workflows.

Risk: The skill has no local fallback if the third-party API fails.

Mitigation: Treat API errors as service failures and retry later rather than substituting unsupported local advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/privacy-tech-advisor)
- [ToolWeb API Portal](https://portal.toolweb.in)
- [Privacy Tech Advisor API Endpoint](https://portal.toolweb.in/apis/compliance/privacy-tech-advisor)
- [ToolWeb Platform](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with API-backed privacy maturity assessment, roadmap, tool recommendations, budget guidance, and executive summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls are tracked for billing by the third-party service.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
