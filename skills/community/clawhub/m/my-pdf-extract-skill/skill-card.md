## Description: <br>
Extracts product code, name, batch, and quantity data from text-based PDF label files and prepares structured Excel output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangshouxin](https://clawhub.ai/user/zhangshouxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can use this skill to extract structured product label records from text-searchable PDFs, handle multi-line product names, validate extracted rows, and export the result to Excel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extraction workflow expects text-searchable PDFs and may miss or misread data in scanned files or unfamiliar layouts. <br>
Mitigation: Test on representative PDFs first and review the generated Excel rows before relying on the output. <br>
Risk: The workflow reads a configured local PDF path and writes a configured Excel output file. <br>
Mitigation: Use an appropriate working directory and confirm file paths before granting local file access or write permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangshouxin/my-pdf-extract-skill) <br>
- [Publisher profile](https://clawhub.ai/user/zhangshouxin) <br>
- [pdfplumber documentation](https://github.com/jsvine/pdfplumber) <br>
- [pandas documentation](https://pandas.pydata.org/) <br>
- [OpenClaw skill development guide](https://docs.openclaw.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an Excel workbook when the described extraction script is run against a configured PDF input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
