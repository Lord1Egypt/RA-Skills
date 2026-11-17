## Description:

Manage Plutio projects and tasks through the Plutio REST API, including listing projects and people, querying tasks, creating tasks, and updating or closing task details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grewingm](https://clawhub.ai/user/grewingm)

### License/Terms of Use:


## Use Case:

Developers and operations users use this skill to integrate an agent with Plutio workspaces for project lookup, task triage, task creation, and task status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived Plutio API credentials and local access tokens.

Mitigation: Use the narrowest Plutio API application permissions available, avoid putting secrets in chat history, shell profiles, or command history, prefer an OS credential store or password manager, and rotate exposed credentials.

Risk: Commands can read or change sensitive workspace data, including projects, tasks, assignees, people, due dates, and status.

Mitigation: Treat command output as sensitive business data and require explicit confirmation before bulk updates, closures, or direct API deletion.

Risk: Task creation and update behavior depends on Plutio API limitations, including required board and group IDs for visible tasks.

Mitigation: Confirm task board and group IDs in Plutio before creating tasks and verify important changes in the Plutio UI.

## Reference(s):

- [Plutio Skill Setup Guide](references/setup-guide.md)
- [Plutio API Endpoints Reference](references/api-endpoints.md)
- [Plutio Integration Examples](references/examples.md)
- [Plutio PowerShell 7 Workflows](references/powershell-workflows.md)
- [Plutio](https://plutio.com/)
- [ClawHub Plutio Skill Page](https://clawhub.ai/grewingm/skills/plutio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash, PowerShell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable CLI commands and API request/response examples that use Plutio workspace credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
