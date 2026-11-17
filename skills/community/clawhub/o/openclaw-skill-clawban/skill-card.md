## Description:

Kanban Workflow is a TypeScript skill for a stage-based agentic co-worker that integrates project-management platforms through CLI-first adapters and provides setup, workflow verbs, polling, diffing, and automation hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonvanlaak](https://clawhub.ai/user/simonvanlaak)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate assigned project-management work across GitHub, Planka, Plane, and Linear with a shared stage model, setup workflow, task-selection verbs, status updates, and scheduled autopilot polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or change more project-management items than its assigned-only behavior suggests.

Mitigation: Use a dedicated least-privilege account or token scoped to the exact repo, team, project, or board the skill should manage.

Risk: Scheduled autopilot execution can repeatedly act through inherited CLI privileges.

Mitigation: Do not enable the OpenClaw cron option until assigned-only filtering, stage mappings, and automation behavior are reviewed for the target workspace.

Risk: Ticket titles, bodies, comments, and internal project details may be shown to the agent or captured in logs.

Mitigation: Avoid exposing sensitive ticket content, review CLI auth state before use, and treat config/kanban-workflow.json as sensitive metadata.

Risk: Flagged npm development dependencies may affect tests or developer servers.

Mitigation: Update the flagged npm dev dependencies before running tests or developer servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonvanlaak/skills/openclaw-skill-clawban)
- [README](README.md)
- [Security](SECURITY.md)
- [Adapter notes](src/adapters/README.md)
- [Requirements](references/REQUIREMENTS.md)
- [Technical plan](references/TECH_PLAN.md)
- [Architecture review](references/ARCH_REVIEW.md)
- [GitHub CLI](https://cli.github.com/)
- [planka-cli](https://github.com/voydz/planka-cli)
- [Planka](https://github.com/plankanban/planka)
- [Plane](https://github.com/makeplane/plane)
- [Linear GraphQL API](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with CLI commands, workflow guidance, configuration details, and project-management updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local platform CLIs or wrapper scripts using the host's authenticated CLI sessions or API-key environment variables.]

## Skill Version(s):

0.1.6 (source: release evidence, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
