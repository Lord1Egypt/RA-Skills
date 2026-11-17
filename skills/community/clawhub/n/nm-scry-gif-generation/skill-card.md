## Description:

Converts webm/mp4 video files to optimized GIFs via ffmpeg with configurable quality settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert screen recordings or other supported video files into shareable GIFs with configurable size and quality settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose installing ffmpeg as a system package dependency.

Mitigation: Treat any ffmpeg installation command as a separate user-approved system package action.

Risk: GIF conversion writes an output file path selected during the workflow.

Mitigation: Review the output path before running conversions and verify the generated file after completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scry-gif-generation)
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and conversion presets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for validating input videos, checking ffmpeg, running GIF conversions, and verifying output files.]

## Skill Version(s):

1.9.19 (source: server release evidence; artifact frontmatter lists 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
