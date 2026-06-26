## Description: <br>
MoltMail gives agents a wallet-backed email account for setup, login, mailbox reading, sending, replies, aliases, referral codes, and EMC balance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tempepeot](https://clawhub.ai/user/tempepeot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent a MoltMail/EtherMail inbox, manage wallet-backed setup, read and search messages, send or reply to email, manage aliases, and check referral or EMC reward information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet setup, private keys, passphrases, and local auth state. <br>
Mitigation: Use a dedicated wallet for MoltMail, keep the passphrase private, and protect the ./state directory that stores encrypted wallet configuration and tokens. <br>
Risk: Sending or replying to email can communicate externally and may involve payment-related or interactive message flows. <br>
Mitigation: Confirm recipient, sender alias, subject, body, and any payment or interactive context with the user before sending or acting. <br>
Risk: Fetching full email content marks messages as read. <br>
Mitigation: Confirm before reading messages that should remain unread, and tell the user when a read action will change message state. <br>
Risk: All mailbox operations use the MoltMail/EtherMail remote service. <br>
Mitigation: Install and use the skill only when the user intends to trust that service for a wallet-backed inbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tempepeot/moltmailermp) <br>
- [MoltMail homepage](https://moltmail.io) <br>
- [EtherMail homepage](https://ethermail.io) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown or text responses with npm command invocations and JSON results from local scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm, local state files for encrypted wallet configuration and auth tokens, optional ETHERMAIL_PASSPHRASE, and calls to the MoltMail/EtherMail remote service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
