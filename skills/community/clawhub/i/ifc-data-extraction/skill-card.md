## Description:

Extract structured data from IFC (Industry Foundation Classes) files using IfcOpenShell. Parse BIM models, extract quantities, properties, spatial relationships, and export to various formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, BIM engineers, and construction data teams use this skill to parse IFC models, extract element properties, quantities, spatial relationships, materials, and export structured BIM data for reporting or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BIM model exports can contain sensitive building layouts, project metadata, and material details.

Mitigation: Review export destinations and sharing permissions before writing files, SQL tables, or shared-folder outputs.

Risk: Large IFC models can consume significant memory when processed all at once.

Mitigation: Process large models by entity type or scoped query to reduce memory pressure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/ifc-data-extraction)
- [IfcOpenShell](https://ifcopenshell.org)
- [IFC Standard](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/)
- [Data Driven Construction](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with Python code examples and structured extraction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local exports to Excel, CSV, JSON, pandas DataFrames, or SQL databases depending on user request.]

## Skill Version(s):

2.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
