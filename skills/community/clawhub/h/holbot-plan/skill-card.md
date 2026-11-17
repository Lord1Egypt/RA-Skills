## Description:

Create structured plans for multi-step tasks, including features, research, automations, events, or other goals that benefit from breakdown, and deepen existing plans with interactive sub-agent review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcbuer](https://clawhub.ai/user/jcbuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert multi-step goals into structured implementation plans with scope, file maps, ordered steps, acceptance criteria, risks, and test scenarios. They can also use the deepen flow to expand an existing plan with implementation details, edge cases, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may consult persistent MEMORY.md context during planning without explicit scope or approval.

Mitigation: Use it only where prior memory is appropriate; avoid shared or sensitive environments unless memory access is clearly scoped and user-approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcbuer/skills/holbot-plan)
- [Brainstorm Skill](artifact/references/brainstorm.md)
- [Deepening Workflow](artifact/references/deepening-workflow.md)
- [Plan Sections Reference](artifact/references/plan-sections.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown structured plan with section headings, numbered implementation steps, acceptance criteria, risk notes, and test scenarios]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repo-relative file paths, implementation sequencing, time estimates, and optional saved plan paths when requested by the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
