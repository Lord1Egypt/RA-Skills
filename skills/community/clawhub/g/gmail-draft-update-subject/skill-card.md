## Description: <br>
Atomic node skill to update the subject of an existing Gmail draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a Gmail draft already exists and only its subject line needs to be set or updated through the configured native CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the subject of an existing Gmail draft through the user's configured Gmail CLI. <br>
Mitigation: Confirm gog is trusted, authenticated to the intended Gmail account, and only granted access where changing that draft is acceptable. <br>
Risk: The command may target the wrong draft ID or use an unintended subject if parameters are supplied incorrectly. <br>
Mitigation: Check the JSON response after execution and retry or fail rather than proceeding without confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-draft-update-subject) <br>
- [Publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the configured gog CLI and returns confirmation from the Gmail draft update command.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
