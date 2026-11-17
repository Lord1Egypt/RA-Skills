## Description:

Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate batches of images from random or user-provided prompts through the OpenAI Images API, then review the resulting image files, prompt mapping, and gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to OpenAI for image generation.

Mitigation: Avoid private or sensitive prompt content unless sending it to the API provider is intended.

Risk: The skill writes generated images, prompts.json, and index.html to local storage.

Mitigation: Use --out-dir to choose the output location and review generated files before sharing or publishing them.

Risk: The skill requires an OpenAI API key.

Mitigation: Provide OPENAI_API_KEY only in an environment where use of the key and related API costs are authorized.

## Reference(s):

- [OpenAI Images API documentation](https://platform.openai.com/docs/api-reference/images)
- [ClawHub skill page](https://clawhub.ai/andy27725/skills/openai-image-gen-andy27725)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files]

**Output Format:** [Command-line execution that writes image files, prompts.json, and an index.html gallery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and OPENAI_API_KEY; supports model, prompt, count, size, quality, output format, background, style, and output directory options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
