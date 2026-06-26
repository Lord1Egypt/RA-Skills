## Description: <br>
Ollie File Processor helps an agent batch rename local files and convert common image, PDF, DOCX, and Markdown formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollielin](https://clawhub.ai/user/ollielin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to prepare or reorganize local file sets, including batch filename changes and format conversions for images, PDFs, DOCX files, and Markdown documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk renaming and conversion operations can change local files. <br>
Mitigation: Use dry-run mode before execution, review the preview, and back up important files. <br>
Risk: Format conversion requires optional third-party Python packages and, for some PDF workflows, external system dependencies. <br>
Mitigation: Install only the dependencies required for the intended conversion in a virtual environment from trusted package sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ollielin/ollie-file-processor) <br>
- [Poppler Windows Releases](https://github.com/oschwartz10612/poppler-windows/releases/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, rename, or convert local files when the referenced scripts are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
