## Description:

Verifies public LYGO lattice mirrors, builds public verification manifests, prepares Haven Star Chart proposal mappings, and plans external free-server sync for Layer C world-network workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO SOVEREIGN LICENSE v2.0

## Use Case:

Developers and operators use this skill to verify public LYGO Layer C mirror endpoints, generate local public verification manifests, create Star Chart proposal JSON, and plan external sync steps while preserving local stack authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A manifest can steer the verifier to contact arbitrary HTTPS hosts from the user's environment.

Mitigation: Use only a LYGO stack and manifest you control, avoid custom manifests from others, and prefer the default fixed verification path.

Risk: Opt-in builder or refresh modes can execute Python against the trusted stack and write manifest, proposal, report, or snapshot files.

Mitigation: Run zero-write verification first, and use write, rebuild, refresh, or snapshot flags only after explicit user intent and required trust or consent flags.

Risk: Public mirrors can be stale, degraded, or inconsistent with local LYGO roots.

Mitigation: Treat public HTTPS data as mirror evidence only, verify local Layer A and B roots first, and report public degradation without rewriting local records from public data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-external-lattice-anchor)
- [World Lattice Layer Documentation](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/WORLD_LATTICE_LAYER.md)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Haven Star Chart](https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html)
- [Agent Contract](references/AGENT_CONTRACT.md)
- [Security Notes](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown/text guidance with shell commands and optional JSON reports, manifests, proposals, or sync plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default verification is non-mutating; report, manifest, proposal, and snapshot writes require explicit opt-in flags or consent.]

## Skill Version(s):

1.1.1 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
