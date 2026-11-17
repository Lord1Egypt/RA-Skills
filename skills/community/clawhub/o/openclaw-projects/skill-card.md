## Description:

Builds coordinated multi-agent Project setups in OpenClaw for teams that need shared workflows, task-manager coordination, queue-based handoffs, and project configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent operators use this skill to set up coordinated multi-agent project teams, including team interviews, project rulebooks, shared workspace files, task-manager workflow wiring, queue-based communication, heartbeat behavior, and safety handoff steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes agent behavior and OpenClaw configuration for coordinated projects.

Mitigation: Use it with a trusted operator, take recovery snapshots before setup, and review generated project rules and configuration changes before relying on them.

Risk: Documented shell and path setup examples may be unsafe if user-provided project IDs, repository names, or folder names are substituted without validation.

Mitigation: Strictly validate every project ID, repository name, folder name, and path before running setup commands or writing project files.

Risk: Task-manager integration depends on separately installed Asana or ClickUp skills and their credentials.

Mitigation: Confirm each participating agent has the required dependency skill installed and stores credentials through the user's secret management system before project setup.

## Reference(s):

- [OpenClaw Projects skill page](https://clawhub.ai/encryptshawn/skills/openclaw-projects)
- [Project Files Reference](references/project-files.md)
- [Workflow Reference](references/workflow.md)
- [Interview Question Banks](references/interview-questions.md)
- [Team Archetypes](references/team-archetypes.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, Markdown file templates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project setup instructions and generated coordination file content for OpenClaw agent teams.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
