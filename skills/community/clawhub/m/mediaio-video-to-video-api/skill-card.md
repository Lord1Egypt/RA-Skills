## Description: <br>
Transform and restyle existing videos using AI via Media.io OpenAPI, including style transfer, creative effects, and video transformation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call Media.io OpenAPI for video-to-video transformation, credit checks, and task result retrieval. It is suited for workflows that submit media URLs, image URLs, and prompts to Media.io and then poll for generated video task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends media URLs, image URLs, prompts, and an API key to Media.io for processing. <br>
Mitigation: Use a dedicated, revocable Media.io API key and avoid submitting sensitive private media unless Media.io's handling of that data is acceptable. <br>
Risk: API calls consume Media.io credits and may create asynchronous generation tasks. <br>
Mitigation: Check available credits before submitting work and use the task result API to monitor task status. <br>


## Reference(s): <br>
- [Media.io OpenAPI documentation](https://platform.media.io/docs/) <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-video-to-video-api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses and Markdown guidance with optional Python or cURL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key in API_KEY or an explicitly supplied api_key; sends submitted media URLs, image URLs, and prompts to Media.io.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
