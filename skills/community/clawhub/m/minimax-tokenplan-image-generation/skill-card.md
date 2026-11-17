## Description:

Generates images with the MiniMax image-01 model from text prompts or reference images, with prompt optimization and watermark controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4833675](https://clawhub.ai/user/4833675)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure MiniMax image generation and run text-to-image or image-to-image requests through the bundled Python script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real MiniMax API key could be stored in the skill source or documentation during setup.

Mitigation: Use an environment variable or secret store for MINIMAX_API_KEY and avoid committing configured credentials.

Risk: Prompts and reference images are sent to a third-party MiniMax endpoint.

Mitigation: Avoid sending sensitive prompts or local reference images unless the user has approved third-party processing.

Risk: The custom --base-url option can redirect requests to an unintended endpoint.

Mitigation: Use the documented MiniMax API hosts and review any custom endpoint before execution.

Risk: Configured output paths can overwrite existing writable files.

Mitigation: Choose output locations deliberately and review paths before running the generator.

## Reference(s):

- [MiniMax Image Generation Documentation](https://platform.minimaxi.com/docs/guides/image-generation)
- [ClawHub Skill Page](https://clawhub.ai/4833675/skills/minimax-tokenplan-image-generation)
- [ClawHub Install Link](https://clawhub.ai/skills/minimax-tokenplan-image-generation)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown instructions with shell commands; script stdout returns saved image paths or temporary image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports base64 image saving, URL response mode, configurable output paths, one to nine generated images, and optional reference-image input.]

## Skill Version(s):

0.9.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
