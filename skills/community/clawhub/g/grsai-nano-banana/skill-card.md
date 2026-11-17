## Description:

Generates images with the grsai nano-banana model from text prompts or reference-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiww](https://clawhub.ai/user/ruiww)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to create text-to-image or image-to-image requests through grsai, poll for completion, and save generated images to a local output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and the grsai API key are sent to the configured endpoint.

Mitigation: Use trusted grsai accounts and endpoints, avoid sensitive prompts or internal image URLs, and avoid placing real API keys in command-line history.

Risk: A custom base URL can redirect API requests and credentials to a different destination.

Mitigation: Use the default service endpoint unless the replacement endpoint is fully trusted.

Risk: Generated image files are downloaded and saved to a local directory where existing files could be overwritten.

Mitigation: Save outputs only to a controlled directory where overwrites are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruiww/skills/grsai-nano-banana)
- [grsai homepage](https://grsai.ai/)
- [grsai nano-banana documentation](https://grsai.ai/zh/dashboard/documents/nano-banana)
- [grsai dashboard](https://grsai.ai/zh/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, curl, and a grsai API key; supports prompt, model, resolution, aspect ratio, input image URL, polling, filename, output directory, and base URL options.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
