## Description: <br>
Extract structured data from IFC (Industry Foundation Classes) BIM models using IfcOpenShell, including quantities, properties, spatial relationships, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, BIM engineers, and construction data teams use this skill to parse IFC files, extract project metadata, building elements, quantities, property sets, spatial hierarchy, materials, and relationships, then export the results for analysis and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide exports of IFC-derived data to arbitrary SQL database targets, including table replacement behavior. <br>
Mitigation: Prefer local CSV, Excel, JSON, pandas, or local SQLite outputs unless database credentials and table replacement are explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/ifc-data-extraction) <br>
- [IfcOpenShell](https://ifcopenshell.org) <br>
- [buildingSMART IFC standard](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/) <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and structured export recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local exports to pandas DataFrames, Excel, CSV, JSON, and optional SQL database tables.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
