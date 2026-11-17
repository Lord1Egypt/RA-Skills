## Description:

Download Gmail attachments through IMAP when the user wants to pull invoices, statements, or other files from Gmail into a local folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whauff](https://clawhub.ai/user/whauff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to download Gmail attachments into a local folder with sender, subject, date, extension, and result-limit filters. It is suited for invoice, statement, receipt, and similar attachment export workflows that do not require Google Cloud APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gmail app passwords grant mailbox access and may be exposed through command history or process listings if passed as command-line arguments.

Mitigation: Use a dedicated Gmail app password, prefer environment variables or a safer secret mechanism instead of `--gmail-pass`, and revoke the app password when the task is complete.

Risk: The skill writes email attachments to the local filesystem, which can place sensitive files in an unintended or shared location.

Mitigation: Choose a private destination folder explicitly, run `--dry-run` before downloading, and review the final save path in the summary.

Risk: Broad filters can download more messages or attachment types than intended.

Mitigation: Use sender, subject, date, extension, and `--max-results` filters to limit the mailbox search before running a full download.

## Reference(s):

- [Gmail Setup](references/setup.md)
- [Downloader Script](scripts/download_gmail_attachments.py)
- [Gmail IMAP Settings](https://mail.google.com/mail/#settings/fwdandpop)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; downloaded attachment files and optional JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes matched attachments to a local folder and can emit a JSON summary when requested.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
