## Description:

Deploy an ad campaign management system with 4 agents that automate campaign strategy, creative production, real-time bidding, and performance analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a four-agent advertising workflow for campaign strategy, creative production, bid optimization, and performance analysis. It supports setup of role-specific Pilot Protocol hostnames, manifests, peer handshakes, and example campaign data flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs many dependent skills without pinned versions.

Mitigation: Use trusted, pinned versions of each dependent skill before installing this workflow.

Risk: The deployment prefix is used to form hostnames for campaign agents.

Mitigation: Validate the prefix as a simple hostname-safe value before using it in setup commands or manifests.

Risk: Peer handshakes establish trust between agents handling budget, creative, bid, and reporting data.

Mitigation: Manually verify peer identities before completing handshakes.

Risk: The analyst role can send campaign reports through Slack or webhook integrations.

Mitigation: Confirm exactly where reports will be sent before enabling the analyst role or external report flow.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-ad-campaign-manager-setup)
- [Publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific setup instructions for strategist, creative, bidder, and analyst agents.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
