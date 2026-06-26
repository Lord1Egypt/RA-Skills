## Description: <br>
Generate AI images using ByteDance Seedream via Media.io OpenAPI. Delivers high aesthetic quality and detailed rendering for text-to-image and image-to-image tasks with 4K support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate and edit images with ByteDance Seedream 4.0 through Media.io OpenAPI, including text-to-image and image-to-image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, reference image URLs, task IDs, and an API key to Media.io. <br>
Mitigation: Use a revocable API key and avoid submitting sensitive prompts or private/internal image URLs. <br>
Risk: Media.io generation and account credit calls may consume account credits. <br>
Mitigation: Monitor credit usage and confirm the selected workflow before invoking generation APIs. <br>
Risk: The skill depends on the Python requests package to call the Media.io API. <br>
Mitigation: Install requests from a trusted Python package source in the intended runtime environment. <br>


## Reference(s): <br>
- [Seedream AI Image Generator on ClawHub](https://clawhub.ai/wondershare-boop/mediaio-seedream-image-generator) <br>
- [Media.io API Documentation](https://platform.media.io/docs/) <br>
- [Media.io Developer Portal](https://developer.media.io/) <br>
- [Media.io Pricing](https://developer.media.io/pricing.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; Media.io API calls return JSON task and status responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY and calls openapi.media.io for credit lookup, generation task creation, and task result polling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
