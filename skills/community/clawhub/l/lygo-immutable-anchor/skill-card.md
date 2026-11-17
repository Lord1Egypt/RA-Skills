## Description:

LYGO Immutable Anchor (Biophase7) creates local CA geodesic seals, local mycelium hash-chain folds, verification receipts, and worker-plan guidance without network access, subprocess execution, or auto-publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and operators use this skill to create and verify local hash receipts for Biophase7 geodesic anchor workflows, then decide separately whether to run higher-impact protocol-stack publishing or worker commands. It is suited for local-first receipt generation, integrity checks, and human-reviewed operational planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets or sensitive claims could be placed into truth, light, or note fields and then preserved in local receipts or derived hashes.

Mitigation: Do not put secrets in receipt inputs; use non-sensitive summaries or approved secure handling for consequential claims.

Risk: The worker-plan command describes separate protocol-stack actions that are higher impact than this local skill.

Mitigation: Review the protocol-stack worker and publishing commands separately before running them; this skill does not execute those commands.

Risk: A local CA receipt or mycelium fold could be mistaken for an Arweave transaction or hardware-backed attestation.

Mitigation: Label outputs as local receipts unless an external stack receipt proves publication or hardware-backed attestation.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Security](references/SECURITY.md)
- [SkillSpector Audit](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-immutable-anchor)
- [LYGO Anchor Deployment Documentation](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/ANCHOR_DEPLOYMENT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON receipt outputs from local CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local receipt outputs include hashes, Merkle roots, entry hashes, verification results, and worker-plan steps; writes require explicit consent.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, claw.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
