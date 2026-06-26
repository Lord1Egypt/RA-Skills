## Description: <br>
Generate Office files with a bundled Python engine. Use when creating or exporting Word (.docx), Excel (.xlsx), or PowerPoint (.pptx) files from structured JSON, reports, meeting minutes, project plans, trackers, business briefs, or natural-language requirements that must be turned into Office documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujohn74](https://clawhub.ai/user/lujohn74) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured JSON or natural-language office-document requirements into Word, Excel, or PowerPoint files through a bundled Python generator. It is suited for reports, meeting minutes, project plans, trackers, and business briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup step installs third-party Python Office-generation libraries. <br>
Mitigation: Install in a normal non-privileged environment and proceed only if the dependency installation is acceptable for the workspace. <br>
Risk: Generated files are written to user-selected output paths and may embed local image files referenced by the request. <br>
Mitigation: Choose output paths deliberately and include only image files intended to be embedded in the generated document. <br>
Risk: The wrapper can run an alternate Python binary through OFFICE_GENERATOR_PYTHON. <br>
Mitigation: Set OFFICE_GENERATOR_PYTHON only to a trusted Python binary. <br>


## Reference(s): <br>
- [Input formats](references/input-formats.md) <br>
- [ClawHub skill release](https://clawhub.ai/lujohn74/office-generator-py) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Office document files (.docx, .xlsx, .pptx), stdout file paths, and JSON request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written to caller-selected output paths; standard mode accepts full JSON requests and business mode accepts built-in template kinds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
