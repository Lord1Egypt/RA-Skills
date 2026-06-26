## Description: <br>
Formats uploaded Word documents into Chinese official-document layouts with template selection, GB/T 9704-2012 styling, official title and header fonts, and Times New Roman for Western text and numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Erich1566](https://clawhub.ai/user/Erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and document-preparation staff use this skill to convert DOCX drafts into Chinese official-document formats, optionally applying a named template, document number, and issuing organization header. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The formatter reads user-supplied DOCX files and optional local templates, so untrusted or unintended files could be processed. <br>
Mitigation: Use trusted DOCX files and templates, and keep inputs in a controlled workspace. <br>
Risk: The skill writes to a caller-provided output path, which could overwrite an important document if pointed at the wrong location. <br>
Mitigation: Direct outputs to a controlled workspace and review the destination path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Erich1566/official-layout-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Configuration, Guidance] <br>
**Output Format:** [Formatted DOCX file with a status object containing the output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python-docx, user-supplied DOCX input and output paths, optional DOCX templates, and the expected local fonts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
