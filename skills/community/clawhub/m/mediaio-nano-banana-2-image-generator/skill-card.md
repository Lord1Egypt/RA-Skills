## Description:

Generate AI images using Nano Banana Pro through Media.io OpenAPI, including prompt-based generation, image inputs, aspect ratio selection, and up to 4K output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call Media.io image-generation APIs, submit prompts and optional reference images, and query asynchronous task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, task IDs, reference image URLs, and the Media.io API key are sent to Media.io.

Mitigation: Use a dedicated Media.io API key with limited account exposure and avoid submitting sensitive prompts or image URLs unless approved for that service.

Risk: The skill installs and imports the requests dependency without a pinned requirements file.

Mitigation: Install dependencies in an isolated environment and pin requests through a reviewed requirements file before production use.

Risk: Running the router script directly queries and prints account credits.

Mitigation: Run the script only in an appropriate environment and avoid exposing terminal logs that may reveal account usage information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/mediaio-nano-banana-2-image-generator)
- [Media.io API Documentation](https://platform.media.io/docs/)
- [Media.io Developer Portal](https://developer.media.io/)
- [Media.io Pricing](https://developer.media.io/pricing.html)
- [Nano Banana Pro Endpoint](https://openapi.media.io/generation/banana/i2i-banana-2)
- [Task Result Endpoint](https://openapi.media.io/generation/result/{task_id})
- [Credits Endpoint](https://openapi.media.io/user/credits)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks plus JSON API responses from Media.io]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key in API_KEY; generated image jobs return task IDs that must be queried for final results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
