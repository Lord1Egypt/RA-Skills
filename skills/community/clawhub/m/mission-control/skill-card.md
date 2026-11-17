## Description:

Kanban-style task management dashboard for AI assistants. Manage tasks via CLI or dashboard UI. Use when user mentions tasks, kanban, task board, mission control, or wants to track work items with status columns (backlog, in progress, review, done).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdsthomas](https://clawhub.ai/user/rdsthomas)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams using AI assistants use Mission Control to set up and operate a task board where human-authored work items can be prioritized, tracked, and handed to an agent for execution. The skill guides setup of the dashboard, webhook transform, GitHub integration, and CLI task updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions can cause an agent to perform powerful local or repository actions when moved into an active work state.

Mitigation: Use Mission Control with a private, trusted-user repository, review tasks before execution, and keep the agent constrained by sandbox and permission policies.

Risk: The skill relies on GitHub, gateway, webhook, and optional CORS-proxy access paths that can expose sensitive task data or control surfaces if broadly reachable.

Mitigation: Prefer fine-grained single-repository GitHub tokens, require signed webhooks with a configured secret, avoid storing gateway tokens in the browser when possible, and restrict gateway or proxy exposure with authentication and origin controls.

Risk: The server security review marked the release suspicious because it handles GitHub and local-agent access that users should inspect before installing.

Mitigation: Review the release before installation and deploy only in a tightly restricted agent environment aligned with the server-provided security guidance.

## Reference(s):

- [Mission Control README](README.md)
- [Mission Control Skill Reference](SKILL.md)
- [How Mission Control Works](docs/HOW-IT-WORKS.md)
- [Prerequisites](docs/PREREQUISITES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Gateway Setup Guide](docs/gateway-setup.md)
- [Configuration Reference](assets/examples/CONFIG-REFERENCE.md)
- [Mission Control Homepage](https://github.com/rdsthomas/mission-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workspace files, dashboard assets, webhook transform setup, and task status updates when used by an agent.]

## Skill Version(s):

2.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
