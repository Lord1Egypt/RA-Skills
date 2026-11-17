## Description:

Phason state resolution skill for Reson8-Labs split-brain states, HTTP 408 timeout deadlocks, push/flip conflicts, and coherence density spikes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toolate28](https://clawhub.ai/user/toolate28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide resolution of Reson8-Labs ledger conflicts by detecting candidate states, validating conservation and braid continuity, selecting a higher-WAVE state, and verifying the committed result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to mutate ledger state or release locks from broad conflict triggers.

Mitigation: Narrow invocation triggers and require explicit user approval before any commit or lock release.

Risk: Cached event replay may duplicate, reorder, or apply stale state changes.

Mitigation: Add replay protection, idempotency checks, audit logging, and rollback controls before using cached events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toolate28/skills/phason-flipper)
- [Knot 16 Phason Resolution interactive simulator](public/publications/knot-16/445.html)
- [quasicrystal_phason_scheduler.py](quasicrystal_phason_scheduler.py)
- [POP protocol spec](references/protocol-spec.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Code]

**Output Format:** [Markdown with JSON and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include state selection steps, validation checks, commit guidance, cache replay guidance, and example payloads.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
