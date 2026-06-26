## Description: <br>
Convert IFC files (2x3, 4x1, 4x3) to Excel databases using IfcExporter CLI. Extract BIM data, properties, and geometry without proprietary software. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, BIM engineers, and construction data teams use this skill to convert IFC models into Excel workbooks and optional Collada geometry for validation, quantity takeoff, material schedules, and analytics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs filesystem access to read IFC files and write conversion outputs. <br>
Mitigation: Run it only on folders and model files the user chooses, and review generated Excel or geometry files before sharing them. <br>
Risk: The workflow depends on a local IfcExporter or IfcOpenShell installation. <br>
Mitigation: Use a trusted converter installation and verify converter and input paths before running single-file or batch jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/ifc-to-excel) <br>
- [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto) <br>
- [buildingSMART Industry Foundation Classes](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of Excel workbooks and Collada geometry files from user-selected IFC files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
