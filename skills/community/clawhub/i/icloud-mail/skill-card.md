## Description:

An iCloud Mail integration for reading, searching, sending, and managing email, drafts, threads, and folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maton](https://clawhub.ai/user/maton)

### License/Terms of Use:

MIT-0

## Use Case:

People using iCloud Mail use this skill to find and read messages, manage drafts and folders, and send or reply to email. It can also support user-approved email automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting exposes the selected mailbox to the skill's account and its enabled workflows.

Mitigation: Confirm the mailbox being connected, use an account with only the necessary connections for hosted code, and revoke unused app-specific passwords and connections.

Risk: Sending, editing, moving, or deleting email can have consequential or irreversible effects.

Mitigation: Review recipients and message content before sending, inspect the target before changes or deletions, and check the mailbox before retrying a write whose outcome is uncertain.

Risk: Automations can run repeatedly and deliver mailbox data to configured destinations.

Mitigation: Review each function, trigger, and destination; grant only necessary connections; resolve the documented network-policy incompatibility before enabling automation; and remove unused automations.

Risk: Mail access depends on a local bridge, and hosted environments may not support the required network path.

Mitigation: Use a trusted local computer for the bridge and verify the documented network requirements before relying on mail commands or automation.

## Reference(s):

- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Apple: app-specific passwords](https://support.apple.com/en-us/102654)
- [Apple: iCloud Mail server settings](https://support.apple.com/en-us/102525)
- [RFC 3501: IMAP4rev1](https://www.rfc-editor.org/rfc/rfc3501)
- [RFC 5321: SMTP](https://www.rfc-editor.org/rfc/rfc5321)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Natural-language email content and results, Markdown summaries, and optional command or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and list by default; confirm mailbox changes, sends, connections, and automations before proceeding.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
