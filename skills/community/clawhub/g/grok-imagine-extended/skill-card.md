## Description:

Generates and edits images and creates or animates videos with xAI Grok Imagine Extended from text prompts and optional input images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ademczuk](https://clawhub.ai/user/ademczuk)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to request xAI-generated images, image edits, text-to-video outputs, and image-to-video animations from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied image URLs or local path strings are sent to xAI.

Mitigation: Avoid sensitive prompts and private image locations when using the skill.

Risk: API credentials can be exposed if passed directly on the command line.

Mitigation: Use XAI_API_KEY or a managed secret instead of the --api-key command-line flag.

Risk: Video generation and multiple-image generation can increase external API cost.

Mitigation: Review expected costs before generating videos or batches of images.

## Reference(s):

- [xAI Image Generations documentation](https://docs.x.ai/docs/guides/image-generations)
- [ClawHub skill page](https://clawhub.ai/ademczuk/skills/grok-imagine-extended)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and saved image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY. Generated media is saved to the filename provided by the user.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
