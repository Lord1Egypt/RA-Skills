## Description: <br>
Safely reads, writes, cleans, transforms, filters, sorts, and merges local Excel and CSV data without arbitrary code execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data operators use this skill to automate local spreadsheet ETL tasks such as reading Excel or CSV files, cleaning rows, transforming column types, filtering and sorting data, and writing merged outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dependency lockfile uses plain HTTP mirror URLs despite documentation claiming official HTTPS npm sources. <br>
Mitigation: Regenerate and review the lockfile from an official HTTPS npm registry before installing or deploying the release. <br>
Risk: Spreadsheet write and merge functions can create or overwrite files at caller-supplied local paths. <br>
Mitigation: Run the skill only on intended paths, use backups for important spreadsheets, and restrict write locations in automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-etl-handle-safe) <br>
- [Publisher profile](https://clawhub.ai/user/43622283) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Text] <br>
**Output Format:** [JavaScript function results and local Excel/CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes caller-supplied local file paths; no model invocation is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence, skill.yaml, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
