## Description:

Use OOMOL's HTML to Image service to capture webpages or convert supplied HTML and CSS into images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the skill to capture a public webpage or turn supplied HTML and optional CSS into an image through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code.

Mitigation: Review installer contents and preinstall a verified CLI version.

Risk: The CLI's documented startup skill synchronization can affect other agent installations.

Mitigation: Check and control this synchronization before enabling the skill.

Risk: HTML and CSS submitted for rendering are processed by OOMOL and the rendering provider.

Mitigation: Send only HTML and CSS you intend those services to process.

## Reference(s):

- [HTML to Image](https://html2img.com)
- [HTML to Image API documentation](https://html2img.com/docs/getting-started/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Image URLs, Text, Shell commands]

**Output Format:** [Image URLs and text; Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated image URLs from capture or conversion actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
