## Description:

Use the OOMOL-connected PhantomBuster integration to inspect agents, containers, and organizations, or launch and stop agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect a connected PhantomBuster organization and its agents or containers, and to launch or stop agents through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified third-party code, and the remote installers' exact system changes are unknown.

Mitigation: Review setup before enabling the skill, and approve and verify a specific oo CLI release instead of allowing automatic script execution.

Risk: PhantomBuster requests pass through OOMOL, and agent launch or stop operations can affect account state.

Mitigation: Review managed-skill synchronization settings and confirm launch or stop operations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-phantombuster)
- [PhantomBuster](https://phantombuster.com)
- [PhantomBuster API documentation](https://hub.phantombuster.com/reference/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON action results and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action; launching or stopping an agent changes its state.]

## Skill Version(s):

1.0.5 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
