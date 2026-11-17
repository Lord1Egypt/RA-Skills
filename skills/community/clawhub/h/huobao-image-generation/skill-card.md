## Description:

AI 火宝 generates images from text prompts or transforms existing image URLs using configurable AI image models, size, count, watermark, and API key settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongweigen](https://clawhub.ai/user/kongweigen)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to run text-to-image and image-to-image generation workflows from an agent environment. The skill returns structured JSON containing generated image URLs, request settings, and usage data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and API credentials are sent to an undisclosed chatfire.site endpoint despite Volcengine branding.

Mitigation: Review the endpoint before installation, use a narrowly scoped disposable API key, and avoid sensitive prompts or private image URLs.

Risk: Passing API keys on the command line or enabling debug mode can expose credentials or prompt content in shared terminals, CI logs, or shell history.

Mitigation: Prefer the HUOBAO_API_KEY environment variable and keep debug mode disabled in logged or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongweigen/skills/huobao-image-generation)
- [ClawHub publisher profile](https://clawhub.ai/user/kongweigen)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Image URLs, Shell commands]

**Output Format:** [JSON printed to standard output, with command-line usage examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful responses include generated image URLs and usage data; failures are reported as JSON or stderr errors.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
