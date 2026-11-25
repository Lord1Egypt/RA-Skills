## Description:

Combines GIFs and videos into vertical or grid composites with ffmpeg. Use for multi-part tutorial media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to combine generated terminal, browser, image, GIF, or video assets into a composite for tutorials and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output files may replace files already at the chosen paths, and sequential concatenation may differ from the intended layout.

Mitigation: Review output paths and confirm the selected composition behavior before running.

Risk: Security scan coverage was partial because several referenced paths or files could not be resolved.

Mitigation: Check referenced files and relevant commands before use.

## Reference(s):

- [Plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scry)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [GIF or video composite files with a brief text report of file size and dimensions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Composition layout and options are specified in a manifest.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
