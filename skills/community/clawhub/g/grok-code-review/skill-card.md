## Description:

Perform expert, security-first code reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code, diffs, pull requests, and implementations for security, correctness, quality, performance, maintainability, and test coverage issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect nearby repository files when a provided snippet or diff lacks enough context.

Mitigation: Review the files the agent reads and avoid sharing repositories or paths that contain unrelated sensitive data.

Risk: Suggested fixes or commands from a code review can be incomplete or unsuitable for a specific production environment.

Mitigation: Review suggested changes before applying them and require explicit confirmation before any action that modifies systems or data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maliot100x/skills/grok-code-review)
- [ClawHub publisher profile](https://clawhub.ai/user/maliot100x)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown structured review with severity sections and optional code or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis and advice only; suggested fixes should be reviewed before applying.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
