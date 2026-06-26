## Description: <br>
Download Gmail attachments through IMAP into a local folder with sender, subject, date, extension, and limit filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whauff](https://clawhub.ai/user/whauff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who need local copies of Gmail attachments use this skill to collect invoices, statements, receipts, or other files without configuring Google Cloud APIs. It supports filtered batch downloads, dry-run previews, and duplicate-safe local filenames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gmail app password and reads mailbox contents through IMAP. <br>
Mitigation: Use a dedicated Gmail app password, avoid pasting it where it may be logged, and confirm IMAP access is intended before running. <br>
Risk: The skill saves email attachments to the local filesystem, which can place untrusted files on the machine. <br>
Mitigation: Use dry-run first, apply narrow sender, date, and file-type filters, choose a dedicated download folder, and review attachments before opening them. <br>


## Reference(s): <br>
- [Gmail Setup](references/setup.md) <br>
- [Downloader Script](scripts/download_gmail_attachments.py) <br>
- [Gmail IMAP Settings](https://mail.google.com/mail/#settings/fwdandpop) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; local attachment files and an optional JSON summary from the downloader script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode can preview matches without writing files; normal runs save matching attachments to a user-selected local folder.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
