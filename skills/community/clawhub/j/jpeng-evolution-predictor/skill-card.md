## Description:

Predict optimal next evolution actions based on history analysis, including stagnation detection, innovation gap measurement, and skill recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze OpenClaw evolution history and choose the next evolution focus, such as breaking stagnation, increasing innovation, exploring new domains, or stabilizing current behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read persistent OpenClaw evolution history by default, including extracted signals, intents, and gene names.

Mitigation: Install only when that history access is acceptable, or require an explicit approved evolution history path before use.

Risk: The security verdict is suspicious because the default history access is not clearly disclosed in the skill instructions.

Mitigation: Review the skill before installing and document the default history path and data exposure expectations for users.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON-compatible prediction object and human-readable text or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prediction category, priority, confidence, reasoning, metrics, alternatives, and suggested skills.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
