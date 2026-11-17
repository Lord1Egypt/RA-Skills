## Description:

Jimeng AI Image Generation helps agents generate images with Volcengine Jimeng AI Image Generation 4.0, including text-to-image, image-to-image, font-design poster mode, and up to 4K output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0521](https://clawhub.ai/user/ken0521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create or edit images through Volcengine Jimeng, including wallpapers, posters, font designs, background replacement, and saved local image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference image URLs are sent to Volcengine Jimeng for generation.

Mitigation: Install and use the skill only when that data sharing is acceptable; avoid sending sensitive prompts or reference images.

Risk: The configured Secret Key can authorize image-generation requests.

Mitigation: Keep the Secret Key private and store credentials only in environment variables or a secret manager.

Risk: Image generation may incur cost based on output image count.

Mitigation: Use --force-single when limiting generation cost is important.

## Reference(s):

- [Jimeng AI Image Generation 4.0 API Reference](references/api.md)
- [Volcengine Jimeng Product Page](https://www.volcengine.com/product/jimeng)
- [Volcengine Console](https://console.volcengine.com/)
- [ClawHub Skill Page](https://clawhub.ai/ken0521/skills/jimeng-image-gen)
- [Publisher Profile](https://clawhub.ai/user/ken0521)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and generated image URLs or saved image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JIMENG_ACCESS_KEY/JIMENG_SECRET_KEY environment variables; image URLs returned by the service are documented as time-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
