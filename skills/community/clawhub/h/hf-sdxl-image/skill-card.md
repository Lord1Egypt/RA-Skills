## Description: <br>
Generates a single image from a text prompt through the Hugging Face Inference API using the default SDXL model or a compatible model selected with HF_IMAGE_MODEL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slippersheepig](https://clawhub.ai/user/slippersheepig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to turn chat requests into generated images through Hugging Face, save the image to a temporary local file, and return it through the active provider's required media delivery path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends image prompts to Hugging Face and requires a Hugging Face bearer token. <br>
Mitigation: Install only when that external service use is acceptable, provide a token scoped to this purpose, and set HF_IMAGE_MODEL only to trusted models. <br>
Risk: Generated image files may persist locally if the caller saves them outside the normal temporary delivery path. <br>
Mitigation: Use a temporary output directory for chat delivery and delete the temporary file after successful send unless the user explicitly requests a persistent copy. <br>
Risk: Image delivery can fail or be misreported if the active chat provider requires a specific outbound media format. <br>
Mitigation: Use the current provider's required image or file-send path and do not claim success until the generated image has been sent through that path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/slippersheepig/hf-sdxl-image) <br>
- [Hugging Face SDXL base model](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) <br>
- [Hugging Face Inference endpoint used by the skill](https://router.huggingface.co/hf-inference/models/<model-id>) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HUGGINGFACE_TOKEN; writes generated images to a caller-specified output path and normally uses temporary storage for chat delivery.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
