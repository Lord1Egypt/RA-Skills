## Description:

Fetch MarsBit news and flash data through the hosted MCP route in marsbit-co for latest news, channel lookup, keyword search, detail, related news, and flash updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domilin](https://clawhub.ai/user/domilin)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to let an agent retrieve MarsBit blockchain news, flash updates, channels, keyword search results, article details, and related news from the hosted MarsBit MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and item IDs are sent to the hosted MarsBit MCP endpoint.

Mitigation: Avoid putting secrets or sensitive personal information in MarsBit news or flash queries.

Risk: Manual GitHub fallback installation can copy unverified source into a local skills directory.

Mitigation: Prefer the ClawHub install path; if using the GitHub fallback, review repository contents and pin or verify the exact version before copying files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/domilin/skills/marsbit-news-skill)
- [MarsBit MCP Endpoint](https://www.marsbit.co/api/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-derived news responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl to call a hosted MCP endpoint; returned MCP text is expected to contain JSON that the agent parses before answering.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
