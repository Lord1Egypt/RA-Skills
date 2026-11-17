## Description:

Generates Rhino 7 Grasshopper (.ghx) XML files from natural language descriptions or images for parametric concept design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elliotbian](https://clawhub.ai/user/elliotbian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and computational design users use this skill to create Rhino 7 Grasshopper definitions with native components, GhPython scripts, sliders, and wiring from natural language or image descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .ghx files can contain GhPython source that runs inside Rhino/Grasshopper.

Mitigation: Inspect any embedded GhPython source before opening generated .ghx files in Rhino/Grasshopper.

Risk: The generator can overwrite local files at the selected output path.

Mitigation: Choose a safe output directory and avoid paths that point to existing or important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elliotbian/skills/grasshopper-generator)
- [README](README.md)
- [Component GUID database](references/component_guids.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python snippets and generated .ghx XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .ghx files to user-selected paths and embed GhPython source.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
