## Description: <br>
Manage Operately from the CLI for goals, OKRs, projects, tasks, milestones, spaces, documents, discussions, check-ins, reviews, assignments, people, permissions, and resource hubs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markoa](https://clawhub.ai/user/markoa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to let an agent inspect and manage an Operately workspace through the operately CLI, including goals, projects, spaces, tasks, reviews, documents, permissions, and resource hubs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate a real Operately workspace with broad workspace-administration powers, including destructive, permission-changing, member/admin, publication, notification, and file-upload actions. <br>
Mitigation: Use a least-privilege or read-only token where possible, and require explicit confirmation before delete, permission, member/admin, publication, notification, or file-upload actions. <br>
Risk: Credentials and base URL settings can route commands to real production, staging, self-hosted, or local Operately instances. <br>
Mitigation: Verify the active profile and base URL before running commands, and avoid putting real passwords or tokens directly on the command line. <br>
Risk: Some authentication flows require human browser confirmation or inbox access and are unsuitable for unattended automation. <br>
Mitigation: Prefer token-based login for headless work and leave Google OAuth or email-code steps to a human when required. <br>


## Reference(s): <br>
- [Operately skills repository](https://github.com/operately/skills) <br>
- [Auth Flows](references/auth-flows.md) <br>
- [Project Workflows](references/project-workflows.md) <br>
- [Goal Workflows](references/goal-workflows.md) <br>
- [Task Workflows](references/task-workflows.md) <br>
- [Space Workflows](references/space-workflows.md) <br>
- [Resource Hubs](references/resource-hubs.md) <br>
- [Collaboration Patterns](references/collaboration-patterns.md) <br>
- [Assignments and Reviews](references/assignments-and-reviews.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed operately CLI and a valid Operately token, environment variable, or saved profile.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
