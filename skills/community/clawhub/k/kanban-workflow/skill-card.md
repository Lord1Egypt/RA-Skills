## Description:

Kanban Workflow is a TypeScript skill for a stage-based agentic co-worker that integrates PM platforms through CLI-auth adapters and provides setup plus workflow verbs around backlog, blocked, in-progress, and in-review stages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonvanlaak](https://clawhub.ai/user/simonvanlaak)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to let an agent inspect, select, update, create, and move project-management work items through a shared Kanban lifecycle while relying on already-authenticated platform CLIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow verbs can make live comments, stage changes, labels/state changes, or new tasks through the authenticated PM CLI.

Mitigation: Install and run the skill only with a scoped CLI account whose project permissions match the intended agent authority.

Risk: Automatic progress updates can repeatedly post visible comments while work remains in progress.

Mitigation: Enable periodic updates only after confirming the cadence, visibility, persisted state, and stop conditions are acceptable for the team.

Risk: The artifact describes early scaffolding and changing interfaces.

Mitigation: Review the configured adapter behavior and run the included tests before using it in CI or production workflows.

## Reference(s):

- [Kanban Workflow README](README.md)
- [Kanban Workflow adapters](src/adapters/README.md)
- [Kanban Workflow requirements](references/REQUIREMENTS.md)
- [Kanban Workflow technical plan](references/TECH_PLAN.md)
- [Kanban Workflow architecture review](references/ARCH_REVIEW.md)
- [GitHub CLI](https://cli.github.com/)
- [planka-cli](https://github.com/voydz/planka-cli)
- [plane-cli](https://github.com/simonvanlaak/plane-cli)
- [linear-cli](https://github.com/simonvanlaak/linear-cli)
- [Planka](https://github.com/plankanban/planka)
- [Plane](https://github.com/makeplane/plane)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON CLI output, TypeScript code/configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow actions may post comments, change stages, or create tasks in the configured project-management system.]

## Skill Version(s):

0.1.12 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
