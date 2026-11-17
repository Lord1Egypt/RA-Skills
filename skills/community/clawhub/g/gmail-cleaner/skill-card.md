## Description:

Gmail Cleaner helps agents scan, bulk clean, organize, filter, and restore messages across one or more Gmail accounts using Gmail API scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cedarscy](https://clawhub.ai/user/cedarscy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide Gmail mailbox cleanup tasks such as scanning senders, trashing matched messages, organizing labels and filters, and restoring messages from trash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful Gmail modify, delete, and settings access.

Mitigation: Use it only with Gmail accounts where that access is acceptable, choose the minimum needed scope, and revoke OAuth tokens when finished.

Risk: Bulk delete and trash-purge operations can cause irreversible mailbox data loss.

Mitigation: Run scan and dry-run modes first, review each query or sender list, and use --skip-trash-purge unless permanent deletion is intentional.

Risk: OAuth token pickle files can grant access to another person's mailbox if shared or reused.

Mitigation: Keep token files local and protected, never use tokens from another person, and remove or revoke tokens after use.

Risk: The scripts may auto-install unpinned Python dependencies.

Mitigation: Prefer installing reviewed, pinned dependencies manually in an isolated environment before running the scripts.

## Reference(s):

- [Gmail API modify OAuth scope](https://www.googleapis.com/auth/gmail.modify)
- [Gmail API readonly OAuth scope](https://www.googleapis.com/auth/gmail.readonly)
- [Gmail API settings OAuth scope](https://www.googleapis.com/auth/gmail.settings.basic)
- [Gmail API labels OAuth scope](https://www.googleapis.com/auth/gmail.labels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose mailbox-modifying operations that should be reviewed and dry-run before execution.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
