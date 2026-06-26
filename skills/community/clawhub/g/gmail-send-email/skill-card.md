## Description: <br>
Atomic node skill to send an email via Gmail using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compose and send Gmail messages through the configured gog CLI when an email needs to be sent to one or more recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email from the configured Gmail account, including to unintended recipients or with sensitive content. <br>
Mitigation: Before each send, verify the recipient list, subject, body, and authorization to share any sensitive information. <br>
Risk: The skill depends on the gog CLI and the Gmail account configuration available to the agent. <br>
Mitigation: Install only if you trust the gog CLI and intend the agent to send email from that configured account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-send-email) <br>
- [Publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Confirmation text from the gog CLI after attempting to send the email] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and a configured Gmail account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
