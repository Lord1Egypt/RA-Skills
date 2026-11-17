## Description:

Evaluate hook security, performance, and SDK compliance. Use for audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Claude Code hooks for security, performance, reliability, and SDK or configuration compliance. It provides evaluation criteria and guidance for reviewing hook implementations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial because several local path-like references could not be resolved, so the benign verdict is not a guarantee of safety.

Mitigation: Review the referenced local materials and consider the incomplete scan evidence before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-hooks-eval)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evaluation report with findings, scores, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a composite score, category scores, issue classifications, and recommendations.]

## Skill Version(s):

1.10.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
