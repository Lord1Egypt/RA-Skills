## Description:

Search GIFs, stickers, emojis, trending media, retrieve GIPHY media by ID, and upload GIF or video assets through the GIPHY API after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to find GIPHY GIFs, stickers, emoji media, channels, tags, and trending content, translate phrases into matching media, and upload confirmed media assets through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party ClawLink plugin that handles GIPHY credentials and persists in OpenClaw.

Mitigation: Review the ClawLink plugin and hosted credential service before installation, request a pinned plugin version and permission manifest, and confirm uninstall and credential revocation steps.

Risk: GIPHY uploads may publish media through the connected account and uploaded material may become searchable.

Mitigation: Require an upload preview and explicit user confirmation, and confirm rights to the media before upload.

## Reference(s):

- [GIPHY API Documentation](https://developers.giphy.com/docs/api/)
- [GIPHY Developers](https://developers.giphy.com/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=giphy-media)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GIPHY media search results, connection checks, upload previews, and error-handling guidance.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
