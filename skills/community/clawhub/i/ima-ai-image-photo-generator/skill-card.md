## Description:

Generates and edits AI images for posters, thumbnails, logos, art, illustrations, product photos, and social media graphics using IMA Studio image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dai-shuo](https://clawhub.ai/user/dai-shuo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, designers, and agents use this skill to generate or transform images from text prompts or input images. Common tasks include product photography, posters, thumbnails, logos, illustrations, art, and social media graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected input images, and the IMA API key are sent to IMA services during generation.

Mitigation: Use a scoped or low-quota test key, avoid sensitive prompts or private images, and rotate credentials after testing.

Risk: Custom service endpoints can expose credentials or generated content to servers the user does not control.

Mitigation: Do not set custom base URLs unless they are controlled and trusted by the user.

Risk: Model preferences and generation logs may be stored under ~/.openclaw.

Mitigation: Review or clear ~/.openclaw logs and preferences after use when working with sensitive projects.

## Reference(s):

- [IMA Studio](https://imastudio.com)
- [ClawHub Skill Page](https://clawhub.ai/dai-shuo/skills/ima-ai-image-photo-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON result handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generation guidance for agents and image-result URLs from IMA services; requires IMA_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
