## Description: <br>
Productivity Tracker is a local task, Pomodoro, time-tracking, daily statistics, and habit-checking skill for managing personal productivity from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers, students, and freelancers can use this skill to create and complete local tasks, run Pomodoro focus sessions, track habits, and review daily productivity statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores task names, habit names, timestamps, and completion history locally under ~/.task-tracker/. <br>
Mitigation: Avoid entering sensitive personal or work details unless the local machine and backups are trusted. <br>
Risk: State-changing commands can complete tasks, delete tasks, or check habits. <br>
Mitigation: Use explicit commands for actions that modify local task or habit data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SxLiuYu/productivity-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output and local JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task, habit, and statistics data locally under ~/.task-tracker/.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
