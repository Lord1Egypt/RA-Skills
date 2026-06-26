## Description: <br>
Generate polished, read-only business reports from CSV/XLSX into static XLSX, PDF, and PPTX deliverables using ReportStudio Community. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xutianliang77-create](https://clawhub.ai/user/xutianliang77-create) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn local CSV/XLSX data and natural language reporting requests into monthly, weekly, or daily business report deliverables with data-supported trends and breakdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes a local ReportStudio Python package on user-selected spreadsheet files. <br>
Mitigation: Install and run it only in an environment where the local ReportStudio package is trusted. <br>
Risk: Incorrect paths, output locations, or column names can produce failed or misleading report runs. <br>
Mitigation: Use the provided wrapper or structured command arguments, quote paths and column names, and keep inputs and outputs in intended directories. <br>
Risk: Generated reports can include warnings for insufficient history, truncation, or unrecognized fields. <br>
Mitigation: Review the returned warnings before sharing XLSX, PDF, or PPTX outputs. <br>


## Reference(s): <br>
- [Acceptance Checklist](references/acceptance.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xutianliang77-create/openclaw-reportstudio-community) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary with ReportStudio JSON and generated XLSX, PDF, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow; generated warnings and artifact paths are returned for acceptance checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
