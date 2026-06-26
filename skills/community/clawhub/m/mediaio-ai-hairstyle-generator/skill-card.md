## Description: <br>
Try different hairstyles and accessories on photos using AI via Media.io OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit user-authorized portrait image URLs to Media.io, poll the asynchronous hairstyle-generation task, and return generated preview URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portrait image URLs are sent to Media.io for processing. <br>
Mitigation: Use only user-provided or user-authorized images, and avoid private, sensitive, or unauthorized images. <br>
Risk: Generated preview URLs may be shareable links. <br>
Mitigation: Treat preview URLs as potentially accessible outside the chat or local environment. <br>
Risk: The Media.io API key could be exposed through logs or responses. <br>
Mitigation: Keep MEDIAIO_API_KEY out of chat logs, command output, and user-facing responses. <br>


## Reference(s): <br>
- [Media.io platform](https://developer.media.io/) <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-ai-hairstyle-generator) <br>
- [Publisher profile](https://clawhub.ai/user/wondershare-boop) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns asynchronous task status and generated preview URLs when Media.io completes processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
