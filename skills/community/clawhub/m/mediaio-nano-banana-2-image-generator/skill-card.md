## Description: <br>
Generate AI images using Nano Banana Pro via Media.io OpenAPI, with advanced reasoning, multi-image fusion, character consistency, and up to 4K resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to call Media.io image-generation APIs, submit text or reference-image prompts, and poll task results for generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media.io API keys are required and are sent to the Media.io OpenAPI service. <br>
Mitigation: Use a revocable Media.io API key, store it in the API_KEY environment variable, and rotate it if exposed. <br>
Risk: Image generation and the bundled credits query can affect or reveal account credit usage. <br>
Mitigation: Monitor Media.io credit usage and limit key scope or access where account controls allow. <br>
Risk: Prompts and reference image URLs may disclose sensitive or private content to the external Media.io service. <br>
Mitigation: Avoid submitting sensitive prompts, private image URLs, or confidential reference material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-nano-banana-2-image-generator) <br>
- [Media.io OpenAPI documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime calls return JSON response payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API_KEY; image generation returns a task_id, and task-result polling returns status and result payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
