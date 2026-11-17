## Description:

Local-first planning engine for trips, weeks, launches, projects, schedules, and structured decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents use Planner to turn goals into structured plans for trips, weeks, launches, projects, schedules, and decisions. It helps capture constraints, phases, milestones, next steps, and notes while keeping planning data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plans are saved locally across sessions and may contain personal schedules, travel details, deadlines, or decision context.

Mitigation: Avoid storing secrets or highly sensitive personal details, and periodically review or delete the local planner JSON files when retention matters.

## Reference(s):

- [Planner Philosophy](references/philosophy.md)
- [ClawHub Planner Skill](https://clawhub.ai/agistack/skills/planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text output backed by local JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-created plans locally under ~/.openclaw/workspace/memory/planner/.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
