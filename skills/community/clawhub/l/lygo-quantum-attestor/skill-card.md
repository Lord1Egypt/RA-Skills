## Description:

LYGO Quantum Attestor helps agents create and verify local Protocol 6 software attestations using Biophase7 anchors, SLM Merkle data, Delta9 seals, and non-collapsing receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent operators use this skill to generate local software attestation artifacts, verify node integrity, seal attestations, and emit receipts for LYGO-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipts may be mistaken for hardware-backed proof or live network consensus.

Mitigation: Treat receipts only as local software attestation artifacts unless separate hardware or network consensus evidence is available.

Risk: Input values supplied through --truth, --chaos, or --anchor-file may be stored in generated JSON artifacts.

Mitigation: Do not provide secrets or sensitive data in those fields, and review generated artifacts before sharing them.

Risk: The skill can write attestation artifacts to disk when requested.

Mitigation: Use write options only with explicit consent and confirm the output path before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-quantum-attestor)
- [ClawHub Release Page](https://clawhub.ai/deepseekoracle/lygo-quantum-attestor)
- [Security Audit](https://clawhub.ai/deepseekoracle/skills/lygo-quantum-attestor/security-audit)
- [Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-quantum-attestor)
- [Security Notes](references/SECURITY.md)
- [SkillSpector Audit](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON attestation artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may include local attestation, sealed attestation, verification, or receipt JSON when writes are explicitly requested with consent.]

## Skill Version(s):

1.0.1 (source: frontmatter, claw.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
