## Description:

Read and manage email via IMAP (ProtonMail Bridge, Gmail, etc.). Check for new/unread messages, fetch content, search mailboxes, and mark as read/unread. Works with any IMAP server including ProtonMail Bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvarrieur](https://clawhub.ai/user/mvarrieur)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let an agent check, search, fetch, and update IMAP mailboxes such as ProtonMail Bridge, Gmail, or other standard IMAP accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IMAP credentials can be exposed if local environment files are mishandled.

Mitigation: Store credentials in a secure secret store or a chmod 600 ignored .env file, and confirm credential files are never committed.

Risk: Remote IMAP access without TLS or with certificate validation disabled can expose credentials and message contents.

Mitigation: Use TLS for remote IMAP servers and disable certificate validation only for a verified local ProtonMail Bridge setup.

Risk: The scheduled email-summary example contains a hard-coded iMessage destination.

Mitigation: Replace the phone number with a confirmed recipient or remove the scheduled delivery example before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvarrieur/skills/imap-email)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from CLI commands with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMAP credentials in environment variables and network access to the configured IMAP server.]

## Skill Version(s):

1.0.3 (source: server release and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
