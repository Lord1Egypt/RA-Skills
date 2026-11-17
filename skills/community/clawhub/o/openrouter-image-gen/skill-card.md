## Description:

Generate images using Google Gemini via OpenRouter API with text prompts or reference-image guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangwenyu2](https://clawhub.ai/user/yangwenyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate image files from prompts, optionally using a local reference image for style or character guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference-image option can upload any readable local file supplied through --ref to OpenRouter.

Mitigation: Use only non-sensitive prompts and reference images, avoid arbitrary local paths, and add image validation, file-size limits, path restrictions, and a clear external-upload warning before broad use.

Risk: Generated outputs can be written outside the intended workspace if an unrestricted output path is provided.

Mitigation: Keep output paths within the intended workspace and review generated files before sharing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangwenyu2/skills/openrouter-image-gen)
- [OpenRouter API endpoint](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PNG image files with command-line status text and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY or an API key passed to the script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
