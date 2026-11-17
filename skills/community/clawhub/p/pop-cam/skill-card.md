## Description:

AI image generation in any visual style, transforming photos or generating images from text prompts via the Pop-cam NanoBanana API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petagit](https://clawhub.ai/user/petagit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate new images from prompts or transform source images through the Pop-cam NanoBanana API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source images, and related generation metadata are sent to Pop-cam for image generation.

Mitigation: Use the skill only when that third-party handling is acceptable, and avoid sensitive or regulated images unless the user has approved that data sharing.

Risk: The POPCAM_API_TOKEN is required for authenticated generation requests.

Mitigation: Keep the token private, pass it through environment variables, and refresh it if it may have been exposed.

Risk: The optional webhook_url sends generation results to a caller-provided endpoint.

Mitigation: Use webhook_url only with trusted HTTPS endpoints that the user controls.

## Reference(s):

- [Pop-cam OpenClaw](https://www.pop-cam.com/openclaw)
- [Pop-cam Skill Definition JSON](https://www.pop-cam.com/api/openclaw/skill)
- [Pop-cam NanoBanana API Endpoint](https://www.pop-cam.com/api/v1/nanobanana)
- [ClawHub Skill Page](https://clawhub.ai/petagit/skills/pop-cam)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POPCAM_API_TOKEN; outputs may include API request guidance, webhook usage guidance, and generated image download URLs.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
