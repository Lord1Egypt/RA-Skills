## Description: <br>
Reads, searches, and manages email via IMAP and sends email via SMTP, including mailbox checks, message fetch and search, read/unread updates, and attachments across common mail providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apple133junjiang-a11y](https://clawhub.ai/user/apple133junjiang-a11y) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can configure this skill to let an agent check, search, fetch, and update mailbox messages over IMAP and send email over SMTP. It is intended for accounts where the user deliberately grants the agent mail access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real authority to read mailbox contents, change read/unread state, download attachments, and send email. <br>
Mitigation: Install only for an intended mailbox, use a dedicated or least-privilege account with an app password or authorization code, and review recipients, message bodies, attachments, and mailbox mutation commands before execution. <br>
Risk: Credential and TLS settings can weaken account security if secrets are mishandled or certificate verification is disabled. <br>
Mitigation: Keep credentials out of shared logs and repositories, rotate app passwords when needed, and keep IMAP_REJECT_UNAUTHORIZED and SMTP_REJECT_UNAUTHORIZED enabled except for a reviewed test environment. <br>
Risk: Attachment download behavior writes email-provided filenames into a selected local directory. <br>
Mitigation: Download only to a restricted safe directory, inspect files before opening or forwarding them, and avoid untrusted attachment filenames until filename and path handling is hardened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apple133junjiang-a11y/imap-smtp-email-chinese) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/apple133junjiang-a11y) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; invoked scripts return JSON or console text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose mailbox content, message metadata, attachment files, or SMTP delivery metadata depending on the invoked command.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence; package.json and _meta.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
