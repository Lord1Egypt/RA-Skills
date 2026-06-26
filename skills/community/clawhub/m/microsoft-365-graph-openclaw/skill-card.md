## Description: <br>
Microsoft 365 Graph for OpenClaw manages Outlook mail, calendar, OneDrive, contacts, and push-based webhook wake signals via Microsoft Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[draeden79](https://clawhub.ai/user/draeden79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect self-hosted OpenClaw workflows to Microsoft 365 Graph for Outlook mail, calendar, OneDrive, contacts, and push-based mail wake signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Microsoft Graph permissions can grant read/write access to mail, files, calendar, and contacts. <br>
Mitigation: Use the smallest documented permission profile that fits the workflow and prefer a Microsoft app registration controlled by the deploying organization. <br>
Risk: OAuth tokens, webhook tokens, clientState values, logs, and service environment files can expose account or hook access if mishandled. <br>
Mitigation: Store secrets in protected host-managed locations, keep token-bearing state files out of version control, and rotate credentials if logs, shell history, or screenshots may have exposed them. <br>
Risk: Privileged setup scripts can write system configuration and enable services when run without dry-run mode. <br>
Mitigation: Review dry-run output before using sudo, validate changes on a non-production host first, and apply to production only after approval. <br>
Risk: File-sharing operations can create exposure if anonymous sharing is used unintentionally. <br>
Mitigation: Avoid anonymous sharing unless it is explicitly required and approved for the deployment. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/draeden79/microsoft-365-graph-openclaw) <br>
- [Project Homepage](https://github.com/draeden79/microsoft-365-graph-openclaw) <br>
- [Auth Reference](references/auth.md) <br>
- [Mail Reference](references/mail.md) <br>
- [Calendar Reference](references/calendar.md) <br>
- [OneDrive Reference](references/drive.md) <br>
- [Contacts Reference](references/contacts.md) <br>
- [Mail Webhook Adapter Reference](references/mail_webhook_adapter.md) <br>
- [Architecture](docs/architecture.md) <br>
- [Permission Profiles](docs/permission-profiles.md) <br>
- [Minimal Setup](docs/minimal-setup.md) <br>
- [App Registration](docs/app-registration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and script-based workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Microsoft Graph and OpenClaw setup guidance; included scripts may perform API calls, write local state files, and configure services when executed by the user.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
