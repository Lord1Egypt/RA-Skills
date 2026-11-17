## Description:

Resizes images to specific dimensions with support for custom sizes, batch resizing, aspect ratio preservation, presets, and local Pillow-based processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to resize individual images or batches of images to exact dimensions, preset social-media/document sizes, or proportional widths and heights while preserving image quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Pillow for image processing.

Mitigation: Install dependencies in a virtual environment when possible and pin Pillow to a reviewed version.

Risk: Batch resizing creates output files for every supported image in the selected input directory.

Mitigation: Run batch operations only on directories intentionally chosen by the user and confirm the output directory before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/image-size-resizer)
- [Publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline Python and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create resized image files in user-selected output paths or directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
