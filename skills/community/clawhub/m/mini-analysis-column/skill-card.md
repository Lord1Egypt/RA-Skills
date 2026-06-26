## Description: <br>
Analyzes a numeric column in a CSV file and reports its maximum, minimum, and average values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdmseven](https://clawhub.ai/user/fdmseven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run a local helper script that summarizes a single numeric CSV column. It is suited for quick inspection of values such as scores or metrics when the CSV has headers and pandas is installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debug mode can print the CSV shape and first rows, which may expose sensitive data in logs or terminal history. <br>
Mitigation: Avoid debug mode on sensitive CSV files and review terminal output before sharing logs. <br>
Risk: The skill may activate on broad CSV review wording even when the user does not intend to run local analysis. <br>
Mitigation: Confirm the target file path and numeric column before executing the helper script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fdmseven/mini-analysis-column) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with setup and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports rounded maximum, minimum, and mean values for one numeric column.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
