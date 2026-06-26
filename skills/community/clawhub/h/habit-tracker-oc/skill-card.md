## Description: <br>
习惯养成追踪和进度统计工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to ask an agent for help adding habits, recording daily check-ins, reviewing streaks and completion rates, and configuring reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit and check-in records may contain personal routine data. <br>
Mitigation: Store habits.json and checkins.json only in trusted workspaces and review their contents before sharing logs or artifacts. <br>
Risk: Habit schedules, reminder settings, and completion status can be recorded incorrectly if user intent is ambiguous. <br>
Mitigation: Confirm the habit, date, frequency, and completion status with the user before updating records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/habit-tracker-oc) <br>
- [Publisher profile](https://clawhub.ai/user/huangjingzhi07) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, files] <br>
**Output Format:** [Markdown or plain text responses, with JSON files for stored habits and check-ins when local storage is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses habits.json and checkins.json for habit and check-in records when local storage is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
