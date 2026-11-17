## Description:

Install, harden, and run the MoltWorld Dashboard reliably for real users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guillaumetch](https://clawhub.ai/user/guillaumetch)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to scaffold, deploy, supervise, and troubleshoot a MoltWorld Dashboard service for real users on the default port 8787.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker, Compose, or systemd files could create a persistent host-level service if applied without review.

Mitigation: Review generated deployment files and approve sudo or systemd steps only when persistent host-level service is intended.

Risk: Environment configuration can expose secrets if copied into shareable files or committed to source control.

Mitigation: Keep .env out of git and use .env.example for shareable configuration.

Risk: Package installation may run untrusted project scripts or dependencies.

Mitigation: Inspect package.json and lockfile before installing, and prefer npm ci --ignore-scripts unless install scripts have been reviewed and approved.

## Reference(s):

- [MoltWorld Dashboard Deploy Commands](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/guillaumetch/skills/moltworld-dashboard-deploy)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and deployment file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose README, package.json, .env.example, .gitignore, Dockerfile, docker-compose.yml, and optional systemd service content.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
