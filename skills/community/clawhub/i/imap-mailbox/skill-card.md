## Description: <br>
Read and manage emails via IMAP protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shimonxin](https://clawhub.ai/user/shimonxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to inspect an IMAP mailbox, search messages, read email content, download attachments, and generate daily email digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private email content and attachments. <br>
Mitigation: Use a low-risk mailbox or app-specific credential and confirm mailbox reads or downloads before running commands. <br>
Risk: TLS certificate verification is weakened. <br>
Mitigation: Prefer a revised version that verifies TLS certificates before use with sensitive mailboxes. <br>
Risk: Email digests, attachments, message text, and mailbox state may be saved locally. <br>
Mitigation: Choose or disable local storage locations and avoid opening downloaded attachments directly. <br>
Risk: Some dependency sources are resolved over HTTP. <br>
Mitigation: Prefer HTTPS dependency sources and review dependencies before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shimonxin/imap-mailbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown, terminal text, local files, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local digest, attachment, message text, and mailbox state files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
