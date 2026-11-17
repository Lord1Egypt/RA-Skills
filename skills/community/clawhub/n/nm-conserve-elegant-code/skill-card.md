## Description:

Guide minimal code via a decision ladder with full safety, edge, and negative-case coverage

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before adding code or dependencies and when reviewing a diff. It helps them choose the simplest adequate approach while preserving correctness, security, performance, and edge-case handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because four references could not be resolved.

Mitigation: Review unresolved references before relying on guidance that depends on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conserve-elegant-code)
- [Project page listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code]

**Output Format:** [Code with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected decision-ladder rung and relevant safety, performance, and edge-case considerations.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
