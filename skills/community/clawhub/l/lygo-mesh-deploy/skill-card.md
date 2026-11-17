## Description:

LYGO mesh deploy supports Phase 5 epidemic gossip, SLM Merkle, mycelium and consensus routes, and Phase 9 TLS HTTPS node API workflows for local cluster scripts and pinned gossip before wide-area use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare and run LYGO mesh deployment workflows, including local gossip convergence checks, node API endpoint review, TLS setup, and wide-area safety controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks operators to run unpinned remote code and an unpinned installer.

Mitigation: Review or pin the exact GitHub commit and ClawHub package version before installing or running the skill.

Risk: Mesh scripts and node APIs can expose public network services.

Mitigation: Run the scripts in a least-privileged, isolated environment and expose public services only after explicit operator review with TLS and gossip pinning enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-mesh-deploy)
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO protocol stack pages](https://deepseekoracle.github.io/lygo-protocol-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operator guidance for TLS, gossip pinning, and review before public network exposure.]

## Skill Version(s):

1.0.1 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
