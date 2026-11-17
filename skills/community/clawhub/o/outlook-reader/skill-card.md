## Description:

Connects to Outlook on Windows to search mail by subject keywords and download matching attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[die0921](https://clawhub.ai/user/die0921)

### License/Terms of Use:

MIT-0

## Use Case:

Outlook users and automation developers use this skill to find mailbox messages such as billing emails and retrieve their attachments with Python-based Outlook automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive mailbox messages and attachments may be accessed or downloaded with too little user control.

Mitigation: Run only against intentionally selected mailboxes and folders, list matching messages before downloading, and validate sender and attachment type.

Risk: Attachment filenames or ZIP extraction may create unsafe or unexpected local files.

Mitigation: Sanitize filenames, restrict writes to an approved save directory, and avoid ZIP extraction unless a controlled privacy and security process is in place.

Risk: Automatically forwarding matched mail to an AI assistant could expose private mailbox content.

Mitigation: Do not enable automatic forwarding unless the user has explicit authorization and a documented data-handling process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/die0921/skills/outlook-reader)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code blocks and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts may download Outlook attachments to a local directory when run by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
