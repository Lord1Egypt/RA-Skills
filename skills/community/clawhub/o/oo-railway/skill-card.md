## Description:

Use the oo CLI to inspect Railway projects, services, deployments, and logs, manage variables, deploy services, and roll back eligible deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Railway account users can use an OOMOL-connected account to inspect Railway projects, services, deployments, and logs; manage variables; deploy services; and roll back eligible deployments. The skill directs users to confirm write and destructive actions before they run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI dependency can install additional agent skills, an effect the security review says is not clearly explained.

Mitigation: Review CLI setup separately, use narrowly scoped Railway credentials with OOMOL, and consider setting OO_SKILLS_SYNC_DISABLED=1 before running oo to prevent automatic skill installation.

## Reference(s):

- [Railway](https://railway.com)
- [Railway API documentation](https://docs.railway.com/integrations/api)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses with concise operational guidance and example commands in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action responses vary and may include Railway data and execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
