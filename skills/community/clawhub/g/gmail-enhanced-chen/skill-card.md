## Description:

Enhanced Gmail integration with advanced features including label management, attachment handling, advanced search, email parsing, and automated email processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email automation users use this skill to integrate with Gmail for advanced search, label management, attachment handling, parsing, sending, and automated email processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Gmail permissions that allow reading, sending, labeling, and modifying mailbox data.

Mitigation: Install only when those permissions are acceptable; use a dedicated Google OAuth client and the least-privilege account available.

Risk: Credential and token files can expose mailbox access if they are not protected.

Mitigation: Keep credential and token files private and restrict filesystem access to them.

Risk: Saved automation rules can modify messages or send replies beyond the user's intent.

Mitigation: Review and limit saved rules before running process_rules().

Risk: Bulk attachment downloads may mishandle filenames or overwrite files.

Mitigation: Avoid bulk attachment downloads until filename sanitization and overwrite protections are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/skills/gmail-enhanced-chen)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [Google Cloud Console](https://console.cloud.google.com)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Google OAuth credential and token file paths.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
