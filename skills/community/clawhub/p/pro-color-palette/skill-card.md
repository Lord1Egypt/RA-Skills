## Description:

Pro Color Palette helps agents generate color palette cards, extract dominant colors from images, and create poster, phone UI, or cover mockups from preset palettes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryantaozi](https://clawhub.ai/user/ryantaozi)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and content creators use this skill to choose preset color schemes, produce image palette cards, extract palettes from source images, and preview those palettes in simple branded mockups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URL inputs can trigger unrestricted network requests and write downloaded content to a predictable temporary file.

Mitigation: Prefer local image files, avoid untrusted or internal/private URLs, and validate destinations, response size, image type, and temporary-file handling before shared or server use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryantaozi/skills/pro-color-palette)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, color tables, file paths, and generated image references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG palette cards and mockup images through bundled Python scripts.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
