## Description:

Natural language task and project management that captures tasks from conversation, organizes them into projects, tracks progress, and serves a local Kanban dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bparticle](https://clawhub.ai/user/bparticle)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn natural conversation into local Markdown task and project records, maintain project status, and view work through a local Kanban dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated task data may be exposed if the dashboard is bound to a LAN address or shared through a public tunnel.

Mitigation: Keep the dashboard bound to localhost for normal use, and use trusted access controls before enabling network access, public tunnels, static hosting, or persistent services for sensitive data.

Risk: The skill writes local task and project Markdown in the configured planner workspace.

Mitigation: Install only if local planner file writes are acceptable, choose the workspace path deliberately, and keep backups or version control for important task data.

Risk: Setup, dashboard exposure, or persistence workflows may propose shell commands, including sudo commands.

Mitigation: Review all shell and sudo commands before execution, especially commands that expose the dashboard or create persistent services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bparticle/skills/natural-language-planner)
- [README](artifact/README.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [License](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command snippets, plus local Markdown task and project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or manage a local dashboard and write task, project, index, configuration, and attachment files in the configured planner workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
