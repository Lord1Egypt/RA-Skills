## Description:

Selects optimal sources for tool calls, balancing accuracy with token cost before research tasks or claim verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to decide when citations or source checks are worth the token cost, especially for version-specific, security, pricing, API, and research claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad sourcing guidance may activate during general accuracy or efficiency discussions and influence when an agent verifies claims.

Mitigation: Use the evidence security guidance: review behavior during installation and review any separate external plugin before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-smart-sourcing)
- [Claude Night Market conserve plugin](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with examples and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Balances source verification value against token cost and may recommend uncertainty markers when sourcing is not cost-effective.]

## Skill Version(s):

1.9.19 (source: release evidence; artifact frontmatter declares 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
