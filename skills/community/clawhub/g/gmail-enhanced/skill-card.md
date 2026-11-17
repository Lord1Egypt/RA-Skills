## Description:

Enhanced Gmail integration with advanced features including label management, attachment handling, advanced search, email parsing, and automated email processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use Gmail Enhanced to interact with Gmail accounts for search, labels, attachments, message parsing, sending, and rule-based processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Gmail scopes that can read, send, modify messages, and manage labels.

Mitigation: Use a dedicated Google OAuth client and grant only the Gmail scopes required for the intended workflow.

Risk: OAuth credential and token files are persisted on disk.

Mitigation: Store credential and token files outside shared folders and repositories with file permissions limited to the local user.

Risk: Attachment downloads can write mailbox-provided filenames to local paths.

Mitigation: Add filename validation, overwrite protection, and a trusted download directory before enabling attachment downloads.

Risk: Auto-reply and message-processing rules can send or modify email based on mailbox input.

Mitigation: Require confirmation, narrow search queries, and rate limits before running automated reply or bulk-processing rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/skills/gmail-enhanced)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Cloud Console](https://console.cloud.google.com)
- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Gmail API workflow guidance and Python client usage examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
