## Description:

CEO-perspective plan review and strategy upgrader supporting four modes: expansion, selective expansion, hold scope, and scope reduction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and product owners use this skill to review implementation plans from a CEO-style strategic perspective before development. It helps challenge assumptions, compare implementation approaches, map failure modes, identify observability gaps, and choose whether to expand, hold, or reduce scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect local project context, which may expose commit history, TODOs, architecture documents, or design notes during the agent session.

Mitigation: Use it only on projects where sharing that repository context with the active agent session is acceptable.

## Reference(s):

- [Openclaw Ceo Review on ClawHub](https://clawhub.ai/x-rayluan/skills/openclaw-ceo-review)
- [x-rayluan ClawHub publisher profile](https://clawhub.ai/user/x-rayluan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured review sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include premise challenges, implementation alternatives, failure-mode maps, observability checklists, edge-case analysis, and a final review status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
