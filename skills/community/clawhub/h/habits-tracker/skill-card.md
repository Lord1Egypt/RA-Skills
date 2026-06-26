## Description: <br>
Habits Tracker helps agents provide local Node.js CLI commands and guidance for tracking habits, routines, streaks, completions, reminders, and weekly progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and manage a local habit-tracking workflow, log completions, review streaks and weekly progress, recover from missed days, and configure local reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit names, notes, dates, and medication or health routines may contain sensitive personal data stored locally under ~/.config/habit-tracker. <br>
Mitigation: Avoid recording sensitive details unless needed, restrict local file access, and review notes before sharing reports or logs. <br>
Risk: Cron reminders or event integrations can create scheduled local checks that may run when not expected. <br>
Mitigation: Add cron or event integrations only intentionally and review the schedule and script path before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/habits-tracker) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privacy notes for sensitive personal or health-related habit notes.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and target metadata; artifact files contain older version metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
