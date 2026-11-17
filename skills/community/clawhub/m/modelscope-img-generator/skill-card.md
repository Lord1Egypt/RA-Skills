## Description:

Generate images with ModelScope API. Use for image generation requests. Supports text-to-image + image-to-image; configurable models; use --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windandliberty](https://clawhub.ai/user/windandliberty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate new images or edit existing images through ModelScope community models. It supports prompt-based generation, image-to-image workflows, model selection, and LoRA adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if pasted into chat or passed through command arguments.

Mitigation: Use MODELSCOPE_API_KEY from a protected environment or secret store instead of the --api-key argument.

Risk: Prompts and input images are sent to ModelScope and may include sensitive content.

Mitigation: Use the skill only with content appropriate for ModelScope processing and avoid sensitive images or prompts.

Risk: Untrusted ModelScope models or LoRAs may produce unsafe or unsuitable results.

Mitigation: Select only trusted ModelScope models and LoRA adapters and review generated outputs before use.

Risk: Result-image downloads need review because the security guidance calls for tighter URL validation.

Mitigation: Review download behavior before installation and restrict accepted result URLs to trusted ModelScope-controlled locations where possible.

Risk: Dependencies are declared with lower bounds and are not pinned.

Mitigation: Pin dependencies in deployment environments and review updates to requests and pillow before rollout.

## Reference(s):

- [ModelScope](https://modelscope.cn)
- [ModelScope Model Hub](https://modelscope.cn/models)
- [ClawHub Skill Page](https://clawhub.ai/windandliberty/skills/modelscope-img-generator)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated image files are saved to disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MODELSCOPE_API_KEY, uv, Python 3.10+, network access to ModelScope, and trusted model or LoRA choices.]

## Skill Version(s):

1.2.0 (source: manifest.yaml and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
