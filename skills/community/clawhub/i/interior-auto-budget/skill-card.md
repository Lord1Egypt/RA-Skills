## Description:

Generates editable interior design budget spreadsheets from DXF floor-plan data and a local pricing library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior designers and budget preparers use this skill to turn CAD-exported DXF floor plans into Excel budget drafts for residential or commercial interior projects. It helps preserve a local pricing system while reducing manual line-item setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pricing library path is hardcoded for the original author's local environment.

Mitigation: Confirm and update the local pricing-library path before running the script.

Risk: Automatically estimated areas, quantities, and budget totals may be inaccurate for a specific project.

Mitigation: Review the generated workbook and adjust quantities and prices before sharing it with a client.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/137984917-cyber/skills/interior-auto-budget)
- [Publisher profile](https://clawhub.ai/user/137984917-cyber)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided DXF file and a local pricing JSON library, then writes an editable XLSX budget file.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
