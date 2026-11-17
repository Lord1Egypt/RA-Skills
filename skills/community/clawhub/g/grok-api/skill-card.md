## Description:

Calls Grok-compatible APIs through the LeonAI proxy for chat, reasoning, image generation, image editing, and video generation using OpenAI-compatible request patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lygjoey](https://clawhub.ai/user/lygjoey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route explicit Grok requests through a LeonAI proxy for text chat, reasoning, image generation or editing, video generation, and model listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API credentials are sent to the LeonAI proxy rather than directly to xAI.

Mitigation: Install only when the proxy and its data handling are trusted, avoid secrets or regulated data in prompts, and use explicit Grok commands to prevent unintended external calls.

Risk: The artifact includes an example that can enable NSFW image generation.

Mitigation: Review and disable or avoid the NSFW option unless it is appropriate for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lygjoey/skills/grok-api)
- [Publisher profile](https://clawhub.ai/user/lygjoey)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated media URLs, JSON API responses, model lists, and token usage summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
