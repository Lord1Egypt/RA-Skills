## Description:

Query uptime monitors, heartbeat monitors, manage sites, retrieve incidents, create monitors, and fetch SLA reports from your PingHarbor account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[captain-cole](https://clawhub.ai/user/captain-cole)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to inspect PingHarbor uptime and heartbeat monitoring data, retrieve incident and SLA information, and create monitors or sites from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a PingHarbor API key to access the user's monitoring account.

Mitigation: Install only when the publisher and PingHarbor account access are trusted, and provide the key through the documented PINGHARBOR_API_KEY environment variable.

Risk: Create actions can persist monitors, heartbeat monitors, or sites in the PingHarbor account and may affect alerts or account usage.

Mitigation: Review create requests before execution and confirm monitor, heartbeat, site, and interval details before allowing the agent to proceed.

## Reference(s):

- [PingHarbor homepage](https://pingharbor.com)
- [PingHarbor MCP endpoint](https://api.pingharbor.com/functions/v1/mcp)
- [ClawHub skill page](https://clawhub.ai/captain-cole/skills/pingharbor)
- [Publisher profile](https://clawhub.ai/user/captain-cole)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown or plain text with optional shell commands, configuration snippets, and PingHarbor tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PINGHARBOR_API_KEY for authenticated PingHarbor account access.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
