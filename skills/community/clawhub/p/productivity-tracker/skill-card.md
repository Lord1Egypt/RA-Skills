## Description:

Productivity Tracker is a lightweight local task management and time tracking skill for task lists, pomodoro sessions, daily statistics, and habit check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers, students, and freelancers use this skill to manage local tasks, track focus sessions, record habit check-ins, and review daily productivity statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores task, habit, and statistics data locally under ~/.task-tracker.

Mitigation: Install only when local storage of productivity data is acceptable, and review local data handling expectations before use.

Risk: The delete command removes local task entries immediately without a confirmation prompt.

Mitigation: Review task IDs before deletion and back up ~/.task-tracker when entries need to be retained.

Risk: Pomodoro timing depends on the terminal process continuing to run.

Mitigation: Keep the terminal session open during focus timers or use the feature only for lightweight local tracking.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local task, habit, and statistics data are stored under ~/.task-tracker.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
