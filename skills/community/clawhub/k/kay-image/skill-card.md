## Description:

Kay Image helps agents generate images from text or reference images and analyze images or videos through KIE AI and optional LaoZhang API integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papayalove](https://clawhub.ai/user/papayalove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Kay Image to create images, edit images from references, inspect image or video content, and poll generation task status from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images or videos may be sent to cloud AI providers.

Mitigation: Use only data suitable for the configured providers and avoid confidential or regulated media unless provider handling is acceptable.

Risk: Custom base URL environment variables can redirect API-key-bearing requests.

Mitigation: Use clean, trusted environment variables and avoid setting custom *_BASE_URL values unless the endpoint is explicitly trusted.

Risk: The release under-discloses some external routing and provider credentials.

Mitigation: Review configured providers and credentials before deployment, and prefer a version that declares all providers and validates API destinations.

## Reference(s):

- [Kay Image ClawHub listing](https://clawhub.ai/papayalove/skills/kay-image)
- [KIE AI](https://kie.ai/)
- [KIE AI API endpoint](https://api.kie.ai)
- [LaoZhang API endpoint](https://api.laozhang.ai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [CLI output, generated image files, downloaded media files, and optional text analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KIE_API_KEY for image generation; understanding mode uses KIE_UNDERSTANDING_API_KEY by default or LAOZHANG_API_KEY when configured.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
