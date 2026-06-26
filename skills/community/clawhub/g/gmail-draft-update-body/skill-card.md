## Description: <br>
Atomic node skill to update the body text of an existing Gmail draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when they need to update only the body text of an existing Gmail draft through the local Gmail CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill updates an existing Gmail draft body and may replace text in the wrong draft or account if inputs are incorrect. <br>
Mitigation: Confirm the target draft ID, Gmail account, and final body text before execution, then review the draft before any separate send action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-draft-update-body) <br>
- [Publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON confirmation from the Gmail CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog CLI and a valid target Gmail draft ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
