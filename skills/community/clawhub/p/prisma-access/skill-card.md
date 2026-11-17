## Description:

All-in-one Prisma Access management for Strata Cloud Manager (SCM). Generate configurations, audit against best practices, migrate between tenants, troubleshoot issues, and automate via SCM API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesandao](https://clawhub.ai/user/leesandao)

### License/Terms of Use:

MIT-0

## Use Case:

Network security administrators and engineers use this skill to generate, audit, migrate, troubleshoot, and automate Prisma Access configurations through Strata Cloud Manager workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, delete, migrate, and push Prisma Access security configuration using tenant credentials.

Mitigation: Use a least-privileged SCM service account and require explicit confirmation for every create, update, delete, migration, and push operation.

Risk: Configuration changes may have tenant-wide network security impact if applied without review.

Mitigation: Prefer dry runs with impact previews, review proposed changes before execution, and avoid automatic commits.

Risk: Credential values may be exposed through shell command patterns on shared machines.

Mitigation: Avoid passing secrets directly in shared shell histories or logs, and handle SCM client credentials through protected environment management.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leesandao/skills/prisma-access)
- [Publisher profile](https://clawhub.ai/user/leesandao)
- [Project homepage](https://github.com/leesandao/prismaaccess-skill)
- [Strata Cloud Manager API base URL](https://api.sase.paloaltonetworks.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SCM API-compatible JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, required folder parameters, query parameters, audit findings, migration plans, and troubleshooting recommendations.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
