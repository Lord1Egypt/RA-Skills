## Description:

Reviews Prometheus instrumentation in Go code for proper metric types, labels, and patterns. Use when reviewing code with prometheus/client_golang metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to review Go code that uses prometheus/client_golang instrumentation, focusing on metric types, label cardinality, metric naming, histogram buckets, registration lifecycle, and /metrics exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review findings may be incomplete or incorrect because the skill provides guidance rather than automated verification.

Mitigation: Confirm findings against the referenced Go code and require concrete file or symbol evidence before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/prometheus-go-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review guidance with checklist items and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to cite concrete files or symbols before recording findings.]

## Skill Version(s):

2.3.1 (source: evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
