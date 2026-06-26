## Description: <br>
Validates daily market_data.json files with market-data quality checks and returns a pass or reject result with issue reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szrw1825](https://clawhub.ai/user/szrw1825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data operations teams use this skill to validate daily market_data.json files before downstream financial reporting, analysis, or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically email validation failures using hard-coded SMTP settings and a source-code credential. <br>
Mitigation: Remove or replace the hard-coded SMTP credential and recipient, make alerts explicitly opt-in, and confirm mail settings before installing or running the skill. <br>
Risk: The skill uses fixed local paths for market-data files, imports, and logs. <br>
Mitigation: Review and update file paths and logging locations for the target environment before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text validation report and CheckResult-style pass/fail issue list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write logs and, when configured in the artifact, send alert email on repeated failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
