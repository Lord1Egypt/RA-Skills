## Description: <br>
Professional DOCX/PPTX document editing with tracked changes, formatting preservation, highlights, strikethrough, and Git version control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TsukiSama9292](https://clawhub.ai/user/TsukiSama9292) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external collaborators, developers, and document reviewers use this skill to fetch DOCX or PPTX files, apply structured edits, preserve common formatting, generate review artifacts, and manage edited document versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local files, download documents from arbitrary URLs, use SFTP/SSH, upload edited documents, and write Git commits. <br>
Mitigation: Use explicit local copies, avoid sensitive documents unless the scripts have been reviewed, and review generated files and commits before sharing or retaining them. <br>
Risk: The PPTX slide rearrange feature can damage presentations. <br>
Mitigation: Do not use PPTX slide rearrangement as written; keep backups and review edited presentations manually in PowerPoint or another trusted editor. <br>
Risk: Document editing may preserve only common formatting and can miss exact-match table replacements. <br>
Mitigation: Preview document text before creating edit rules, use exact search strings, and manually inspect the edited output before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TsukiSama9292/office-document-editor) <br>
- [Publisher profile](https://clawhub.ai/user/TsukiSama9292) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Edited DOCX/PPTX files, Markdown diff reports, JSON edit rules, and shell command workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown conversions, timestamped edited documents, diff reports, and Git commits when the workflow script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
