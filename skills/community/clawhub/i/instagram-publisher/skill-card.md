## Description:

Publish posts to Instagram. Use when the user says 'post to Instagram', 'publish on IG', 'schedule Instagram post', 'create Instagram carousel', 'post a Reel', or wants to publish photos, carousels, or Reels to their Instagram Business account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to publish or schedule Instagram photos, carousels, and Reels through a connected Instagram Business or Creator account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded token that grants publish access to connected social media accounts.

Mitigation: Keep the connector URL private, treat it like a password, and revoke or regenerate it if exposed or no longer needed.

Risk: The skill can publish or schedule Instagram content through a third-party service.

Mitigation: Review media, captions, destination account, and scheduled time before confirming publication.

Risk: Using the skill requires trusting Boring with publishing access to the connected Instagram Business or Creator account.

Mitigation: Install only when that trust is acceptable for the account and workflow being connected.

## Reference(s):

- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring API documentation](https://boring-doc.aiagent-me.com)
- [Instagram Publisher on ClawHub](https://clawhub.ai/snoopyrain/skills/instagram-publisher)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Instagram publishing or scheduling confirmations, including post IDs and scheduled times.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
