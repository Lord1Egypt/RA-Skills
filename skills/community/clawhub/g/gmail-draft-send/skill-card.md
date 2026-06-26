## Description: <br>
Atomic node skill to send an existing Gmail draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send a specific existing Gmail draft through the local gog CLI and receive JSON confirmation that the send completed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to send Gmail drafts through the local gog CLI. <br>
Mitigation: Before use, verify the gog binary and Gmail account, and require confirmation of the exact draft ID, recipients, subject, and final body before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-draft-send) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON] <br>
**Output Format:** [JSON confirmation returned after executing a Gmail draft send command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog binary and an existing Gmail draft ID; retries failed attempts up to three times.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
