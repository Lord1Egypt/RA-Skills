## Description: <br>
Pans Excel helps agents create, analyze, clean, visualize, convert, and export Excel workbooks through a local Python command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to generate Excel workbooks, reports, charts, formulas, validations, data cleaning steps, and CSV/JSON/PDF conversions for tabular data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports an unsafe data parser that can execute Python code from crafted command input. <br>
Mitigation: Review or patch scripts/excel.py before installing by removing the eval() fallback and accepting only strict JSON or safe literal parsing with validation. <br>
Risk: Some commands modify the original workbook or write output files. <br>
Mitigation: Use copies of important spreadsheets, avoid untrusted --data values, and check output paths before running commands. <br>


## Reference(s): <br>
- [Pans Excel on ClawHub](https://clawhub.ai/dashiming/pans-excel) <br>
- [Publisher profile: dashiming](https://clawhub.ai/user/dashiming) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated spreadsheet files from the tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local Excel, CSV, JSON, and PDF files depending on the selected command.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
