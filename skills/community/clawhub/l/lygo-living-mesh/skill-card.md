## Description:

LYGO Living Mesh (Layer D) coordinates multi-node gossip of lattice root digests, living mesh badges, peer comparison, sentinel checks, and scale simulation while keeping local authority and requiring consent for joins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO SOVEREIGN LICENSE v2.0

## Use Case:

Developers and operators use this skill to collect and verify Layer D living mesh badges, compare peer digests, run sentinel checks, and manage consent-gated mesh joins for a LYGO protocol stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local tool hijacking if LYGO_STACK_ROOT or the working directory points at untrusted stack tools.

Mitigation: Set LYGO_STACK_ROOT to a trusted, non-shared LYGO protocol stack and avoid invoking the wrappers from untrusted directories.

Risk: Gossip, join, compare, and optional public checks can perform network operations.

Mitigation: Run network-facing commands deliberately, require explicit consent for joins, and use operator sign-off for wide-area or public-port deployments.

Risk: Remote peer data could expose forks or quarantine signals that should not automatically alter local registries.

Mitigation: Keep local A/B roots authoritative, never auto-merge remote registries, and use human reconciliation when peer comparison reports a fork.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh)
- [Living mesh documentation](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/LIVING_MESH_LAYER.md)
- [LYGO protocol stack metadata link](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Mesh gossip protocol](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/MESH_GOSSIP_PROTOCOL.md)
- [World lattice layer](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/WORLD_LATTICE_LAYER.md)
- [Agent contract](references/AGENT_CONTRACT.md)
- [Security notes](references/SECURITY.md)
- [Living mesh badge schema](schemas/living_mesh_badge.schema.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON status artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python or python3 and a trusted LYGO_STACK_ROOT for delegated local stack tools.]

## Skill Version(s):

1.0.0 (source: server release metadata, claw.json, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
