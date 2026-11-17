## Description:

Explain how email and Google Calendar work for OpenClaw agents, including the distinction between agent email and owner email, how gog and the Google Workspace skill are used, where related credentials/config live, and how to troubleshoot common setup or access issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to explain Gmail and Google Calendar account boundaries, configure gog-based access, and troubleshoot common owner-calendar sharing and OAuth setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance can lead users to authorize broad owner Google Workspace access beyond the immediate email or calendar task.

Mitigation: Authorize only the services needed for the current task, prefer a separate agent account with shared resources, avoid granting Drive, Docs, Sheets, or Contacts unless required, and revoke unused Google permissions afterward.

Risk: The skill references credential and auth-profile file paths that may contain sensitive Google OAuth or account data.

Mitigation: Treat the paths as locations only and do not print or paste credential file contents into chat or logs.

## Reference(s):

- [Google Calendar](https://calendar.google.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides explanatory setup and troubleshooting guidance; does not directly access Google services.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
