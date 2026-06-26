## Description: <br>
Generate and edit AI images and videos with Media.io OpenAPI, including text-to-image, image-to-image, text-to-video, image-to-video, task status, and credit queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Media.io OpenAPI endpoints for AI image and video generation or editing, credit checks, and task-result polling. It is useful when an agent needs one routed Python entry point for Media.io generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, videos, and API keys are sent to Media.io. <br>
Mitigation: Use a dedicated or test API key and avoid submitting sensitive prompts, private media URLs, or proprietary videos unless approved for Media.io processing. <br>
Risk: Generation calls can consume Media.io credits. <br>
Mitigation: Monitor credit usage, query Credits before large runs, and handle insufficient-credit responses before retrying. <br>
Risk: Generated media results are returned by asynchronous external API tasks. <br>
Mitigation: Poll Task Result until the task reaches a terminal status, then review generated outputs before publishing or using them downstream. <br>


## Reference(s): <br>
- [Media.io AIGC API capability reference](references/mediaio-aigc-api-reference.md) <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>
- [Media.io credit pricing](https://developer.media.io/pricing.html) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response payloads with Python and shell usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY. Generation endpoints usually return a task ID and require polling Task Result for final media URLs.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
