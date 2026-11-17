## Description:

Apply video filters - scale, crop, watermark, speed, blur, and visual effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video engineers use this skill to choose FFmpeg commands for resizing, cropping, watermarking, speed changes, blur, brightness, rotation, filter chaining, and fade effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example FFmpeg commands write output files and could overwrite important media if users choose an existing filename.

Mitigation: Confirm input files and choose output filenames that will not overwrite important media before running commands.

Risk: Commands require a local FFmpeg installation and may fail or behave differently if FFmpeg is missing or incompatible.

Mitigation: Confirm FFmpeg is installed and available in the execution environment before using the examples.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples assume FFmpeg is installed and that users select input and output filenames appropriate for their media.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
