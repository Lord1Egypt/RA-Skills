## Description:

Generate AI images from text prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfango](https://clawhub.ai/user/0xfango)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate AI images from text prompts, choose model, resolution, aspect ratio, and optional reference images, then display or save the generated image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image URLs are sent to Labnana's external API.

Mitigation: Avoid sensitive prompt content and private reference URLs; use the skill only when this external data flow is acceptable.

Risk: Raw curl examples can be unsafe if user-controlled text is interpolated into shell strings.

Mitigation: Build request bodies with safe JSON serialization and review generated commands before execution.

Risk: The image generation API could be called before the user has reviewed the final parameters.

Mitigation: Require explicit user confirmation before submitting any generation request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xfango/skills/marswave-image-gen)
- [Image Prompt Guide](references/prompt-guide.md)
- [Labnana Image Generation API](https://api.labnana.com/openapi/v1/images/generation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with inline shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May display generated images inline or save JPEG files under .listenhub/image-gen/YYYY-MM-DD-{jobId}/, depending on configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
