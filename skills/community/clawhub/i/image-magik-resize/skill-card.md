## Description:

Resize images using ImageMagick (CLI). Entrypoint is a Bash script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pr1vateer](https://clawhub.ai/user/pr1vateer)

### License/Terms of Use:


## Use Case:

Developers and users invoke this skill to resize local image files with ImageMagick from an agent-accessible command, using dimensions, percentages, or conditional geometry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ImageMagick runs on local image files and writes to a user-selected or default output path, which can create directories or overwrite files within the user's permissions.

Mitigation: Use trusted local inputs, avoid filenames that begin with '-', and confirm the destination path before running the resize command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pr1vateer/skills/image-magik-resize)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Command output text and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and either magick or convert from ImageMagick; output path is user-selected or defaults next to the input image.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
