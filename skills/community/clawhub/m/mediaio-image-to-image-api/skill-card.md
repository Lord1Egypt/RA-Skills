## Description: <br>
Transform existing images into new ones using AI via Media.io OpenAPI, including style transfers, artistic filters, and creative transformations with models such as Seedream and Nano Banana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Media.io image-to-image generation APIs, transform source image URLs with text prompts, and poll task results for generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and related task data are sent to Media.io. <br>
Mitigation: Avoid sensitive or internal image URLs and review Media.io terms before use. <br>
Risk: The skill requires a Media.io API key for authenticated requests. <br>
Mitigation: Use a revocable API key, store it in the API_KEY environment variable, and rotate it if exposed. <br>
Risk: The helper script depends on the requests Python package. <br>
Mitigation: Install dependencies from a trusted package source and keep the runtime environment controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-image-to-image-api) <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>
- [Media.io pricing](https://developer.media.io/pricing.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API calls, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell examples; Media.io API calls return JSON task and result payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Media.io API key and publicly reachable input image URLs; generation APIs return task IDs that must be polled for results.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
