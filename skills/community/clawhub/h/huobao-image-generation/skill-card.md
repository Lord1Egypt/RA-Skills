## Description: <br>
Generates images from text prompts or transforms URL-hosted input images using configurable model, size, count, watermark, and API key settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongweigen](https://clawhub.ai/user/kongweigen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI content creators use this skill to request text-to-image generation or image-to-image transformation from an agent workflow. It is suited for workflows that can send prompts, URL-hosted source images, and API credentials to the configured image-generation endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, generated-image requests, and API keys are sent to api.chatfire.site, which the security summary says is not clearly disclosed in the skill documentation. <br>
Mitigation: Install only if you trust that endpoint, use a dedicated revocable API key, and do not submit confidential or regulated data. <br>
Risk: API keys can be supplied on the command line. <br>
Mitigation: Prefer HUOBAO_API_KEY or a secret manager, avoid command-line secrets, and rotate keys if they may have appeared in shell history, process listings, or logs. <br>
Risk: The code does not enforce the documented generation-count limit. <br>
Mitigation: Keep count values within the documented 1-4 range and review automated calls before using the skill in unattended workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongweigen/huobao-image-generation) <br>
- [Publisher profile](https://clawhub.ai/user/kongweigen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON responses containing success state, prompt details, model, size, generated image URLs, and usage data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key through HUOBAO_API_KEY or --api-key; image-to-image input must be an HTTP or HTTPS image URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
