## Description:

Generate, review, and publish social media content through MCP with AgentAuth and workspace token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tourmind](https://clawhub.ai/user/tourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel marketing teams and their agents use this skill to generate draft social media posts from HotelPost scenarios, review copy and images, and publish or schedule approved content to connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule real social media posts through connected accounts.

Mitigation: Require explicit user confirmation before every publish or schedule action, and verify the selected account and platform before calling publishing tools.

Risk: The skill depends on powerful HotelPost workspace and AgentAuth tokens configured in the agent environment.

Mitigation: Store hp_sk_* and uk_* values in a protected secret store when possible, limit each token to the intended workspace, and rotate tokens if exposure is suspected.

Risk: Image URLs returned by the MCP service may be downloaded and forwarded by the agent.

Mitigation: Confirm image URLs are expected, preserve full signed URL parameters, avoid forwarding unexpected assets blindly, and clean up temporary local image files after use.

## Reference(s):

- [User Onboarding](references/user-onboarding.md)
- [Error Handling](references/error-handling.md)
- [Conversation Examples](references/conversation-examples.md)
- [Feishu Platform Sending Guide](references/feishu-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/tourmind/skills/hotel-asset-marketer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls, configuration snippets, publishing status summaries, and optional shell commands for local image handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce social post drafts, platform-specific copy, image handling steps, scheduling instructions, and publishing status summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
