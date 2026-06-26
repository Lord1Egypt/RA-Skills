## Description: <br>
Generates images through the ModelScope API by listing supported models, helping the agent prepare an optimized prompt, and calling the selected text-to-image model. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[baiyz0825](https://clawhub.ai/user/baiyz0825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to choose a ModelScope text-to-image model, create a prompt from a user request, and generate local image outputs. The bundled ModelScope API reference describes API Inference as suitable for functional testing and early validation rather than commercial API use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation settings are sent to ModelScope using the user's API key. <br>
Mitigation: Avoid including secrets, regulated personal data, or confidential content in prompts; only use the skill when sending this data to ModelScope is acceptable. <br>
Risk: Passing the API key with --api-key may expose it in shell history or process listings. <br>
Mitigation: Set MODELSCOPE_API_KEY in the environment and avoid placing the key directly on the command line. <br>
Risk: ModelScope API Inference is documented by the skill as non-commercial and intended for functional testing and early validation. <br>
Mitigation: Confirm ModelScope service terms and choose an appropriate paid or approved service path before commercial use. <br>
Risk: Generated images and prompt mappings are written to a local output directory. <br>
Mitigation: Choose an appropriate output directory and review generated PNG, prompts.json, and index.html files before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baiyz0825/modelscope-image) <br>
- [ModelScope API Inference introduction](https://modelscope.cn/docs/model-service/API-Inference/intro) <br>
- [ModelScope API Inference limits](https://modelscope.cn/docs/model-service/API-Inference/limits) <br>
- [ModelScope model library](https://modelscope.cn/models) <br>
- [API reference](references/api_reference.md) <br>
- [Model list](references/models.md) <br>
- [Prompt guide](references/prompt_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance, CLI commands, PNG image files, prompts.json, and index.html] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MODELSCOPE_API_KEY; sends prompts and generation settings to ModelScope and saves generated files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
