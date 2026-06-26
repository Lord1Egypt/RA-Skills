## Description: <br>
Generates MiniMax image-01 prompts, calls the MiniMax image generation API, and saves generated PNG images for creative, marketing, web, app, and general visual requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asimons81](https://clawhub.ai/user/asimons81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external users use this skill to turn image requests into detailed MiniMax image-01 prompts, generate images through the MiniMax API, and receive the prompt and generation parameters for iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to MiniMax using the configured API key. <br>
Mitigation: Install only when MiniMax image generation is intended, configure MINIMAX_API_KEY deliberately, and avoid sending sensitive prompt content. <br>
Risk: Generated images may be saved to the local workspace by default. <br>
Mitigation: Review the output path and generated files, and pass an explicit output path when storage location matters. <br>
Risk: The skill has broad activation language for image-related requests. <br>
Mitigation: Review activation behavior before deployment and confirm generated prompts and parameters before relying on the output. <br>


## Reference(s): <br>
- [MiniMax image generation API endpoint](https://api.minimax.io/v1/image_generation) <br>
- [ClawHub skill page](https://clawhub.ai/asimons81/minimax-imagegen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, JSON, Guidance] <br>
**Output Format:** [Markdown response with a generated image path, prompt, parameters, and JSON result metadata from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; generated PNG images are saved under ~/.openclaw/workspace/images unless another output path is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
