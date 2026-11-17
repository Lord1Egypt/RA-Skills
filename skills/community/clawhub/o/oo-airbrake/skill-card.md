## Description:

Search and read Airbrake project, deploy, error group, notice, and status data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support teams use the skill to inspect Airbrake projects, deploys, error groups, notices, and notice processing status from a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI installers execute downloaded code, and the supplied evidence does not verify those installers or the hosted implementation.

Mitigation: Review and approve the CLI installation separately and use a verified release.

Risk: Actions use the permissions of the connected Airbrake account through OOMOL-mediated access.

Mitigation: Connect only an appropriately limited Airbrake account and understand that OOMOL mediates access.

Risk: Automatic agent-skill synchronization may bring skill updates into use before they are reviewed.

Mitigation: Consider disabling automatic agent-skill synchronization.

## Reference(s):

- [Airbrake API documentation](https://docs.airbrake.io/docs/devops-tools/api/)
- [Airbrake](https://airbrake.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured Airbrake data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by the selected Airbrake read action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
