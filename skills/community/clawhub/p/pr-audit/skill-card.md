## Description:

Use when the user wants a local review of a GitHub pull request based on its diff, risks, quality, performance, tests, and security implications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review GitHub pull request diffs for correctness, conventions, performance, test coverage, and security-sensitive changes before merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pull request metadata and diffs may contain sensitive source code or business context.

Mitigation: Confirm the user is comfortable sharing the PR metadata and diff with the reviewing agent before use.

Risk: Review findings can be incomplete or incorrect if the available diff lacks enough repository context.

Mitigation: Ground findings in the actual diff and have a human reviewer verify recommendations before applying changes.

## Reference(s):

- [Skill page](https://clawhub.ai/wimi321/skills/pr-audit)
- [Provenance](references/provenance.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized findings, risk summary, and improvement suggestions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
