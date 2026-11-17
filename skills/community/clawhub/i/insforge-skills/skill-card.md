## Description:

Create and manage InsForge projects through CLI workflows for authentication, project setup, database management, edge functions, storage, deployments, secrets, schedules, logs, and project documentation lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonychang04](https://clawhub.ai/user/tonychang04)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to operate InsForge Backend-as-a-Service projects from an agent workflow, including authentication, project setup, database operations, functions, storage, deployments, secrets, schedules, logs, and CLI documentation lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact account, database, deployment, secrets, and storage workflows.

Mitigation: Review commands before execution, verify authentication and linked project context, and avoid `-y` for destructive or administrative actions unless the exact command and target are known.

Risk: Credentials, access tokens, database dumps, and `.insforge/project.json` may expose sensitive project access if logged or committed.

Mitigation: Prefer OAuth or scoped tokens, keep exports and local project files out of source control and logs, and pass sensitive deployment values through managed environment variables.

Risk: Database imports, raw SQL queries, and storage bucket deletion can modify or permanently remove data.

Mitigation: Use backups, review SQL and import flags such as `--truncate`, and confirm storage bucket targets before deletion.

Risk: `insforge create` can install additional agent skills through an unpinned remote `npx` command.

Mitigation: Inspect generated project changes and installed skills before use in production or CI.

Risk: Deployments upload project archives to hosting infrastructure and can include unintended files if project layout is incorrect.

Mitigation: Run local builds first and verify excluded files, environment variables, and build output directories before deploying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonychang04/skills/insforge-skills)
- [insforge create](references/create.md)
- [insforge login](references/login.md)
- [insforge db query](references/db-query.md)
- [insforge db export](references/db-export.md)
- [insforge db import](references/db-import.md)
- [insforge functions deploy](references/functions-deploy.md)
- [insforge deployments deploy](references/deployments-deploy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, code snippets, JSON examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that authenticate, mutate databases, deploy code, manage secrets, upload files, or export project data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
