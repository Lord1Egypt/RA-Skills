## Description:

Generates and reimagines PNG images through xAI Grok/Flux image APIs using prompts, styles, aspect ratios, and batch settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nixeifoit](https://clawhub.ai/user/nixeifoit)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate new PNG images or create style-transfer reimaginings from source images with xAI Grok/Flux models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to xAI for image generation or reimagining.

Mitigation: Avoid sensitive images, private documents, and confidential prompts unless the deployment has approved xAI data handling for that content.

Risk: The release security summary reports unsafe command examples that could run unintended code if copied with untrusted inputs.

Mitigation: Review and adapt shell and Python snippets before execution, and pass user-controlled values through structured data or safely quoted files.

Risk: Image editing is described as reimagination rather than pixel-precise editing.

Mitigation: Use the skill for style transfer and generated variants, and avoid relying on it for exact inpainting or preservation of unchanged regions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nixeifoit/skills/grok-imagine-image-pro)
- [xAI image generations API endpoint](https://api.x.ai/v1/images/generations)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Files, Configuration instructions]

**Output Format:** [Markdown guidance with shell and Python snippets that produce PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY plus curl and python3; generated images are saved as PNG files from base64 API responses.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
