## Description: <br>
Process Excel and PDF files - extract data, parse tables, generate reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to process spreadsheet and PDF inputs, extract tabular or textual data, and generate report-ready outputs such as CSV files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Excel conversion script can overwrite the selected CSV output path. <br>
Mitigation: Check the output destination before running the script and keep backups for files that must not be replaced. <br>
Risk: Local document processing may expose file contents to the active agent workflow. <br>
Mitigation: Use the skill only on files the user intends to process and avoid running it on unrelated sensitive documents. <br>
Risk: Dependency installation can introduce package supply-chain risk. <br>
Mitigation: Install the listed dependencies in a virtual environment from a trusted package index. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laimiaohua/gi-excel-pdf-process) <br>
- [Publisher profile](https://clawhub.ai/user/laimiaohua) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text, files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; scripts produce CSV files or printed text/table output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file processing with pandas, openpyxl, and pdfplumber dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
