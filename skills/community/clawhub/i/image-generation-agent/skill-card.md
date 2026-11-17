## Description:

Image Generation Agent provides AgentPMT-hosted remote tool calls for generating or editing images from prompts and optional reference images using Google Gemini image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, marketers, e-commerce sellers, content creators, and agents use this skill to create draft or final image assets from text prompts, or to edit images with up to four reference photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images are sent to AgentPMT's hosted service.

Mitigation: Avoid sensitive or regulated images unless organizational policy approves that use.

Risk: Generated outputs are exposed through signed download URLs.

Mitigation: Use the shortest practical expiration period and handle URLs as shareable access tokens until they expire.

Risk: Companion setup examples may use mutable package installation commands.

Mitigation: Prefer pinned or reviewed install paths for companion skills before using them in production workflows.

## Reference(s):

- [Image Generation Agent schema](artifact/schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/image-generation-agent)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/image-generation-agent)
- [AgentPMT publisher profile](https://clawhub.ai/user/agentpmt)

## Skill Output:

**Output Type(s):** [guidance, API Calls, Files, JSON]

**Output Format:** [Markdown guidance with JSON request and response examples; successful tool calls return JSON metadata and signed image download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image bytes are saved to AgentPMT File Manager rather than returned inline; signed URLs expire after the configured retention period.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
