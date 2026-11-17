## Description:

Generate QR code images from text or URLs and decode QR codes from public image URLs without configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create QR code image URLs from supplied text or URLs and decode QR codes from publicly accessible images through the Pipeworx-hosted MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR payload text, URLs, and public image URLs are sent to a Pipeworx-hosted QR service.

Mitigation: Do not use the skill for secrets, private links, sensitive QR contents, or sensitive image URLs unless the service's handling of that data has been reviewed and accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-qrcode)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples; tool results return image URLs or decoded text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [QR generation supports image sizes from 10px to 1000px; QR decoding requires a publicly accessible image URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
