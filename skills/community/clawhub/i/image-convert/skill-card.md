## Description:

Image format conversion, compression, and video-to-GIF conversion for PNG, JPG, WebP, GIF, BMP, TIFF, HEIC, and AVIF workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyton](https://clawhub.ai/user/sunnyton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and technical users use this skill to get concise command guidance for converting, compressing, resizing, and optimizing local image or video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some example commands can overwrite files through force flags, in-place optimization, or matching input and output names.

Mitigation: Write to a new filename or create a backup before running conversion or optimization commands.

Risk: The skill gives command examples for local media tooling, so unsupported formats or missing tools can cause failed conversions.

Mitigation: Verify required tools are installed and inspect the command parameters before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are examples for local tools such as ffmpeg, sips, ImageMagick, gifsicle, pngquant, and optipng; users should review filenames and overwrite behavior before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
