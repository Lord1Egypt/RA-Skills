## Description: <br>
Apply AI-powered age transformation filters to images using Media.io OpenAPI to render younger or older versions of faces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit an authorized face image URL to Media.io, choose an older or younger age effect, and retrieve generated synthetic image URLs after asynchronous processing completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected face image URLs to Media.io for processing. <br>
Mitigation: Use only user-provided or user-authorized images, avoid sensitive private photos unless Media.io's terms are acceptable, and present results as synthetic edited media. <br>
Risk: The skill requires a Media.io API key and can consume paid credits. <br>
Mitigation: Keep the API key out of logs and responses, check credits before generation, and stop with a clear message when credits are insufficient. <br>


## Reference(s): <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer platform](https://developer.media.io/) <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-ai-age-filter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task status guidance and generated image preview URLs when Media.io completes processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
