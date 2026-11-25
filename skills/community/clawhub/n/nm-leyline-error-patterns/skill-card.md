## Description:

Provides error classification, recovery, and graceful-degradation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to classify service and agent errors, choose recovery strategies, and provide actionable debugging guidance when building resilient integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retry guidance could repeat an operation whose earlier attempt already took effect.

Mitigation: Use bounded retries only for operations that are safe to repeat, and check operation status before retrying side effects.

Risk: Replacing or reassigning an agent could duplicate work that is still in progress.

Mitigation: Confirm task ownership and the last checkpoint before reassigning work or starting a replacement.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-error-patterns)
- [Clawdis homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with Python and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory patterns and examples for adaptation to the host service or agent workflow.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
