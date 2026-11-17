## Description:

Kanban Workflow is a TypeScript skill for a stage-based agentic co-worker that integrates PM platforms via CLI-first adapters (CLIs or small wrapper scripts).

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonvanlaak](https://clawhub.ai/user/simonvanlaak)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to let an agent inspect, select, update, and transition project-management work items across GitHub, Planka, Plane, and Linear using a shared stage model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill acts with the same privileges as the selected authenticated project-management CLI or token.

Mitigation: Use least-privilege accounts or scoped tokens and review the selected adapter's permissions before running workflow commands.

Risk: Scheduled autopilot execution can repeatedly change stages or post comments without an interactive review step.

Mitigation: Run manual commands first and enable --autopilot-install-cron only after confirming the scope, stage mappings, and account permissions.

Risk: Task titles, bodies, comments, and workspace identifiers may appear in command output, logs, or config metadata.

Mitigation: Treat config/kanban-workflow.json and command logs as sensitive workspace metadata.

Risk: Linear usage depends on an API-key wrapper and server-side query handling identified as under-scoped by the security evidence.

Mitigation: Audit dependencies and harden or review the Linear wrapper before using the skill in sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonvanlaak/skills/kanban-workflow-export)
- [Adapter notes](src/adapters/README.md)
- [Architecture review](references/ARCH_REVIEW.md)
- [Requirements](references/REQUIREMENTS.md)
- [Technical plan](references/TECH_PLAN.md)
- [GitHub CLI](https://cli.github.com/)
- [Planka CLI](https://github.com/voydz/planka-cli)
- [Plane](https://github.com/makeplane/plane)
- [Linear GraphQL API](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text guidance with CLI commands, JSON configuration examples, and code-oriented workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of config/kanban-workflow.json and may drive comments or stage changes through authenticated PM platform CLIs when commands are executed.]

## Skill Version(s):

0.1.4 (source: package.json, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
