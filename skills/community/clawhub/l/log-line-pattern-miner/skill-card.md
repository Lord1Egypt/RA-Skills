## Description:

Groups pasted log lines by normalized template, counts recurring patterns, and highlights likely error signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and engineers use this skill to triage pasted logs, identify frequent error patterns, and spot rare exceptions obscured by retry noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted production logs may contain credentials or private identifiers.

Mitigation: Remove sensitive data before sharing logs; redact any secrets in examples and do not repeat them.

Risk: Heuristic normalization can merge distinct errors or mistake retry noise for the cause.

Mitigation: Check representative lines and correlated metrics before treating severity or root-cause guesses as confirmed.

## Reference(s):

- [Log Line Pattern Miner on ClawHub](https://clawhub.ai/hmahmadcs/skills/log-line-pattern-miner)
- [Regular-Expressions.info](https://www.regular-expressions.info/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown with a summary, ranked log templates, and optional regex or follow-up commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template counts, severity estimates, redacted examples, and follow-up questions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
