## Description: <br>
Atomic node skill to draft an email via Gmail using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Gmail draft messages through a local gog CLI while leaving review and sending to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts may be created through an untrusted gog CLI or in a Gmail account the user did not intend to use. <br>
Mitigation: Install only if the local gog CLI is trusted and connected to the intended Gmail account. <br>
Risk: Email recipients or draft content may include sensitive or incorrect information. <br>
Mitigation: Review recipients and message content before asking an agent to create drafts, especially for sensitive or confidential material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-draft-email) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text] <br>
**Output Format:** [Shell command that returns a JSON confirmation and a short text status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates Gmail drafts through the local gog CLI; it does not send email.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
