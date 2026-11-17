## Description:

Image-2 helps agents generate, edit, vary, and describe images using OpenAI image and vision APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt](https://clawhub.ai/user/gpt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, marketers, developers, and agent operators use this skill to create image assets, edit existing images, generate variations, and analyze image content from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source images, masks, and URL-fetched image content may be sent to OpenAI.

Mitigation: Use only approved content, avoid sensitive or regulated images, and confirm users understand that image data may leave the local workspace.

Risk: The skill can read arbitrary local image paths or fetch image URLs for upload or analysis.

Mitigation: Run it in a restricted workspace and avoid sensitive local paths, HTTP URLs, and private-network URLs.

Risk: Generated or edited outputs can be saved or overwritten outside a dedicated output folder.

Mitigation: Keep output paths under a dedicated generated-images directory and check target filenames before writing.

Risk: The runtime dependency is declared with a broad semver range.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gpt/skills/image-2)
- [ClawHub metadata homepage](https://clawhub.ai/gpt/image-2)
- [Artifact README](artifact/README.md)
- [Prompt gallery](artifact/examples/prompts-gallery.md)
- [Quick starts](artifact/examples/quick-starts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JavaScript helper calls, JSON-like result objects, local file paths, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved locally by default under ./generated-images when helper functions are used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
