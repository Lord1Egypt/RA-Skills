## Description:

Gmail: Forward a message to new recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to have an agent draft or run Gmail forwarding commands for a selected message, including recipients, optional body text, CC/BCC fields, drafts, and attachment handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may be forwarded to unintended recipients if address lists are not reviewed.

Mitigation: Verify all --to, --cc, and --bcc values before sending, and use --draft or --dry-run for sensitive messages.

Risk: Original attachments are included by default and may expose sensitive files.

Mitigation: Review attachment handling before forwarding and use --no-original-attachments when original files should not be included.

Risk: The command may use a different Gmail sender account or alias than intended.

Mitigation: Confirm the configured gws Gmail account and set --from explicitly when a send-as address is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-forward)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)
- [gws shared auth and global flags](../gws-shared/SKILL.md)
- [gws Gmail commands](../gws-gmail/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and command-option guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and a Gmail account configured for the intended sender.]

## Skill Version(s):

1.0.14 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
