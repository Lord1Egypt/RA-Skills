## Description:

Migrate OpenClaw agents across platforms and servers, preserving identity, memory, configuration, and skills for deployment, backup, syncing, and upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haha8d](https://clawhub.ai/user/haha8d)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to export, transfer, restore, and synchronize OpenClaw agent state across local, server, GitHub, and Docker deployment environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent exports and GitHub syncs can expose sensitive identity, memory, configuration, credentials, or session history.

Mitigation: Sanitize configuration before export, avoid full session exports unless required, use only trusted private repositories, and rotate any credentials that may have moved.

Risk: Restore and pull workflows can overwrite local agent state or execute restore code from a supplied repository.

Mitigation: Inspect restore.sh before execution, pull only from trusted repositories, and test restore behavior in a staging environment before production use.

Risk: Repository synchronization can alter remote repository history, including forced pushes.

Mitigation: Use a dedicated backup repository and confirm it has no important history before allowing force-push behavior.

## Reference(s):

- [Docker deployment guide](references/docker-deploy.md)
- [ClawHub skill page](https://clawhub.ai/haha8d/skills/openclaw-migrate-2)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to run migration, synchronization, and restore scripts after reviewing inputs and credentials.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
