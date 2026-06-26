## Description: <br>
Generate AI videos from text descriptions using Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to check Media.io credits, submit text-to-video generation jobs, and poll task results through Media.io OpenAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends text prompts to Media.io and requires a Media.io API key. <br>
Mitigation: Treat API_KEY as a secret and avoid confidential or regulated prompt content unless Media.io's terms are acceptable for that data. <br>
Risk: Text-to-video generation can consume account credits. <br>
Mitigation: Check credits before generation and monitor usage for the Media.io account tied to the API key. <br>


## Reference(s): <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [ClawHub release page](https://clawhub.ai/wondershare-boop/mediaio-text-to-video-api) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key in API_KEY or an explicit api_key argument; video generation returns a task_id for polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
