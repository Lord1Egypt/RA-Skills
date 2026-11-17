## Description:

Resize images using ImageMagick (CLI). Entrypoint is a Bash script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pr1vateer](https://clawhub.ai/user/pr1vateer)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to resize local image files from the command line with ImageMagick, including fixed geometry, percent scaling, and default output-path generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create output directories and write image files at user-provided paths, which can replace an existing file if paths collide.

Mitigation: Use a distinct output directory or filename and review input, geometry, and output arguments before running the resize command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pr1vateer/skills/image-resize)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [Image files plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the resized image to a requested or inferred output path.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
