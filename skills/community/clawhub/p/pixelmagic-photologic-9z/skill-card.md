## Description:

PixelMagic-PhotoLogic-9z helps agents apply preset and custom ImageMagick photo edits to RAW, JPG, PNG, TIFF, and related image formats for single-image and batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[couplefishes](https://clawhub.ai/user/couplefishes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retouch, color-grade, filter, and batch process photos with ImageMagick-based presets while preserving source images and producing edited output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file writes are insufficiently constrained and could place output or preset files outside the intended folders.

Mitigation: Review generated paths before execution, use a dedicated workspace, and fix path validation before broad or automated use.

Risk: ImageMagick processing can expose the host to dependency and decoder risks when handling untrusted images or outdated installations.

Mitigation: Process only trusted images, install ImageMagick from trusted sources, and keep it current with security patches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/couplefishes/skills/pixelmagic-photologic-9z)
- [ClawHub publisher profile](https://clawhub.ai/user/couplefishes)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Image files plus concise Markdown status with file paths and optional command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create working, temporary, parameter, log, and final output files during image editing.]

## Skill Version(s):

1.1.0 (source: release evidence and _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
