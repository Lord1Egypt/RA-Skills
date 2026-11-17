## Description:

Combines GIFs and videos into vertical or grid composites with ffmpeg. Use for multi-part tutorial media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical authors use the skill to combine GIFs, videos, and images into media compositions for tutorials and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that some examples concatenate media sequentially instead of producing the described vertical or grid layout.

Mitigation: Check that the selected example matches the intended layout, then inspect the resulting composition before using it.

Risk: The security review reports that FFmpeg examples can silently overwrite existing output files.

Mitigation: Choose a new output path or confirm and back up any existing file before running an example.

Risk: The security review was partial because several referenced paths were missing, so its evidence is incomplete.

Mitigation: Review the referenced components and their commands before installing or running the skill.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scry-media-composition)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [Composed GIF or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Combines multiple media inputs; reports output dimensions and file size.]

## Skill Version(s):

1.10.3 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
