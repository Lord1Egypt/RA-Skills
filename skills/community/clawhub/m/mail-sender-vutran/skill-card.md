## Description: <br>
Sends emails via SMTP with a custom recipient, subject, and body using user-provided SMTP configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaskies](https://clawhub.ai/user/Jaskies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to send a plain-text email through an SMTP provider configured by environment variables or command-line arguments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMTP credentials are required to send mail and could be exposed if hardcoded or shared in conversation history. <br>
Mitigation: Use environment variables or command-line arguments only for the intended task, prefer provider app passwords, and avoid storing SMTP secrets in skill files or conversation history. <br>
Risk: The skill sends real email through the configured SMTP account, so mistaken recipients or message bodies can leave the user's environment. <br>
Mitigation: Review the recipient, subject, and body before execution and grant credentials only when sending mail is the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jaskies/mail-sender-vutran) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text script status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMTP server, port, username, password, sender, recipient, subject, and body.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
