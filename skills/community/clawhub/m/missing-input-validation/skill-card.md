## Description:

External input flows into sensitive operations without being checked for type, shape, range, or sanitization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify missing validation at trust boundaries and improve handling of external input before it reaches sensitive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation or debugging guidance could expose sensitive raw input in errors, logs, or responses.

Mitigation: Keep errors clear but use field names, expected constraints, correlation IDs, and redacted or truncated values instead of raw sensitive input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/missing-input-validation)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise secure-coding guidance and validation recommendations for agent responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
