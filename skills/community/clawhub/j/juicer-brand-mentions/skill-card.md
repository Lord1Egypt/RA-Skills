## Description:

Monitors social platforms for relevant brand mentions and sends a short digest to a chosen chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicer](https://clawhub.ai/user/juicer)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and communications teams use this skill to find relevant public mentions across social platforms. It filters unrelated name matches and can deliver a concise daily digest to a connected chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches consume Juicer credits, and daily automation can create recurring usage.

Mitigation: Check the account balance and tell the user the expected cost before running searches or enabling a daily schedule.

Risk: Search results may be sent to the selected chat, and the connected Juicer integration has account permissions.

Mitigation: Review the integration's account permissions and confirm the digest destination with the user.

## Reference(s):

- [Juicer MCP Server documentation](https://developers.juicer.io/mcp-server)
- [Juicer Developer Portal](https://www.juicer.io/developer)
- [ClawHub skill release](https://clawhub.ai/juicer/skills/juicer-brand-mentions)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [Plain-text mention digest with post links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters irrelevant and duplicate posts; reports date coverage and search credit use.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
