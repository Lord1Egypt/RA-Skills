## Description:

Manage Operately from the CLI: goals, OKRs, projects, project templates, tasks, milestones, spaces, documents, discussions, check-ins, reviews, assignments, people, permissions, full-text search, document history, and Docs & Files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markoa](https://clawhub.ai/user/markoa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and company teams use this skill to operate an Operately workspace through CLI commands for goals, projects, tasks, spaces, documents, reviews, assignments, people, permissions, search, and document history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad full-access workspace operations, including destructive commands and admin, member, permission, and visibility changes.

Mitigation: Use the least-privileged token available, verify target IDs before execution, and require human confirmation for deletes, admin or member changes, permission changes, and public or company-wide visibility changes.

Risk: Inline credential examples can lead to exposed secrets in shell history, logs, or process lists.

Mitigation: Prefer environment or secret-manager injection for tokens and passwords, and avoid placing secrets directly in command lines.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/markoa/skills/operately-cli)
- [Operately skills homepage](https://github.com/operately/skills)
- [Project Workflows](references/project-workflows.md)
- [Project Template Workflows](references/project-template-workflows.md)
- [Goal Workflows](references/goal-workflows.md)
- [Task Workflows](references/task-workflows.md)
- [Space Workflows](references/space-workflows.md)
- [Docs & Files](references/docs-and-files.md)
- [Collaboration Patterns](references/collaboration-patterns.md)
- [Assignments and Reviews](references/assignments-and-reviews.md)
- [Auth Flows](references/auth-flows.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated API-changing operations in an Operately workspace.]

## Skill Version(s):

1.9.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
