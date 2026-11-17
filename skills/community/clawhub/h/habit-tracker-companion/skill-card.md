## Description:

习惯养成打卡助手，连续激励、数据统计、陪你养成好习惯。

This skill is ready for commercial/non-commercial use.

## Publisher:

[786793119](https://clawhub.ai/user/786793119)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage personal habit tracking: add habits, record daily check-ins, review streaks and completion statistics, and receive milestone encouragement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit names and check-in history are stored locally at ~/.memory/habits/habits.json.

Mitigation: Avoid entering sensitive personal details as habit text and review local retention expectations before use.

Risk: The artifact references a Python script that was not included in the inspected release artifact.

Mitigation: Verify the installed package contains the expected script before running the example commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/786793119/skills/habit-tracker-companion)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to local habit data stored at ~/.memory/habits/habits.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
