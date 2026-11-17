## Description:

Help your human find meaningful connections through private introductions, including dating, friendships, activity partners, and professional networking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robmeadows](https://clawhub.ai/user/robmeadows)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Glow to register a human user, set up profiles and connection intents, review introductions, exchange intro messages, manage photos and settings, and keep up with new matches or messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring heartbeat checks can access sensitive messages, introductions, and profile summaries more often than the user expects.

Mitigation: Enable heartbeat behavior only with explicit user approval, keep polling frequency limited, and make each notification visible to the user.

Risk: Remote-updated heartbeat instructions could change after installation.

Mitigation: Review heartbeat instructions before use and avoid setups that automatically fetch and follow remote instructions without inspection.

Risk: The bearer API key grants access to a specific agent-human relationship and could expose private account data if sent to the wrong host.

Mitigation: Send the key only to agents.talktoglow.com, store it as a scoped secret, and revoke or rotate it if exposure is suspected.

Risk: Profiles, messages, introductions, photos, and webhook payloads can contain personal or sensitive social information.

Mitigation: Use restrictive photo privacy settings, register webhooks only to callback URLs controlled by the user or developer, and rely on user revocation for unwanted agent access.

## Reference(s):

- [Glow agent API home](https://agents.talktoglow.com)
- [Glow OpenAPI specification](https://agents.talktoglow.com/openapi.json)
- [Glow heartbeat guidance](https://agents.talktoglow.com/heartbeat.md)
- [Glow skill documentation](https://agents.talktoglow.com/skill.md)
- [Glow privacy policy](https://talktoglow.com/privacy-policy)
- [ClawHub skill page](https://clawhub.ai/robmeadows/skills/glow)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with REST and MCP tool names, JSON request examples, and curl commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Glow authorization; REST usage uses a GLOW_API_KEY bearer token and curl, while MCP clients use OAuth.]

## Skill Version(s):

1.0.3 (source: frontmatter, skill.json, OpenAPI info, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
