## Description: <br>
Generate images with ModelScope API. Use for image generation requests. Supports text-to-image + image-to-image; configurable models; use --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windandliberty](https://clawhub.ai/user/windandliberty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new images or edit existing images through ModelScope community image models. It supports text prompts, optional input images, model selection, and LoRA configuration while saving the generated image to the current working directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional input images are sent to ModelScope for generation or editing. <br>
Mitigation: Install and use only when the user trusts ModelScope with the prompts and input images provided. <br>
Risk: The script downloads the final image from a URL returned by ModelScope, which may be a storage or CDN URL rather than the main API host. <br>
Mitigation: Review generated files before use and keep the skill's API endpoint fixed to the official ModelScope endpoint. <br>
Risk: Generated files are saved locally and can overwrite a caller-specified path. <br>
Mitigation: Use explicit, unique output filenames in the current working directory and review paths before running commands. <br>


## Reference(s): <br>
- [ModelScope](https://modelscope.cn) <br>
- [ModelScope Model Hub](https://modelscope.cn/models) <br>
- [ModelScope API Endpoint](https://api-inference.modelscope.cn/) <br>
- [ClawHub Skill Page](https://clawhub.ai/windandliberty/modelscope-img-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/windandliberty) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated image files saved locally by the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MODELSCOPE_API_KEY, uv, Python 3.10+, requests, and pillow; may download the final image from a ModelScope-returned storage or CDN URL.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
