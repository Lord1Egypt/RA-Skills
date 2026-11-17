## Description:

Warm multi-turn goal clarification and action planning for users with vague, oversized, or tangled goals who need help narrowing focus and turning goals into concrete next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryxdguan](https://clawhub.ai/user/terryxdguan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to clarify vague or overloaded goals, understand constraints, choose a realistic focus, and turn the result into next steps, short-term to-do lists, milestones, or weekly schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use saved goal, task, schedule, and progress context when the host app provides it.

Mitigation: Users should review what planning context is saved, used, or cleared, and avoid providing sensitive goal details that are not needed for planning.

Risk: Generated plans or weekly schedules may not fit the user's real constraints if the available context is incomplete or stale.

Mitigation: Treat plans as proposals, confirm assumptions with the user, and revise schedules when availability, energy, dependencies, or progress changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terryxdguan/skills/goal-clarifier)
- [English Guide: Gentle Goal Clarifier](references/guide-en.md)
- [Workflow: Gentle Goal Clarification to Action Plan](references/workflow-en.md)
- [Examples: Gentle Goal Clarifier](references/examples-en.md)
- [Evaluation Checklist: Gentle Goal Clarifier](references/eval-checklist-en.md)
- [Chinese Guide: Gentle Goal Clarifier](references/guide-zh.md)
- [Chinese Workflow: Gentle Goal Clarification to Action Plan](references/workflow-zh.md)
- [Chinese Examples: Gentle Goal Clarifier](references/examples-zh.md)
- [Chinese Evaluation Checklist: Gentle Goal Clarifier](references/eval-checklist-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Conversational text and Markdown action plans; weekly schedules may be emitted as JSON code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use host-provided goal, task, schedule, and progress context when available.]

## Skill Version(s):

0.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
