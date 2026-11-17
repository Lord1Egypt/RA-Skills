## Description:

Generate PPT documents using Python and python-pptx. No third-party API calls, fully open source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangzhanyou](https://clawhub.ai/user/xiangzhanyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate PowerPoint presentations locally from a title and structured slide content with optional bullet lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a PowerPoint file to the path provided by the user or agent.

Mitigation: Choose an intended output path before execution and review the resulting file location after generation.

Risk: Generated presentation content may be inaccurate, incomplete, or unsuitable for external sharing.

Mitigation: Review the generated slides before distributing the presentation outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiangzhanyou/skills/openclaw-ppt-generator)

## Skill Output:

**Output Type(s):** [files, json, shell commands, guidance]

**Output Format:** [PowerPoint .pptx file with a JSON status response containing the generated file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated locally with python-pptx from user-provided title, slide content, and optional output path.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
