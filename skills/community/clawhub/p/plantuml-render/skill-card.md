## Description:

Render PlantUML diagrams using the PlantUML JAR. Use this skill to generate PNG/SVG/PDF images from PlantUML source code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafeimao-gjf](https://clawhub.ai/user/jiafeimao-gjf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn PlantUML source files into diagram assets for documentation or agent-authored Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Java process with a PlantUML JAR and writes rendered diagram files.

Mitigation: Use a trusted PlantUML JAR, review the PlantUML source before rendering, and run the skill only in a workspace where local file creation is expected.

Risk: The published artifact has setup quality issues, including reliance on a local JAR that may be missing.

Mitigation: Confirm Java and the PlantUML JAR are installed in the expected script directory before relying on the skill in a workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Guidance]

**Output Format:** [PNG, SVG, or PDF diagram files with optional Markdown image links and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Java and a trusted PlantUML JAR located beside the Python script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
