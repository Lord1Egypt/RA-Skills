## Description:

MiniMax image generation tool supporting text-to-image and image-to-image workflows, generating 1-9 images per request with customizable aspect ratios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang92229](https://clawhub.ai/user/lixiang92229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call the MiniMax API for text-to-image and image-to-image generation from prompts or reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to MiniMax, and image-to-image use can expose sensitive images.

Mitigation: Use only non-sensitive prompts and reference images, and confirm that MiniMax's service terms and privacy handling fit the intended use.

Risk: Generated images and prompt summaries may be stored locally in output files and a markdown call log.

Mitigation: Use a dedicated output directory, review generated files before sharing or syncing the workspace, and remove logs that contain sensitive usage history.

Risk: The output path can overwrite user-writable files if an agent or user supplies an unsafe path.

Mitigation: Restrict --output to a dedicated image directory and review file paths before execution.

Risk: The downloader can fetch unvalidated image URLs returned by the remote service.

Mitigation: Prefer base64 mode when appropriate or review network access expectations before allowing downloads.

Risk: The skill requires a MiniMax API key managed by the user.

Mitigation: Store MINIMAX_API_KEY in the environment, avoid committing secrets, and use limited or rotating keys where possible.

## Reference(s):

- [MiniMax Image Generation API Reference (English)](references/api_en.md)
- [MiniMax Image Generation API Reference (Chinese)](references/api.md)
- [MiniMax Platform](https://platform.minimaxi.com)
- [MiniMax Image Generation API Endpoint](https://api.minimaxi.com/v1/image_generation)
- [Project homepage](https://github.com/lixiang92229/lx-minimax-image-generation)
- [ClawHub skill page](https://clawhub.ai/lixiang92229/skills/lx-minimax-image-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, Python examples, and JSON API results containing image URLs, base64 image data, or local file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MINIMAX_API_KEY; URL-format results may be downloaded to a local output directory and successful calls append a local markdown log.]

## Skill Version(s):

1.1.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
