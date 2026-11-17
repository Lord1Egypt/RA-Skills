## Description:

Routes requests to Meitu scene skills for image, video, product, poster, portrait, ID photo, background removal, carousel, beauty, and direct Meitu CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjie-oss](https://clawhub.ai/user/dongjie-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill pack to route visual creation and editing requests to specialized Meitu workflows or direct Meitu CLI execution. It supports poster generation, stickers, virtual try-on, product replacement, motion transfer, upscaling, ID photos, cutouts, carousels, beauty enhancement, and platform-specific image adaptation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide Meitu OpenAPI access and secret keys in chat.

Mitigation: Configure credentials with environment variables or a manually created local credentials file instead of pasting secrets into chat.

Risk: Unpinned global install and npx fallback paths may execute code that changes after review.

Mitigation: Review and trust the runtime source before installation, and prefer pinned or internally approved installation flows for controlled environments.

Risk: Memory and profile personalization can include selected local context in prompts sent to Meitu OpenAPI.

Mitigation: Disable personalization unless the user accepts this data flow, and review local context before enabling memory-backed workflows.

Risk: The external oc-workspace.mjs helper is treated as privileged local code by several workflows.

Mitigation: Verify the helper script and its permissions before use, especially in shared or production workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongjie-oss/skills/other-openclaw-skills)
- [Security Model](SECURITY.md)
- [Meitu CLI Reference](skills/meitu-poster/references/meitu-cli-guide.md)
- [Output Formats](skills/meitu-poster/references/output-formats.md)
- [Product Multi-Angle View Prompt Templates](skills/meitu-product-view/references/prompts.md)
- [Platform Size Presets](skills/meitu-image-adapt/references/platform-presets.md)
- [Video Motion Transfer Input Quality Guide](skills/meitu-video-dance/references/input-quality-guide.md)
- [Meitu OpenAPI Portal](https://www.miraclevision.com/open-claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and generated media workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Meitu CLI workflows that return task IDs, media URLs, files, and user-facing error guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
