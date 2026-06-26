## Description: <br>
Atomic node skill to delete an email via Gmail using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user has identified a Gmail message that should be moved to trash through the gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent could move the wrong Gmail message to trash if the target message is ambiguous. <br>
Mitigation: Before running the Gmail trash command, show the sender, subject, date, and message ID, then confirm the exact message with the user. <br>
Risk: A Gmail trash command can fail or return an error after execution is attempted. <br>
Mitigation: Check for successful confirmation, retry failed delete commands up to three times with a short wait, then report the error and stop if deletion still fails. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Text with an inline shell command and confirmation status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and a Gmail message ID.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
