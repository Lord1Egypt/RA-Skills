## Description:

Helps a text-only agent analyze, describe, extract, or OCR image content by sending a user-supplied image and prompt to a configured multimodal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzfly256](https://clawhub.ai/user/zzfly256)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a text-only model needs to answer questions about images through a bring-your-own-key multimodal provider. It supports local image files and image URLs with Anthropic-compatible or OpenAI-compatible APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, image URLs, prompts, optional system prompts, and API credentials are sent to the configured multimodal provider.

Mitigation: Use only providers and HTTPS endpoints approved for the data being processed, and avoid sensitive images unless that provider is approved.

Risk: The skill can fetch arbitrary image URLs from the user's machine when URL input is used with base64 transfer.

Mitigation: Avoid arbitrary or private-network image URLs until URL validation and download limits are added.

Risk: API keys may be stored directly in the local configuration file.

Mitigation: Prefer environment variable references for credentials and restrict any local config file permissions.

## Reference(s):

- [Configuration Schema Reference](references/config-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/zzfly256/skills/multimodal-image-understanding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script prints the upstream model reply to stdout and emits JSON-formatted errors to stderr.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
