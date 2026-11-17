## Description:

Investigate OpenClaw pnpm test memory growth, Vitest OOMs, RSS spikes, and heap snapshot deltas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to investigate test OOMs and memory growth by reproducing the relevant test shape, collecting heap or RSS evidence, and deciding whether growth points to retained worker state or a cleanup issue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heap snapshots may retain sensitive data without warning or safeguards.

Mitigation: Use synthetic test data, restrict snapshot access, review snapshots before sharing, and delete them when finished.

## Reference(s):

- [Openclaw Test Heap Leaks on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-test-heap-leaks)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Analysis]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
