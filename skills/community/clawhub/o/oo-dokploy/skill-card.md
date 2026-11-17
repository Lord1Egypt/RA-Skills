## Description:

Manage Dokploy projects, services, deployments, domains, and related settings through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Dokploy projects, services, deployments, logs, domains, and providers, and to create, update, deploy, or remove resources through their connected Dokploy account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installers whose effects were not verified and may not receive separate approval.

Mitigation: Install the CLI from a verified release with the user's approval, and review installer effects before setup.

Risk: Setup may automatically install other agent skills.

Mitigation: Review or disable automatic installation of additional skills.

Risk: Dokploy operations can change or delete resources, and the hosted connector implementation was not verified.

Mitigation: Use a narrowly scoped Dokploy connection and retain the documented confirmations for changes and deletions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-dokploy)
- [Dokploy](https://dokploy.com)
- [Dokploy API documentation](https://docs.dokploy.com/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON API results and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Dokploy account and selected action.]

## Skill Version(s):

1.0.5 (source: skill metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
