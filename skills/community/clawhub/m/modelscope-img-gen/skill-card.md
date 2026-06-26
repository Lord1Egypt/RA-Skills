## Description: <br>
Generates AI images through the ModelScope API with model selection and optional LoRA configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netyingxiao](https://clawhub.ai/user/netyingxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate image files from text prompts through ModelScope, including optional model and LoRA selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and model settings are sent to ModelScope. <br>
Mitigation: Use only prompts and settings that are appropriate to share with ModelScope. <br>
Risk: The ModelScope API key can be exposed through command-line history or a saved local key file. <br>
Mitigation: Prefer MODELSCOPE_API_KEY or a secure secret store, and avoid --api-key or --save-key when shared systems or logs are in scope. <br>
Risk: A generated image can overwrite an existing file at the chosen output path. <br>
Mitigation: Check the output path before running the generator and choose a unique filename when preserving existing files matters. <br>


## Reference(s): <br>
- [ModelScope AI Image Generator on ClawHub](https://clawhub.ai/netyingxiao/modelscope-img-gen) <br>
- [Publisher profile: netyingxiao](https://clawhub.ai/user/netyingxiao) <br>
- [ModelScope access token page](https://modelscope.cn/my/myaccesstoken) <br>
- [ModelScope inference API endpoint](https://api-inference.modelscope.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [Generated image file plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is result_image.jpg; users can choose a model, output path, and optional LoRA settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
