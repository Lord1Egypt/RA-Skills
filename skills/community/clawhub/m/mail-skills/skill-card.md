## Description: <br>
Comprehensive email management skill. Use this skill when the user wants to fetch, search, read, send, reply to, move, delete, mark, or summarize emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgwanai](https://clawhub.ai/user/lgwanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent manage email through local IMAP/SMTP workflows, including fetching, searching, reading, summarizing, sending, moving, deleting, marking, and exporting email data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and store full mailbox contents locally. <br>
Mitigation: Use an app-specific mail password, protect or encrypt the mail_data directory, and install only when mailbox access is acceptable. <br>
Risk: The skill can change mailbox state by sending, deleting, moving, marking, and exporting messages. <br>
Mitigation: Require manual approval before send, delete, move, mark, and export actions. <br>
Risk: Broad fetches and untrusted attachments can expose sensitive content or unsafe files. <br>
Mitigation: Avoid broad fetches, patch attachment filename handling, and redact verification codes before fetching untrusted mail. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lgwanai/mail-skills) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown summaries, command-line instructions, local email files, SQLite records, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, write, export, and modify mailbox state through configured local mail accounts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
