## Description:

GitHub 通知自动分拣 triages GitHub notification emails by forwarding urgent failures and security alerts, buffering review and merge items for a daily summary, and silently archiving low-priority messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devincodel](https://clawhub.ai/user/devincodel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to route GitHub notification emails from a dedicated sub-mailbox into urgent forwards, daily-summary buffer entries, or read archives. It is intended for GitHub notifications, not non-GitHub email handling or manual email composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured mail-cli profile can read, send, and mark messages in the GitHub sub-mailbox.

Mitigation: Install only when that mailbox authority is acceptable, review credential scope before deployment, and pin @clawemail/mail-cli where possible.

Risk: Urgent forwards and daily summaries may expose full urgent-message bodies or repository metadata to the resolved main email address.

Mitigation: Review the forwarding and summary formats before use, and adjust the workflow if full bodies or repository metadata should not be forwarded or stored.

## Reference(s):

- [GitHub Triage Rules](references/triage-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/devincodel/skills/github-triage)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with bash commands, JSON examples, and email summary formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mail-cli actions to forward urgent messages, buffer daily-summary metadata, and mark low-priority messages as read.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
