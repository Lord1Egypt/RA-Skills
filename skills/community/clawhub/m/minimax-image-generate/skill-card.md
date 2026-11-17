## Description:

MiniMax image generation skill for text-to-image and image-to-image workflows, supporting multiple aspect ratios and URL or Base64 image responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silingyuan0](https://clawhub.ai/user/silingyuan0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images through the MiniMax API from text prompts or reference images, then save generated outputs locally or return URL/Base64 image data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to MiniMax as part of image generation or editing.

Mitigation: Use only prompts and images that are approved for external processing, and avoid secrets, private data, or sensitive images.

Risk: The downloader can fetch arbitrary image URLs and write to caller-chosen local paths.

Mitigation: Restrict image URLs to trusted sources and save outputs only inside a dedicated output directory.

Risk: The skill depends on a MiniMax API key in the runtime environment.

Mitigation: Keep MINIMAX_API_KEY scoped and secret-managed, and rotate it if it is exposed.

## Reference(s):

- [MiniMax API reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/silingyuan0/skills/minimax-image-generate)
- [MiniMax China API base URL](https://api.minimaxi.com/v1)
- [MiniMax International API base URL](https://api.minimax.io/v1)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python function usage; generated image outputs are saved files, URLs, or Base64 strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and optional MINIMAX_REGION; URL responses are documented as valid for 1 hour.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
