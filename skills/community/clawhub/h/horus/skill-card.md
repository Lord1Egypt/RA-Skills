## Description:

Register, track, and validate state observations against declared constraints without assuming universal truth or enforcing physical laws.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uniaolives](https://clawhub.ai/user/uniaolives)

### License/Terms of Use:

CC0 1.0 Universal

## Use Case:

Developers and AI-system designers use this skill as a protocol guide and reference implementation for observation registration, constraint declaration, violation logging, projection, and audit-trace export in distributed intelligence systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference Python uses assert-based validation, which can be disabled in optimized runtime modes.

Mitigation: Replace asserts with explicit runtime validation before using the reference implementation in production.

Risk: Predicate evaluation failures may be swallowed during constraint checking, reducing audit visibility.

Mitigation: Record predicate evaluation failures in the violation or audit log with enough context for review.

Risk: Exported traces can contain state coordinates, observer identifiers, metadata, constraints, and violations.

Mitigation: Add privacy controls, pseudonymous identifiers, and access checks before exporting or sharing traces.

Risk: The artifact includes integrity and determinism claims that may need reconciliation with actual export behavior.

Mitigation: Validate checksum generation, timestamp handling, and deterministic serialization against deployment requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uniaolives/skills/horus)
- [CS-RV Protocol Whitepaper](artifact/CS-RV_Protocol_Whitepaper.md)
- [CS-RV Implementation Guide](artifact/skills.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes protocol guidance, migration notes, tests, and JSON audit-trace examples.]

## Skill Version(s):

7.7.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
