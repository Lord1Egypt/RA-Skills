## Description: <br>
Generate Chinese official government documents formatted to GB/T 9704-2012 standards, including document numbers, titles, body text, attachments, signatures, contacts, and page numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxue1985122219](https://clawhub.ai/user/zhangxue1985122219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, public-sector document authors, and agent developers use this skill to produce standardized Chinese official documents such as notices, requests, reports, and letters. It provides formatting guidance and a Python document-generation script for creating .docx files aligned with GB/T 9704-2012. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the generator with the default output path can overwrite an existing document. <br>
Mitigation: Review CONFIG["outputFile"] before execution and write to a new path when preserving existing files matters. <br>
Risk: Contact details or official information included in CONFIG and CONTENTS will be written into the generated .docx file. <br>
Mitigation: Include only information intended for the final document and review the generated file before sharing. <br>
Risk: The script depends on a local python-docx installation and document rendering may vary by local Word fonts. <br>
Mitigation: Install dependencies in a virtual environment and confirm required Chinese fonts are available where the document is opened. <br>


## Reference(s): <br>
- [GB/T 9704-2012 reference](artifact/references/gbt9704-2012.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhangxue1985122219/official-document) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python configuration snippets and shell commands; generated .docx files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python execution with python-docx; users should review outputFile before running to avoid overwriting an important document.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
