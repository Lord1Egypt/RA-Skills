## Description:

Converts user-provided 2D images with labeled dimensions into precise SVG plans and STL models for engineering plotting and 3D printing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auto-dog](https://clawhub.ai/user/auto-dog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert dimensioned part images into reviewed SVG profiles and STL model outputs for 3D printing or machining workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is a template rather than a finished automatic image-to-STL converter, so incorrect geometry could produce an unusable part.

Mitigation: Review dimensions and require user confirmation of the SVG profile before editing the 3D model script or exporting STL output.

Risk: Dependency installation and task-specific script edits can affect the user's workspace if run without isolation.

Mitigation: Use an isolated virtual environment, pin reviewed dependency versions where possible, and copy the template script into the project workspace before modifying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/auto-dog/skills/image-to-3d-model)
- [README.md](artifact/README.md)
- [README_zh.md](artifact/README_zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python code edits and generated SVG/STL files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation of the SVG profile before STL generation; task-specific geometry is adapted from the template.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
