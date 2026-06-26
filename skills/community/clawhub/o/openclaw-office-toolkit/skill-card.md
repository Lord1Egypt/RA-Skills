## Description: <br>
Helps agents read, create, edit, and validate Word, Excel, PowerPoint, and PDF documents using local Office and PDF tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect, generate, modify, and validate common Office and PDF files in local workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process local Office and PDF files, including untrusted documents. <br>
Mitigation: Use a sandbox or controlled environment for untrusted files and review generated file changes before relying on them. <br>
Risk: Dependency metadata is incomplete for required local tools and Python libraries. <br>
Mitigation: Verify python-docx, openpyxl, python-pptx, pypdf, pandoc, and LibreOffice or soffice are installed before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/axelhu/openclaw-office-toolkit) <br>
- [Publisher Profile](https://clawhub.ai/user/axelhu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or editing of local .docx, .xlsx, .csv, .pptx, and .pdf files when the required local tools are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
