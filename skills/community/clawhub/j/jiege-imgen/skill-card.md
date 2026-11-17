## Description:

Generates, edits, and saves project image assets through an OpenAI Images API-compatible gateway, including new images, reference-image edits, logos, icons, banners, covers, illustrations, backgrounds, empty states, promotional graphics, and product visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tans](https://clawhub.ai/user/tans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn project image requests into reusable PNG assets, either by generating new images or editing provided reference images. It is suited for application graphics, marketing visuals, product imagery, and project-integrated image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default gateway can receive API keys, prompts, and uploaded reference images.

Mitigation: Use the default gateway only when it is trusted, or override it with --base-url or OPENAI_BASE_URL; avoid confidential images and broad API keys.

Risk: The skill follows API-returned image URLs and writes generated assets into project paths.

Mitigation: Review output paths and inspect generated files before committing, deploying, or wiring them into sensitive projects.

Risk: Generated or edited images may be unsuitable, inaccurate, or inconsistent with project requirements.

Mitigation: Check the resulting PNG assets against the requested subject, style, dimensions, and intended use before shipping.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes PNG files to requested project paths and prints JSON containing the resolved output path and API route.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
