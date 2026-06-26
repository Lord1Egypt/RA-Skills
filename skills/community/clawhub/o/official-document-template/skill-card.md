## Description: <br>
Converts Markdown official-document content into Word documents formatted to GB/T 9704-2012 for notices, requests, reports, replies, opinions, and related document types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunkguo](https://clawhub.ai/user/hunkguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to draft or convert Chinese official-document Markdown into consistently formatted Word documents. It is intended for document preparation workflows that need GB/T 9704-2012 layout, fonts, margins, line spacing, and title hierarchy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter writes a DOCX file to the selected output path. <br>
Mitigation: Choose the output path deliberately and avoid paths that would overwrite an existing document. <br>
Risk: Document appearance depends on local Python dependencies and Chinese fonts being installed. <br>
Mitigation: Install python-docx and the required fonts before conversion, then review the generated DOCX in Word or WPS. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/hunkguo/official-document-template) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Official document formatting specification notes](artifact/公文排版规范.md) <br>
- [Template usage guide](artifact/模板使用指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the converter produces DOCX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Markdown input and an output path selected by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
