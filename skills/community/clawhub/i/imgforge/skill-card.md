## Description:

Generate AI images for free using Z-Image-Turbo. Say "generate an image of..." and get stunning results in seconds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistant users use this skill to turn natural-language prompts into image files for thumbnails, avatars, banners, concept art, and visual mockups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the ModelScope API token are sent to ModelScope/Alibaba services.

Mitigation: Avoid secrets, private business data, and personal data in prompts; keep MODELSCOPE_API_KEY out of shared logs and repositories.

Risk: The current downloader saves bytes from an API-provided image URL without tight destination or size checks.

Mitigation: Run the skill in a controlled workspace, review output paths before execution, and avoid privileged directories for generated files.

Risk: The security verdict is suspicious because external API calls and image downloads require review.

Mitigation: Review and scan the skill before deployment, and install only from a trusted or pinned release source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurizerush/skills/imgforge)
- [ClawHub publisher profile](https://clawhub.ai/user/futurizerush)
- [Project homepage](https://github.com/FuturizeRush/zimage-skill)
- [Z-Image project](https://github.com/Tongyi-MAI/Z-Image)
- [Z-Image-Turbo model card](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)
- [ModelScope API inference limits](https://modelscope.ai/docs/model-service/API-Inference/limits)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, JSON]

**Output Format:** [Markdown guidance with shell commands; the CLI can save image files and optionally print JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MODELSCOPE_API_KEY; supports width and height from 512 to 2048 pixels and an optional JSON output mode.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
