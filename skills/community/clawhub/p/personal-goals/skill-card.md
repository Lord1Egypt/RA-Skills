## Description:

Acts as the user's goal-setting and accountability partner by tracking life goals, milestones, progress, and deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gekacross](https://clawhub.ai/user/gekacross)

### License/Terms of Use:


## Use Case:

External users use this skill in personal goal-setting chats to define goals, break them into milestones, track progress, update deadlines, and run retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain a persistent goals file that may include sensitive life, health, finance, career, or relationship information.

Mitigation: Install only when persistent personal-goal memory is acceptable, and review the stored goals file for sensitive content before broader use.

Risk: Broad trigger conditions can cause the skill to read or update goal memory without an explicit confirmation step.

Mitigation: Narrow the trigger conditions and require user confirmation before writing updates to knowledge/personal/goals.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gekacross/skills/personal-goals)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, file updates]

**Output Format:** [Markdown guidance and structured updates to knowledge/personal/goals.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain persistent personal-goal state in the agent workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
