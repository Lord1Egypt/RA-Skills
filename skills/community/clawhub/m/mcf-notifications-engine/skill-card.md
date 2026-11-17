## Description:

Multi-channel notification delivery with customizable templates, email and SMS sending, and full delivery logging - built for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cameron48](https://clawhub.ai/user/cameron48)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let AI agents send email and SMS notifications, manage reusable templates, and inspect delivery logs through a unified notification API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email and SMS notifications may contact recipients without proper consent or lawful basis.

Mitigation: Confirm consent or another lawful basis before sending notifications, especially for automated agent-driven outreach.

Risk: Notification messages and delivery logs may contain sensitive, regulated, or operationally confidential information.

Mitigation: Avoid sending secrets or regulated data unless the provider contract supports it, and review how logs are retained, protected, and deleted.

Risk: Paid x402 requests may create unexpected costs if an agent sends notifications or queries logs repeatedly.

Mitigation: Set agent-side limits and review the quoted price in 402 responses before allowing automated requests.

## Reference(s):

- [Notifications Engine ClawHub listing](https://clawhub.ai/cameron48/skills/mcf-notifications-engine)
- [MCF Agentic notification gateway](https://gateway.mcfagentic.com)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Text]

**Output Format:** [Markdown guidance with API endpoint details and notification workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve paid x402 requests in USDC on Base L2 and delivery logs containing notification metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
