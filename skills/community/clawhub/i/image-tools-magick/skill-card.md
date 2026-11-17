## Description:

Comprehensive image editing toolkit using ImageMagick for resizing, cropping, compositing, padding, annotating, adjusting, background removal, format conversion, and image info, with operations writing to new files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform local, script-driven image manipulation with ImageMagick, including resize, crop, overlay, padding, annotation, adjustment, background removal, conversion, and image metadata inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted image text, filenames, or option values may become local shell commands in adjust.sh and annotate.sh.

Mitigation: Use only trusted local filenames, captions, and option values until those scripts avoid eval and call ImageMagick with argument arrays.

Risk: Temporary-file handling in composite.sh may be unsafe for sensitive images in shared multi-user environments.

Mitigation: Avoid processing sensitive images in shared environments until composite.sh uses mktemp with trapped cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pratiknarola/skills/image-tools-magick)
- [Publisher Profile](https://clawhub.ai/user/pratiknarola)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline bash code blocks and local file outputs from shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ImageMagick on Linux or macOS; scripts write modified images to new files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
