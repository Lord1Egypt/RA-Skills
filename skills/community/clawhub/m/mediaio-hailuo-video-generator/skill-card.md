## Description: <br>
Generate AI videos using MiniMax Hailuo (Hailuo 2.3) via Media.io OpenAPI, with support for text-to-video and image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to call Media.io OpenAPI from an agent for Hailuo video generation, credit checks, task submission, and result polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, image URLs, and generation parameters to Media.io. <br>
Mitigation: Avoid submitting sensitive prompts or private image URLs unless they are appropriate to share with Media.io. <br>
Risk: The skill requires a Media.io API key and generation can consume credits or quota. <br>
Mitigation: Use a rotatable API key, monitor usage, and rotate the key if exposure or misuse is suspected. <br>
Risk: Video generation is asynchronous and may return a task ID before the final media is ready. <br>
Mitigation: Poll the Task Result API with the returned task ID and handle pending, failed, and missing-task responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/mediaio-hailuo-video-generator) <br>
- [Media.io OpenAPI Documentation](https://platform.media.io/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses with Markdown usage guidance and Python or cURL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key; generation requests return a task ID that should be polled for results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
