## Description:

Create parametric 3D-printable parts and enclosures with CadQuery, export STL or 3MF files, render review previews, and iterate on fit, tolerances, and printability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniosilveira](https://clawhub.ai/user/antoniosilveira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and makers use this skill to guide agents through requirement gathering, parametric CadQuery modeling, STL or 3MF export, preview rendering, and printability review for functional 3D-printed parts such as brackets, mounts, adapters, and enclosures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include a micromamba bootstrap flow that may fetch and execute remote installation code.

Mitigation: Review and replace the micromamba install path with a verified package-manager or checksum-validated installation flow before deployment.

Risk: CadQuery model files are executable Python and can run arbitrary code when passed to the model runner.

Mitigation: Run only generated or trusted model scripts, preferably inside a disposable virtual environment or container without secrets or broad filesystem access.

## Reference(s):

- [Design Review](references/design-review.md)
- [Python Requirements](references/requirements.txt)
- [OpenClaw 3D Printing Skill on ClawHub](https://clawhub.ai/antoniosilveira/skills/openclaw-3d-printing-skill)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline Python and shell code blocks plus generated STL, 3MF, and PNG file paths when helper scripts are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses millimeters for model dimensions and returns concise print settings, fit warnings, and support or orientation guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
