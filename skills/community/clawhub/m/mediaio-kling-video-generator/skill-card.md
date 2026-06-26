## Description: <br>
Generate high-quality AI videos from text or images using Kling via Media.io OpenAPI with cinematic visuals and smooth motion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users use this skill to call Media.io Kling generation APIs for image-to-video and prompt-driven video tasks, then poll task results and check account credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, image URLs, video URLs, task IDs, and related generation parameters to Media.io. <br>
Mitigation: Avoid submitting confidential, regulated, or non-consented media, and review Media.io handling requirements before use. <br>
Risk: The skill requires a Media.io API key for remote API calls. <br>
Mitigation: Use a dedicated or least-privilege key where possible, keep it in the API_KEY environment variable, and monitor Media.io usage. <br>


## Reference(s): <br>
- [Media.io OpenAPI Documentation](https://platform.media.io/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/mediaio-kling-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [api calls, json, code, guidance] <br>
**Output Format:** [JSON API responses with task IDs, task status, generated media results, and Python usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key; generation calls may return task IDs that need polling with the Task Result API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
