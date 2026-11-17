## Description:

Deploy and manage cloud services on Ink (ml.ink), including projects, services, databases, DNS, custom domains, workspace configuration, and deployment monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gluonfield](https://clawhub.ai/user/gluonfield)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and operate applications on Ink, including services, databases, environment variables, DNS, and custom domains. It supports initial deployment workflows and ongoing operations such as logs, status checks, redeploys, and resource configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real infrastructure changes, including deployment, deletion, DNS, database, and secret operations.

Mitigation: Confirm the workspace, project, repository, branch, and exact target resource before any mutation, and require explicit approval for delete, DNS, and secret replacement operations.

Risk: The skill recommends global CLI installation paths that may introduce supply-chain or version drift risk.

Mitigation: Use a pinned or verified Ink CLI installation path before allowing the agent to execute infrastructure commands.

Risk: Temporary secret files used for imports can remain in the working tree if cleanup fails.

Mitigation: Use temporary files only when needed, delete them immediately after import, and verify that no secret file remains in the working tree.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gluonfield/skills/ink-skill)
- [Ink platform](https://ml.ink)
- [Ink DNS](https://ml.ink/dns)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Ink CLI commands that mutate cloud infrastructure, secrets, DNS, repositories, databases, and deployed services.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
