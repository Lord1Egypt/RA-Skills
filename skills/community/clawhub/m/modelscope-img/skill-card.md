## Description: <br>
Generates images through the ModelScope API with selectable models and optional LoRA configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[focus883](https://clawhub.ai/user/focus883) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images from text prompts through ModelScope models, optionally choosing Qwen or Tongyi models and LoRA settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ModelScope API keys can be exposed when saved on shared machines or passed in command history. <br>
Mitigation: Prefer MODELSCOPE_API_KEY on shared machines, and review or delete ~/.modelscope/api_key when stored credentials are no longer needed. <br>
Risk: Prompts are sent to ModelScope and may contain sensitive information. <br>
Mitigation: Avoid private information in prompts and treat prompt text as data sent to an external service. <br>
Risk: The skill makes network calls and writes generated image files locally. <br>
Mitigation: Use it only when ModelScope image generation is intended, choose output paths deliberately, and review generated files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/focus883/modelscope-img) <br>
- [ModelScope access token page](https://modelscope.cn/my/myaccesstoken) <br>
- [ModelScope API inference endpoint](https://api-inference.modelscope.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts save generated images to local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ModelScope API key and writes image outputs such as result_image.jpg.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
