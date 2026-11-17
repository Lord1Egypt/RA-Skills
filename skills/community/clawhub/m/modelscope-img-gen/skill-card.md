## Description:

Generates AI images through the ModelScope API, with model selection and single or multiple LoRA configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netyingxiao](https://clawhub.ai/user/netyingxiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to prompt ModelScope image-generation models, choose a model, optionally apply LoRA weights, and save the generated image to a local file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and generation requests are sent to ModelScope.

Mitigation: Avoid sensitive or regulated content in prompts and confirm ModelScope is acceptable for the intended data.

Risk: API keys can be exposed if passed on the command line or saved without appropriate local file protections.

Mitigation: Prefer an environment variable or secret manager, avoid command-line keys, and protect permissions before using --save-key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netyingxiao/skills/modelscope-img-gen)
- [ModelScope access token page](https://modelscope.cn/my/myaccesstoken)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Image file with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a ModelScope API key and may store it in ~/.modelscope/api_key when --save-key is used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
