## Description:

Manage Microsoft 365 task workflows by using Microsoft Graph CRUD operations for Microsoft To Do tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT

## Use Case:

Employees, operators, and developers use this skill to create, list, update, and delete Microsoft To Do tasks with clear task names, owners, due dates, and status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests delegated Microsoft Graph permissions including Tasks.ReadWrite, User.Read, and offline_access.

Mitigation: Use a tenant and app registration you control, and grant only the documented delegated permissions needed for Microsoft To Do CRUD.

Risk: Reusable login tokens are cached in a local file.

Mitigation: Set M365_TOKEN_CACHE_PATH to a private user-owned location and restrict local file access to that account.

Risk: The tasks:delete command deletes live Microsoft To Do tasks without a confirmation step.

Mitigation: Treat delete operations as destructive, verify the target list and task ID before execution, and prefer list or update commands when reviewing task state.

Risk: The artifact text mentions Planner and reminders, but security evidence says to expect Microsoft To Do CRUD rather than Planner automation or reminders.

Mitigation: Scope usage and review to Microsoft To Do task CRUD behavior unless separate evidence validates Planner or reminder automation.

## Reference(s):

- [M365 Task Manager Playbook](artifact/references/playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/abdelkrim/skills/openclaw-skill-m365-task-manager-by-altf1be)
- [Project Homepage](https://github.com/ALT-F1-OpenClaw/openclaw-skill-m365-task-manager)
- [Microsoft Graph API Endpoint](https://graph.microsoft.com/v1.0)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires M365_TENANT_ID and M365_CLIENT_ID; optionally uses M365_TOKEN_CACHE_PATH for local token cache location.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
