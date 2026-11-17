## Description:

Syncs IMAP mailbox messages from one or more accounts into local Markdown files organized by account and date for email analysis, knowledge-base building, and AI summarization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettersao](https://clawhub.ai/user/bettersao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to copy IMAP email into local Markdown files for downstream analysis, AI-generated summaries, mail monitoring, and local knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox contents are copied into local plaintext Markdown files.

Mitigation: Use the skill only with mailboxes intended for local copying, restrict local file permissions, and consider disk encryption.

Risk: IMAP credentials are stored in config.json.

Mitigation: Use app-specific, revocable passwords and keep config.json out of version control.

Risk: The runner installs dependencies at execution time.

Mitigation: Pin or preinstall reviewed dependencies before deployment instead of relying on the bundled run script as written.

Risk: Account names influence local output paths.

Mitigation: Use simple account names containing only letters, digits, and hyphens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettersao/skills/mail-imap-sync)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration]

**Output Format:** [Local Markdown email files plus console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes messages under an emails directory grouped by account and date; state.json tracks incremental IMAP UID progress.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
