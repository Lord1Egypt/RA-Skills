## Description: <br>
Generates AI dance videos from image and driving video URLs using Media.io OpenAPI asynchronous task creation and polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check Media.io credits, submit authorized image and driving video URLs, poll asynchronous dance-video generation tasks, and return generated preview URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the Media.io API can consume account credits and requires a Media.io API key. <br>
Mitigation: Check available credits before generation, stop on insufficient credits, and avoid logging or returning raw API keys. <br>
Risk: Image, video, and preview URLs are processed by Media.io and may expose media to a third-party service or public preview-link behavior. <br>
Mitigation: Use only media the user owns or is authorized to share, and avoid private or sensitive URLs unless the user accepts Media.io processing. <br>
Risk: Generated dance videos are synthetic media that could mislead viewers if presented as real footage. <br>
Mitigation: Present generated outputs as edited or synthetic content and avoid identity verification or biometric certainty claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-ai-dance-video-generator) <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes asynchronous task status, trace IDs for troubleshooting, and generated preview URLs when Media.io returns completed results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
