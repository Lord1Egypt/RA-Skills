## Description:

Uses the Laozhang API to generate and edit images with text prompts, image URLs, multi-image fusion, model selection, aspect-ratio options, and optional local saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enihsago](https://clawhub.ai/user/enihsago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images from prompts or edit one or more image URLs through Laozhang API models. It is suited for workflows that need command examples, model selection guidance, and generated image files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and API tokens are sent to api.laozhang.ai.

Mitigation: Use a restricted token file with tight permissions, avoid sensitive or private images, and avoid passing tokens directly on the command line.

Risk: Billing and output behavior may vary by selected model.

Mitigation: Explicitly choose the model for each run and review documented pricing and return formats before use.

Risk: Generated or downloaded image data may be written to local storage.

Mitigation: Use --no-save when local files are not wanted, or provide an explicit output path for controlled storage.

## Reference(s):

- [Model Details](references/models.md)
- [Usage Examples](examples/usage.md)
- [Laozhang API Documentation](https://docs.laozhang.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; the scripts can emit image URLs, JSON responses, and local PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls a remote image API and saves the first generated image locally unless --no-save is used.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
