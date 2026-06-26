## Description: <br>
Execute email operations with platform-specific optimizations and secure credential handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to help an agent read, search, filter, draft, and send email through Apple Mail SQLite access or the himalaya IMAP/SMTP CLI while preserving review before outbound mail is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent access a configured mailbox and prepare outbound messages. <br>
Mitigation: Review every email before approving send, and require explicit confirmation before syncing, moving, deleting, sending, or bulk-processing mail. <br>
Risk: Mailbox credentials and mail transport configuration are sensitive. <br>
Mitigation: Use revocable app passwords or OAuth where possible, store secrets in the configured credential manager, and install himalaya from a trusted source. <br>


## Reference(s): <br>
- [ClawHub Mail skill page](https://clawhub.ai/ivangdavila/mail) <br>
- [Apple Mail SQLite Queries](apple-mail.md) <br>
- [himalaya CLI Patterns](himalaya.md) <br>
- [Email Send Protocol](sending.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include email drafts, search guidance, command examples, and configuration instructions; sending requires explicit user review and confirmation.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
