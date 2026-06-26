## Description: <br>
Generate AI videos from text or image inputs using Google Veo 3 and Veo 3.1 through the Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit Google Veo video-generation jobs to Media.io, check available credits, and poll task results with their own Media.io API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Media.io OpenAPI key to call the hosted service. <br>
Mitigation: Use a scoped or dedicated API key when possible, keep it in the API_KEY environment variable or pass it explicitly at runtime, and rotate it if exposed. <br>
Risk: Video generation requests and task polling are delegated to Media.io's OpenAPI service. <br>
Mitigation: Review Media.io account controls, data-retention settings, and approval practices before submitting sensitive prompts, images, or production workloads. <br>


## Reference(s): <br>
- [Media.io OpenAPI documentation](https://platform.media.io/docs/) <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-google-veo-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python examples and JSON API response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io OpenAPI key supplied through API_KEY or an explicit api_key argument.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
