## Description:

Converts a reference image or text description into a centered, low-resolution pixel sprite while preserving the subject's recognizable design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzfly](https://clawhub.ai/user/yzfly)

### License/Terms of Use:

MIT

## Use Case:

External users and creators use this skill to turn a reference image or text description into a retro game style sprite. When image generation is unavailable, it provides a subject feature card and a reusable prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images and descriptions may be sent to the configured image service.

Mitigation: Use confidential material only when the image service's data handling is acceptable.

Risk: The documented installer runs globally without confirmation and uses unpinned sources.

Mitigation: Install manually or review and pin the source version before installing.

## Reference(s):

- [ClawHub release](https://clawhub.ai/yzfly/skills/pixel-sprite)
- [Project repository (listed in README)](https://github.com/yzfly/skills)
- [Chinese prompt template](artifact/references/prompt.zh-CN.md)
- [English prompt template](artifact/references/prompt.en.md)

## Skill Output:

**Output Type(s):** [Images, Text, Guidance]

**Output Format:** [A generated pixel sprite image when image generation is available; otherwise a subject feature card and reusable prompt in Markdown text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One centered subject; defaults to 32×32, a 6–8 color palette, and a white background. Size, palette, background, and subject count can be adjusted.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
