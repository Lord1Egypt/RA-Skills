## Description:

Detect and recover from context resets, memory/index outages, and cache clears with deterministic, trust-preserving reconstruction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otherpowers](https://clawhub.ai/user/otherpowers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recover safely from lost context, memory/index outages, or cache clears, and to add explicit consent checks before irreversible actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local recovery checkpoint files can preserve sensitive project context if the agent records too much.

Mitigation: Keep manifests minimal, redact secrets and unnecessary PII, and review .memory-latch files periodically.

Risk: Optional HMAC or wallet modes add credential and signer dependencies.

Mitigation: Leave those modes disabled unless deliberately configured; fall back to checksum and text-token consent when required configuration is missing.

Risk: A tampered manifest or unsafe path could mislead recovery.

Mitigation: Use canonical workspace paths, reject symlinks and traversal, prefer owner-only permissions, and verify checksums before trusting checkpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otherpowers/skills/memory-latch)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON manifest snippets and short action tokens]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local workspace checkpoint files under <workspace>/.memory-latch when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
