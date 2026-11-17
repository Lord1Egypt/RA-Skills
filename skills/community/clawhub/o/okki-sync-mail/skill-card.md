## Description:

Okki Sync Mail helps an agent read, search, manage, draft, and send email over IMAP/SMTP while syncing inbound and outbound activity into OKKI CRM follow-up records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate an IMAP/SMTP mailbox, preview and send email with approval controls, manage folders and messages, and sync customer communication records into OKKI CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive mailbox and customer communication data.

Mitigation: Use a dedicated low-privilege mailbox, avoid sensitive customer mail until disclosure and consent requirements are satisfied, and restrict allowed read and write directories.

Risk: The security summary reports under-disclosed external AI and Discord flows.

Mitigation: Review configuration and data flows before installation, and disclose or disable external processing paths that are not acceptable for the deployment.

Risk: The security guidance identifies unsafe shell-command construction paths.

Mitigation: Fix command construction before running automated email capture or other unattended workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/okki-sync-mail)
- [README](artifact/README.md)
- [Integration guide](artifact/INTEGRATION.md)
- [Workflow test report](artifact/WORKFLOW_TEST_REPORT.md)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces email and CRM workflow guidance; actual mailbox and CRM effects depend on configured credentials, approval flags, and runtime commands.]

## Skill Version(s):

2.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
