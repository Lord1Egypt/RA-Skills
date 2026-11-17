## Description:

Comprehensive email management skill for fetching, searching, reading, sending, replying to, moving, deleting, marking, and summarizing email across IMAP/SMTP accounts with a local SQLite index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgwanai](https://clawhub.ai/user/lgwanai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to manage email through a local CLI: fetch and index messages, search and read them, generate Markdown summaries, and perform account actions such as sending, moving, marking, deleting, and exporting email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores email content, attachments, and account-derived data locally.

Mitigation: Use a dedicated mail account or app password and restrict filesystem permissions on the mail_data directory.

Risk: The skill supports high-impact actions such as sending, deleting, moving, exporting, and marking email.

Mitigation: Avoid autonomous send, delete, move, or export actions; require user review before executing account-changing commands.

Risk: The security review reports unsafe file handling around fetched attachments.

Mitigation: Do not fetch or open untrusted attachments until filename containment is fixed.

Risk: Summaries can expose sensitive authentication content such as verification codes.

Mitigation: Treat summary output as sensitive and avoid sharing verification-code reports outside the trusted local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgwanai/skills/mail-skills)
- [README](README.md)
- [Skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local email data, attachment files, SQLite indexes, exported files, and outbound email messages when the user authorizes those workflows.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
