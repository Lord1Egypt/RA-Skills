## Description:

Generate and edit images using Cloudflare Workers AI via the `imageflare` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallytion](https://clawhub.ai/user/sallytion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate new images, edit existing images, and configure Cloudflare Workers AI image model settings through the `imageflare` CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external PyPI CLI that handles a Cloudflare API token.

Mitigation: Review or pin the `imageflare` package before installation, use the interactive config flow, and use a narrowly scoped Cloudflare Workers AI token.

Risk: Cloudflare account credentials may be exposed if tokens are pasted into shared commands or transcripts.

Mitigation: Avoid putting real tokens in command lines or shared logs; configure credentials interactively and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sallytion/skills/imageflare)
- [Cloudflare Workers AI Documentation](https://developers.cloudflare.com/workers-ai/)
- [ImageFlare Homepage](https://github.com/Sallytion/Imageflare)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to produce PNG image files through the external `imageflare` CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
