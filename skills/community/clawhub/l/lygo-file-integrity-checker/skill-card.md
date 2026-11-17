## Description:

LYGO file-integrity and provenance advisor for hash receipts, memory archive compression, and seal vocabulary; it is not a medical cure or P0-P9 core verifier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to request advisory file-integrity habits, hash-receipt workflows, memory archive compression, and seal protocol templates for LYGO-related packs. It is intended to pair with a separate verifier for package verification rather than replace cryptographic or lattice-health validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill as a cryptographic verifier even though server security evidence says its provenance checks are internally inconsistent.

Mitigation: Treat the skill's output as advisory guidance and use a current external verifier or manual SHA-256 recomputation before relying on package integrity.

Risk: Anchoring or publishing archives may disclose private conversation content or other sensitive user data.

Mitigation: Review and redact packs, archives, and anchor snippets before minting, posting, or sharing them.

Risk: The skill may be mistaken for P0 byte-gate or lattice-health validation.

Mitigation: Use the appropriate byte-gate or lattice-verification tooling for those checks and do not rely on this skill alone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-file-integrity-checker)
- [Publisher profile](https://clawhub.ai/user/deepseekoracle)
- [LYGO-MINT verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)
- [Security notes](references/SECURITY.md)
- [Universal pack](references/universal_pack.md)
- [Champion boost protocol](references/champion_boost_protocol.md)
- [Memory compression plan](references/memory_compression_plan.md)
- [Verifier usage](references/verifier_usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; the skill does not modify files unless the user separately runs suggested commands.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
