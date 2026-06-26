## Description: <br>
ModelScope AI skill for text-to-image generation, image editing, visual understanding, and text generation with automatic model rotation when rate-limited. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luhuiwang](https://clawhub.ai/user/luhuiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call ModelScope models for image generation, image-to-image editing, image analysis/OCR, and chat-style text generation from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, OCR inputs, and chat history may be sent to ModelScope remote services. <br>
Mitigation: Use only approved content and avoid confidential or regulated data unless the deployment has reviewed and approved ModelScope processing. <br>
Risk: The scripts log partial API key values while rotating keys. <br>
Mitigation: Use a dedicated low-privilege ModelScope key and remove or mask API-key-prefix logging before routine use. <br>
Risk: ModelScope calls can consume quota and may encounter rate limits. <br>
Mitigation: Confirm user intent before execution, configure scoped keys, and monitor quota and rate-limit behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luhuiwang/ms-ai) <br>
- [ModelScope inference API endpoint](https://api-inference.modelscope.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Image files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text, JSON script output, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable image aspect ratios and dimensions, streaming text output, optional chat history files, and up to 4096 output tokens for text and vision calls.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
