## Description:

Automatically compresses oversized images on macOS with configurable width, quality, and size thresholds, and can optionally send compressed files through WeChat or Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeholdon](https://clawhub.ai/user/yeholdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to compress local PNG, JPEG, or GIF images before sharing them through messaging services or other size-limited channels. It is intended for macOS environments where the built-in `sips` tool is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can send selected local images to WeChat or Telegram.

Mitigation: Prefer the compression-only script unless the destination has been verified, and confirm the chat or contact target before running send helpers.

Risk: Certain input images can be overwritten, especially files already named with `_compressed`.

Mitigation: Use a backup or disposable copy for important images and check the output path before running compression.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yeholdon/skills/image-compression)
- [Publisher profile](https://clawhub.ai/user/yeholdon)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Files, Configuration]

**Output Format:** [Markdown guidance with bash commands, plain-text script output, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates compressed images with a `_compressed` suffix when input files exceed the configured size threshold; helper scripts can send the resulting image to WeChat or Telegram.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
