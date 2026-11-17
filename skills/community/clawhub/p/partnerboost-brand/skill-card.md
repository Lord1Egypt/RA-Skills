## Description:

Call PartnerBoost merchant APIs to manage transactions, performance, billing, partners and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[partnerboost-tech-team](https://clawhub.ai/user/partnerboost-tech-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and merchants use this skill to issue PartnerBoost API calls and summarize merchant-side transaction, performance, billing, account, and partner data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PartnerBoost API keys could be exposed through chat logs, shell history, or copied command output.

Mitigation: Provide PARTNERBOOST_API_KEY through the agent runtime's secret or environment mechanism, avoid pasting keys into prompts, and redact command output before sharing.

Risk: Agent-proposed API calls may retrieve or send sensitive merchant, transaction, billing, or account data.

Mitigation: Review each generated API request before execution and use a least-privileged PartnerBoost API key scoped to the intended merchant workflow.

Risk: Installation from an unintended source can introduce unreviewed skill instructions.

Mitigation: Install only from the intended ClawHub publisher or verified repository source and prefer pinned or verified Skills CLI versions.

## Reference(s):

- [PartnerBoost Brand on ClawHub](https://clawhub.ai/partnerboost-tech-team/skills/partnerboost-brand)
- [Publisher profile](https://clawhub.ai/user/partnerboost-tech-team)
- [PartnerBoost Merchant API skill documentation](artifact/SKILL.md)
- [PartnerBoost API base URL](https://app.partnerboost.com)
- [OpenClaw Skills config](https://docs.openclaw.ai/tools/skills-config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PARTNERBOOST_API_KEY for authenticated PartnerBoost API requests.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
