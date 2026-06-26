## Description: <br>
Reviews data sharing catalog materials for field completeness, special rule compliance, platform consistency, and actionable issue-list output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Github7265](https://clawhub.ai/user/Github7265) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Catalog reviewers and data governance teams use this skill to audit submitted data sharing forms, compare material content with platform catalog state, and produce traceable remediation lists for each reviewed system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit reports or structured extracts may contain sensitive submitted material, and an unsafe output directory could overwrite important files. <br>
Mitigation: Confirm the output directory before running the script and keep generated reports in a private location when submissions contain sensitive data. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/Github7265/material-review) <br>
- [Field completeness checklist](references/field-completeness.md) <br>
- [Special field rules](references/special-field-rules.md) <br>
- [Platform consistency checks](references/platform-consistency.md) <br>
- [Issue list template](references/issue-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional JSON and Markdown report files from the audit script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script can extract structured data from submitted DOCX materials and write structured_data.json, issues.json, and audit_report.md to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
