## Description:

个人RPG系统将日常任务转化为 RPG 任务，帮助用户通过完成任务获得经验值、提升等级并解锁能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yansocool](https://clawhub.ai/user/yansocool)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a Chinese-language personal task tracker that frames daily work as RPG-style quests with XP, levels, attributes, achievements, and progress summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal task and progress data locally under the OpenClaw workspace.

Mitigation: Install only when local storage of this data is acceptable, and avoid recording sensitive personal information.

Risk: Complete and delete commands change task state and may remove tasks from the active task list.

Mitigation: Review task IDs before running data-changing commands and keep backups of local JSON state when recovery matters.

## Reference(s):

- [Project homepage](https://github.com/openclaw/personal-rpg)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [CLI text output with local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists character, task, achievement, statistics, and configuration data under the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
