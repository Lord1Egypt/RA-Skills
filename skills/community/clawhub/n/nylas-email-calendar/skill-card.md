## Description:

Email, calendar, and contacts via the Nylas API across Gmail, Outlook, Exchange, Yahoo, iCloud, and IMAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mqasimca](https://clawhub.ai/user/mqasimca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and operate Nylas-powered email, calendar, and contact workflows from an agent, including message search, email sending, scheduling, and contact lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected Nylas grants may allow the agent to read email, contacts, and calendars.

Mitigation: Use appropriately scoped Nylas grants and limit connected accounts to the workflows the agent needs.

Risk: Email sending, event updates, and calendar deletion can perform real external actions.

Mitigation: Confirm sensitive send, update, or delete requests before running them.

## Reference(s):

- [Nylas Dashboard](https://dashboard-v3.nylas.com)
- [Installation Guide](https://cli.nylas.com/guides/install-openclaw-nylas-plugin)
- [npm Package](https://www.npmjs.com/package/@nylas/openclaw-nylas-plugin)
- [Nylas CLI](https://cli.nylas.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands and tool usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NYLAS_API_KEY and connected Nylas grants; actions may read account data or modify email and calendar state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
