## Description:

Create or update pull request descriptions that are easy for humans and agents to review. Use when asked to create a PR, improve a PR body, add context, compare before/after behavior, add Mermaid diagrams, summarize verification, or document drawbacks and future improvements for code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or improve pull request descriptions that explain the problem, behavior change, diagrams, verification evidence, and remaining tradeoffs for human and agent reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pull request descriptions may expose private logs, identifiers, or URLs.

Mitigation: Review the proposed description for sensitive details before publication.

Risk: Descriptions may make unsupported verification claims.

Mitigation: Check each verification statement against the commands and results actually available.

## Reference(s):

- [PR Context Diagram on ClawHub](https://clawhub.ai/no7dw/skills/pr-context-diagram)

## Skill Output:

**Output Type(s):** [Markdown, Mermaid diagrams, Review guidance]

**Output Format:** [Markdown pull request descriptions with prose, Mermaid diagrams, and verification details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is grounded in the inspected changes and available verification evidence.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
