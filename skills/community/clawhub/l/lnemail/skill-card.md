## Description: <br>
Sets up and uses anonymous email accounts on LNemail.net with Bitcoin Lightning payments for agent workflows that need email reception, notifications, or communication without KYC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnemail](https://clawhub.ai/user/lnemail) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use LNemail to create paid anonymous email accounts, receive plain-text messages such as 2FA codes or notifications, and send email through the LNemail API with Lightning payment confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party anonymous email provider and may handle sensitive email content or account tokens. <br>
Mitigation: Use only for approved workflows, store access tokens in a protected secret location, and keep tokens out of logs and prompts. <br>
Risk: Sending email and account setup require Bitcoin Lightning payments. <br>
Mitigation: Confirm the recipient, message content, invoice, and payment amount before authorizing any Lightning payment. <br>
Risk: Anonymous email may be inappropriate for sensitive, regulated, or identity-bound communications. <br>
Mitigation: Avoid sensitive or regulated email unless the organization has explicitly approved this provider and use case. <br>


## Reference(s): <br>
- [LNemail](https://lnemail.net) <br>
- [ClawHub LNemail skill page](https://clawhub.ai/lnemail/lnemail) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, and API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for using a third-party email service; generated outputs may include commands that call LNemail.net APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
