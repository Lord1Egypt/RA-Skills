## Description:

Generates AI videos from text or images using Kling models through Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to call Media.io Kling video-generation APIs, check credits, submit generation requests, and poll task results from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party media handling and retention terms are under-disclosed.

Mitigation: Avoid submitting sensitive private media or confidential prompts, and confirm Media.io billing and retention terms before use.

Risk: Authenticated API requests may follow redirects and expose the API key outside the intended request path.

Mitigation: Use a dedicated low-privilege or low-credit Media.io API key and prefer a patched router that disables redirects for authenticated requests.

## Reference(s):

- [Media.io OpenAPI Documentation](https://platform.media.io/docs/)
- [ClawHub Skill Release](https://clawhub.ai/wondershare-boop/skills/mediaio-kling-video-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python or cURL examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io OpenAPI key in API_KEY and returns task IDs that can be polled for generated video results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
