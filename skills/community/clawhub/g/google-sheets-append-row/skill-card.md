## Description: <br>
Atomic node skill to append a row in Google Sheets using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to append a single row of values to a specified Google Sheets range through the gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can append data to a Google Sheet through the local CLI. <br>
Mitigation: Use a limited Google account or service account and confirm the spreadsheet ID, range, and row values before allowing the command to run. <br>
Risk: Incorrect spreadsheet ranges or values could add data to the wrong location. <br>
Mitigation: Review the generated gog command and target range before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-sheets-append-row) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with an inline shell command example and JSON confirmation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog CLI and a valid spreadsheet ID, range, and row values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
