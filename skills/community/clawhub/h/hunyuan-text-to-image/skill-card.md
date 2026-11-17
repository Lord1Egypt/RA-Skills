## Description:

This skill uses Tencent HunyuanImage 3.0 through a Python script to generate images from text prompts and optional reference image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Tencent Cloud HunyuanImage 3.0 for text-to-image generation and image-to-image generation from prompt text and optional reference image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image URLs are sent to Tencent Cloud for image generation.

Mitigation: Use only prompts and image URLs approved for Tencent Cloud processing, and avoid sensitive or confidential content unless the deployment policy permits it.

Risk: The skill requires Tencent Cloud credentials on the local machine.

Mitigation: Use narrowly scoped Tencent Cloud credentials, store them in a local environment file outside shared artifacts, and rotate them when access changes.

Risk: The setup guidance includes a fallback that can install Python packages into the system environment.

Mitigation: Prefer the documented virtual environment path and pin dependencies rather than using the system-package fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mebusw/skills/hunyuan-text-to-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with Python command examples and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are reported as temporary and valid for 1 hour.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
