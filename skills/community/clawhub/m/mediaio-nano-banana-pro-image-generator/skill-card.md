## Description: <br>
Generate AI images using Nano Banana Pro via Media.io OpenAPI, including text-to-image and reference-image workflows with up to 4K output support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to submit image-generation prompts or reference-image URLs to Media.io, receive task IDs, and query generation status and results. It is suited for workflows that need automated image generation through the Media.io OpenAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, reference image URLs, and an API key to Media.io and may consume Media.io credits. <br>
Mitigation: Use a dedicated or revocable Media.io API key, avoid confidential prompts or private image URLs, and monitor credit usage before broad deployment. <br>
Risk: The skill depends on the external `requests` package and outbound calls to Media.io services. <br>
Mitigation: Install dependencies in a controlled virtual environment, consider pinning `requests`, and review network access policies before use. <br>


## Reference(s): <br>
- [Media.io API documentation](https://platform.media.io/docs/) <br>
- [Media.io developer portal](https://developer.media.io/) <br>
- [Media.io pricing](https://developer.media.io/pricing.html) <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/mediaio-nano-banana-pro-image-generator) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Images] <br>
**Output Format:** [JSON API responses containing credit balances, task IDs, task status, and generated image result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY and may consume Media.io credits; image generation results are retrieved through asynchronous task polling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
