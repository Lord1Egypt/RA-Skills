## Description:

Discover what two sources agree on - find the signal in the noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to compare two related text sources or extractions and identify shared principles, unique points, and divergences without choosing a winner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad comparison requests may include more source text than the user intended to analyze.

Mitigation: Provide only the two sources intended for comparison and keep sensitive material within the agent environment's configured trust boundary.

Risk: Shared patterns can be mistaken for proof of truth or correctness.

Mitigation: Treat N=2 agreement as evidence of overlap, then use domain review or additional sources before relying on the conclusion.

Risk: Cloud-hosted agent models may process supplied source text as part of normal agent operation.

Mitigation: Use an agent runtime and model provider approved for the sensitivity of the compared sources.

## Reference(s):

- [Pattern Finder ClawHub Page](https://clawhub.ai/leegitw/skills/pattern-finder)
- [Project Homepage](https://github.com/live-neon/skills/tree/main/pbd/pattern-finder)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown narrative with optional structured JSON comparison output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares two user-provided sources and may include shared patterns, source-specific findings, divergence analysis, next steps, and share text for high-confidence matches.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
