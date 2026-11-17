## Description:

习惯养成追踪和进度统计工具.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07)

### License/Terms of Use:


## Use Case:

External users use this skill to define habits, record daily check-ins, review streaks and completion rates, and configure reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit names and check-in history may be written to local JSON files.

Mitigation: Avoid storing sensitive habit details when privacy matters, and review local files before sharing or deploying the skill.

Risk: Casual wording may be interpreted as a request to create a habit, change a reminder, or record a check-in.

Mitigation: Ask for confirmation before changing habit data when the user's intent is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/skills/habit-tracker-oc)
- [ClawHub publisher profile](https://clawhub.ai/user/huangjingzhi07)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text habit updates, reminder settings, and progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local habits.json and checkins.json records when the agent applies habit tracking actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
