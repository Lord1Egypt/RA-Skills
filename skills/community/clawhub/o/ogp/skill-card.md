## Description:

OGP (Open Gateway Protocol) supports federated agent communication, peer management, and project collaboration across OpenClaw and Hermes gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dp-pcs](https://clawhub.ai/user/dp-pcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure and operate OGP federation, exchange agent-to-agent messages, manage peer scopes and policies, and coordinate cross-gateway project collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global CLI installation can pull an unexpected package version.

Mitigation: Pin and verify the @dp-pcs/ogp CLI version before installing or upgrading.

Risk: Federation can grant broad peer privileges and expose agents to remote inbound work.

Mitigation: Grant only necessary scopes, review agent-comms policies, and use approval-required handling for inbound agent work when trust is limited.

Risk: Clearing peers.json can remove federation state.

Mitigation: Back up OGP state files before clearing peer lists or resetting federation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dp-pcs/skills/ogp)
- [OGP project documentation](https://github.com/dp-pcs/ogp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and configuration guidance for the local ogp CLI and OGP state files.]

## Skill Version(s):

0.6.0 (source: server release metadata; artifact frontmatter reports 2.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
