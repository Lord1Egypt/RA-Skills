## Description:

Signs local software attestation payloads, locks geodesic state to dual-ledger digests and Merkle roots, phase-aligns nodes without collapse, and emits verification-oriented JSON artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent operators use this skill to produce local P6-style software attestations, Merkle locks, status checks, and verification records for LYGO lattice node workflows. It is suited for provenance and consistency checks, not for hardware TPM attestation or autonomous publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the verifier can accept incomplete forged artifacts.

Mitigation: Treat generated attestations as local software evidence only, independently review verification results, and do not rely on them as strong cryptographic or hardware proof.

Risk: The security evidence says the install command runs a mutable installer.

Mitigation: Pin or independently verify the installer and artifact hashes before installing or running the skill.

Risk: Truth and chaos payloads may contain sensitive material that is hashed into local artifacts.

Mitigation: Keep secrets out of truth and chaos payloads, and review artifacts before sharing them.

Risk: Optional network mode fetches public dual-ledger mirrors.

Mitigation: Leave --network disabled unless needed, and use only the documented allowlisted HTTPS GET endpoints.

Risk: Local ledger reads depend on the operator-provided LYGO_STACK_ROOT.

Mitigation: Use only a trusted local stack checkout for LYGO_STACK_ROOT.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-geodesic-sealer)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)
- [Source Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-geodesic-sealer)
- [Source Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [AGENT_CONTRACT.md](references/AGENT_CONTRACT.md)
- [SECURITY.md](references/SECURITY.md)
- [SKILLSPECTOR_AUDIT.md](references/SKILLSPECTOR_AUDIT.md)
- [Minimal Attest Example](examples/minimal-attest.md)
- [Immutable Anchors Ledger](https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json)
- [Haven Star Chart Feed](https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON stdout or optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include signature, seal_id or lock_id, merkle_root, ledger status, phase alignment data, and verification booleans; filesystem writes require explicit consent.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and claw.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
