## Description:

Bayesian inference engine for AI agents that updates beliefs with evidence, combines weighted factors into posterior probabilities, and supports calibration tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to start from a prior probability, combine weighted evidence factors, update posterior probabilities, and track calibration over repeated predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires ORACLAW_API_KEY and sends evidence to a third-party provider for paid inference.

Mitigation: Use a scoped API key, confirm the paid API model before installation, and avoid sending sensitive or confidential evidence unless the provider is trusted for that data.

## Reference(s):

- [OraClaw Bayesian homepage](https://oraclaw.dev/bayesian)
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-bayesian)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with JSON-shaped tool input and probability results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; paid inference is disclosed at $0.02 per inference with a free monthly tier.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
