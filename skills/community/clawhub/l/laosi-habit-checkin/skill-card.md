## Description:

习惯追踪 - 每天打卡，自动计算连续天数/历史最佳/总打卡数，多习惯管理，本地JSON持久化

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity agents use this skill to record daily habit check-ins, view streak, best, and total statistics, and manage multiple habits with local JSON persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit names and check-in dates are stored locally in a JSON file.

Mitigation: Use non-sensitive habit names and keep the JSON file in a user-controlled location with appropriate local file permissions.

Risk: Broad trigger words may invoke habit tracking when the user did not specifically intend to update a check-in.

Mitigation: Confirm the target habit and action before creating or updating a check-in record.

Risk: The skill content is primarily Chinese-language.

Mitigation: Review or localize prompts and output labels before using it with non-Chinese users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-habit-checkin)
- [ClawHub publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with Python, bash, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code may create or update a local habit_streaks.json file when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
