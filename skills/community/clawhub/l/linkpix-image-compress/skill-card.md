## Description:

Helps an agent compress and convert local image files with ImageMagick or ffmpeg, including batch processing and JPG, PNG, and WebP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content operators use this skill when they need an agent to reduce local image file size, meet upload limits, batch-compress images, or convert images to WebP while reporting before-and-after file sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image compression or conversion commands may modify the wrong files, write to an unintended location, or use an unsuitable target size or quality.

Mitigation: Confirm the input files, output directory, target size or quality, and any ImageMagick installation step before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-image-compress)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise file-size summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent should confirm input files, output directory, target size or quality, and any ImageMagick installation step before running commands.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
