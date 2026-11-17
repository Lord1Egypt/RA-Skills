## Description:

Microsoft 365 Graph for OpenClaw with webhook-based wake signals. Reduce recurring LLM cost from inbox polling while managing Outlook mail, calendar, OneDrive, and contacts via Microsoft Graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[draeden79](https://clawhub.ai/user/draeden79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect self-hosted OpenClaw deployments to Microsoft 365 workflows. It supports OAuth-based mail, calendar, OneDrive, contacts, and push-based mail wake signals through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Microsoft 365 permissions can allow broad read/write access to mail, calendar, contacts, and OneDrive for the authenticated account.

Mitigation: Grant only the permission profile required for the intended workflow, prefer a tenant-owned app registration for production, and revoke or rotate OAuth grants if credentials may be exposed.

Risk: Privileged setup scripts can write service configuration and manage host services.

Mitigation: Review sudo scripts before use, run dry-run modes first, and deploy initially on a non-production host.

Risk: Webhook tokens, Graph clientState values, OAuth tokens, logs, or shell history may expose credentials.

Mitigation: Store secrets in protected host-managed files, restrict token file permissions, keep token-bearing state out of source control, and rotate exposed tokens immediately.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/draeden79/skills/microsoft-365-graph-openclaw)
- [Project Homepage](https://github.com/draeden79/microsoft-365-graph-openclaw)
- [Auth Reference](references/auth.md)
- [Mail Reference](references/mail.md)
- [Calendar Reference](references/calendar.md)
- [OneDrive Reference](references/drive.md)
- [Contacts Reference](references/contacts.md)
- [Mail Webhook Adapter Reference](references/mail_webhook_adapter.md)
- [Architecture](docs/architecture.md)
- [Minimal Setup](docs/minimal-setup.md)
- [Permission Profiles](docs/permission-profiles.md)
- [Microsoft Device Code OAuth Documentation](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Microsoft Graph API workflow guidance and local setup commands for self-hosted OpenClaw deployments.]

## Skill Version(s):

0.2.2 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
