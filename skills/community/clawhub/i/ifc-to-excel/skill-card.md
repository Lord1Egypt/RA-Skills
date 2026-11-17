## Description:

Convert IFC files (2x3, 4x1, 4x3) to Excel databases using IfcExporter CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, BIM engineers, and construction data teams use this skill to convert IFC model files into Excel workbooks for validation, quantity takeoff, reporting, and downstream analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires filesystem access to read IFC models and write converted output files.

Mitigation: Grant access only to intended model and output folders, and use a trusted IfcExporter or IfcOpenShell installation.

Risk: Generated spreadsheets may expose detailed building or project metadata.

Mitigation: Review generated Excel files before sharing and apply the same access controls used for the source BIM models.

## Reference(s):

- [Ifc To Excel on ClawHub](https://clawhub.ai/datadrivenconstruction/skills/ifc-to-excel)
- [buildingSMART Industry Foundation Classes](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce instructions for filesystem reads of IFC files and writes of Excel or Collada outputs.]

## Skill Version(s):

2.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
