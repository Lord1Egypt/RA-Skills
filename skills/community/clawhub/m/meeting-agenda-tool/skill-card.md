## Description: <br>
Generates standardized Chinese government or enterprise meeting agendas from structured meeting details as Word and PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ywwzzsgit](https://clawhub.ai/user/ywwzzsgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and administrative staff use this skill to turn meeting titles, times, locations, agenda items, hosts, and participant lists into formatted Chinese meeting agenda documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python packages from a package index before generating documents. <br>
Mitigation: Preinstall trusted dependencies in the execution environment and review dependency sources before use. <br>
Risk: The skill writes agenda files locally and may invoke Office or LibreOffice tooling for PDF conversion. <br>
Mitigation: Use a dedicated output folder, review generated filenames and paths, and handle sensitive meeting information according to organizational policy. <br>


## Reference(s): <br>
- [Meeting agenda template specification](references/template.md) <br>
- [ClawHub skill page](https://clawhub.ai/ywwzzsgit/meeting-agenda-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Word document and PDF files generated from JSON meeting data, with brief text status and file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces .docx and .pdf agenda files; PDF output may depend on local Office or LibreOffice conversion support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
