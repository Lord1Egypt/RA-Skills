## Description: <br>
Google Sheets: Append a row to a spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to append one or more rows to a Google Sheets spreadsheet through the gws CLI after confirming the target spreadsheet, range, and values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports a write operation that can append incorrect or unintended data to a Google Sheets spreadsheet. <br>
Mitigation: Confirm the target spreadsheet, sheet range, and row values with the user before execution. <br>
Risk: The skill depends on shared gws authentication guidance that is not included in this artifact. <br>
Mitigation: Install and review the referenced gws-shared authentication guidance before using the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-sheets-append) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for appending rows with the gws CLI; execution should be confirmed before any write.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
