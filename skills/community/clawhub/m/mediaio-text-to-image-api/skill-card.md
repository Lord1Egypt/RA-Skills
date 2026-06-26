## Description: <br>
Generate AI images from text descriptions using Media.io OpenAPI. Provide a text prompt and receive a high-quality AI-generated image. Supports multiple models including Imagen 4, Seedream, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Media.io text-to-image generation APIs from prompts, configure required API credentials, submit generation jobs, and check task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API router can call more than image-generation endpoints, including account credit inspection. <br>
Mitigation: Review the configured API definitions before use and prefer a release that restricts callable operations to the image-generation and task-result endpoints needed for the workflow. <br>
Risk: The skill requires a provider API key for outbound Media.io API calls. <br>
Mitigation: Use a scoped or dedicated API key where available, store it only in the intended environment variable or secret store, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wondershare-boop/mediaio-text-to-image-api) <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Code, Configuration guidance] <br>
**Output Format:** [JSON API responses with Markdown and Python usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key supplied through API_KEY or an explicit api_key argument.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
