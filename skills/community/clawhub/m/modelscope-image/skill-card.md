## Description:

Generates images through the ModelScope API by helping an agent list supported models, shape a prompt, select a text-to-image model, and run the bundled generation script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyz0825](https://clawhub.ai/user/baiyz0825)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate image assets from Chinese or English text prompts through ModelScope-hosted text-to-image models. It is useful when an agent needs guidance for model selection, prompt drafting, API invocation, and collecting generated image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed when passed as command-line arguments.

Mitigation: Use MODELSCOPE_API_KEY through an environment variable or secret manager and avoid the --api-key option.

Risk: Prompts are sent to an external ModelScope service and may include sensitive user content.

Mitigation: Do not submit confidential prompts, private data, or regulated content unless the deployment has appropriate approval.

Risk: The script downloads provider-supplied image URLs and writes generated files locally.

Mitigation: Run in a constrained environment, review output paths, and limit outbound network access and generated output size.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiyz0825/skills/modelscope-image)
- [ModelScope API reference](references/api_reference.md)
- [ModelScope model list](references/models.md)
- [AI art prompt guide](references/prompt_guide.md)
- [ModelScope API inference documentation](https://modelscope.cn/docs/model-service/API-Inference/intro)
- [ModelScope API inference limits](https://modelscope.cn/docs/model-service/API-Inference/limits)
- [ModelScope model catalog](https://modelscope.cn/models)
- [ModelScope AIGC models](https://modelscope.cn/aigc/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated runs produce PNG files, prompts.json, and an index.html gallery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MODELSCOPE_API_KEY; accepts model, prompt, count, size, output directory, and API key parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
