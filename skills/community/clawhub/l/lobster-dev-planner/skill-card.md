## Description:

Lobster Dev Planner helps agents collect software requirements through guided conversation, generate detailed development documentation, and coordinate agent-assisted implementation with connected tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, builders, and nontechnical users use this skill to turn vague software ideas into structured plans, development documents, API and style references, and coordinated implementation steps. It is intended for supervised project planning and agent orchestration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad automatic use of repository, database, deployment, filesystem, and notification tools after development begins.

Mitigation: Use project-scoped or disposable credentials and require human review before commits, pushes, SQL writes, deployments, file changes outside the project, and outbound messages.

Risk: Generated documentation can include weak example credentials or operational assumptions that may be copied into real environments.

Mitigation: Replace all example credentials, review environment variables and secrets handling, and validate security-sensitive documentation before implementation.

Risk: Automated planning and agent delegation can produce incorrect technical choices or unsafe execution steps for the user's project context.

Mitigation: Keep the workflow supervised, review generated plans and task assignments, and run tests and security checks before accepting generated changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-dev-planner)
- [Plan template](references/plan-template.md)
- [Development document template](references/dev-doc-template.md)
- [API document template](references/api-doc-template.md)
- [Style guide template](references/style-guide-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with structured plans, document templates, implementation tasks, and inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project documentation, implementation checklists, tool-use plans, progress reports, and delivery summaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
