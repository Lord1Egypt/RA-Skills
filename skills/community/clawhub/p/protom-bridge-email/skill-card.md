## Description: <br>
Send email through Proton Mail Bridge (localhost SMTP) using age-encrypted credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boilerrat](https://clawhub.ai/user/boilerrat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure a local Proton Mail Bridge mailbox for agent email workflows and to send automated reports, alerts, or test messages through that local SMTP bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent use Proton Bridge credentials and send email through the user's account. <br>
Mitigation: Install it only when agent email sending is intended, keep the age identity private, and use confirmation or recipient allowlists for automated messages. <br>
Risk: Temporary plaintext environment files can expose Proton Bridge credentials before encryption. <br>
Mitigation: Delete the temporary plaintext env file after encryption and store the Bridge credentials only in the age-encrypted file. <br>
Risk: SMTP misconfiguration could route messages outside the intended local Proton Bridge service. <br>
Mitigation: Keep SMTP_HOST set to localhost or 127.0.0.1 and review configuration before enabling automated sending. <br>


## Reference(s): <br>
- [Proton Mail Bridge setup](references/proton-bridge-setup.md) <br>
- [Proton Mail Bridge](https://proton.me/mail/bridge) <br>
- [ClawHub release page](https://clawhub.ai/boilerrat/protom-bridge-email) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with shell command examples and plaintext email body inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends email through a local Proton Bridge SMTP service when the bridge and age-encrypted credentials are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
