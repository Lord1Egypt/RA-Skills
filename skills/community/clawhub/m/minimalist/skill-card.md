## Description:

Subtraction-first engineering for coding tasks: question whether a change needs to exist, reuse existing code, prefer standard library and native platform features, avoid new dependencies, and write the minimum code that fully works with safety guardrails intact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyeshjayswal](https://clawhub.ai/user/divyeshjayswal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep coding, refactoring, fixing, reviewing, and design work focused on the smallest correct change while preserving validation, security, error handling, and other safety guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt agents to run a repository-controlled logging script when rejecting scope or dependencies.

Mitigation: Inspect scripts/log-rejection.js and run it only with explicit approval in repositories you trust; otherwise skip the logging command.

Risk: The skill is persistent and may continue shaping coding responses after activation.

Mitigation: Use the documented off switch when normal coding behavior is desired.

## Reference(s):

- [Minimalist skill page](https://clawhub.ai/divyeshjayswal/skills/minimalist)
- [Publisher profile](https://clawhub.ai/user/divyeshjayswal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise prose and inline code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports lite, full, and ultra intensity levels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
