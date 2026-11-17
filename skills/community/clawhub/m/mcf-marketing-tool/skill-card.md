## Description:

Full marketing automation with prospects, campaigns, outreach tracking, solutions catalog, agent conversation logs, and cost tracking, built for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cameron48](https://clawhub.ai/user/cameron48)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to let AI agents manage marketing operations through API calls, including prospect research, campaign creation, outreach tracking, solution catalog management, conversation log access, and cost monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and research prospects and create marketing campaigns.

Mitigation: Configure explicit human approval before prospect creation, prospect research, or campaign creation.

Risk: The skill can incur paid x402 API requests.

Mitigation: Require human approval and spending controls for paid requests before installation or agent execution.

Risk: The skill can expose agent conversation logs and may process customer, prospect, confidential, or regulated data.

Mitigation: Avoid sending secrets or sensitive conversation content unless the provider's retention, access, and deletion practices are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cameron48/skills/mcf-marketing-tool)
- [MCF Agentic Gateway](https://gateway.mcfagentic.com)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown instructions with an HTTP endpoint table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires x402 payment in USDC on Base for API endpoint access.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
