## Description:

Generates images with MiniMax image-01 and image-01-live models for text-to-image and image-to-image workflows that require a MiniMax Coding Plan API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanycun](https://clawhub.ai/user/wanycun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to invoke MiniMax image generation from prompts or input image URLs, choose supported models, aspect ratios, output formats, seeds, and style options, and receive generated image URLs or base64 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples that pass the MiniMax API key with --api-key can expose the key through shell history or process listings.

Mitigation: Use MINIMAX_API_KEY from the environment and avoid passing secrets directly as command-line arguments.

Risk: Prompts, private image URLs, signed URLs, or regulated data submitted to MiniMax leave the local environment for external processing.

Mitigation: Do not submit confidential prompts, private or signed image URLs, or regulated data unless the deployment has approved MiniMax for that data.

Risk: The artifact specifies an unpinned dependency range for requests.

Mitigation: Use a pinned dependency lockfile before production use.

## Reference(s):

- [MiniMax API key settings](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- [MiniMax image generation API endpoint](https://api.minimaxi.com/v1/image_generation)
- [ClawHub skill page](https://clawhub.ai/wanycun/skills/minimax-image-generation)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Text]

**Output Format:** [Markdown guidance with shell commands and optional JSON or text output from the MiniMax image script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated image URLs or base64 data depending on the selected response format.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
