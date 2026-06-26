## Description: <br>
Analyzes any CSV file and returns row count, column names, and basic statistics for numeric columns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leotrieu](https://clawhub.ai/user/leotrieu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users can invoke this skill to inspect a local CSV file and summarize its shape, columns, and numeric statistics without modifying the source file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python helper on a user-selected CSV file. <br>
Mitigation: Use it only with CSV files intended for analysis, and review the file path before execution. <br>
Risk: The pandas dependency is requested at runtime and is not pinned in the artifact. <br>
Mitigation: Use a controlled environment or pin pandas before deployment when reproducibility or dependency review is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leotrieu/leo-csv-stats-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Readable Markdown summary of CSV row count, column names, and numeric min, max, and average values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads one user-selected local CSV path and leaves the original CSV file unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
