## Description:

Generates AI images from text prompts through ModelScope, with supported model selection and optional LoRA settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[focus883](https://clawhub.ai/user/focus883)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting developers and creators use this skill to generate image files from text prompts through ModelScope models, including Qwen Image and Tongyi Z-Image, with optional LoRA configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be persisted in a local plaintext configuration file.

Mitigation: Prefer MODELSCOPE_API_KEY from a protected environment variable or a key manager, and avoid --api-key or --save-key on shared systems.

Risk: Prompts, model settings, and the ModelScope token are sent to an external ModelScope API.

Mitigation: Use only when external processing is acceptable, and avoid prompts containing private, proprietary, or regulated information.

Risk: The security verdict recommends review before installation.

Mitigation: Run the skill in a dedicated virtual environment and review the scripts before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/focus883/skills/modelscope-img)
- [ModelScope access token page](https://modelscope.cn/my/myaccesstoken)
- [ModelScope inference API endpoint](https://api-inference.modelscope.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated images are saved as local image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output path is result_image.jpg unless the user provides another path.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
