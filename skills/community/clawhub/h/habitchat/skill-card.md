## Description: <br>
HabitChat is a personal habit coach that tracks daily habits and streaks, logs recurring routines, and provides coaching insights and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dinesh18S](https://clawhub.ai/user/Dinesh18S) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to track recurring daily habits, log completions or skips, review streaks and progress, and receive brief habit coaching based on their stored activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder setup can create executable shell scripts from unsanitized habit names. <br>
Mitigation: Avoid enabling reminders until habit names are safely escaped by the publisher, and inspect generated reminder scripts before adding them to cron. <br>
Risk: Habit names containing shell metacharacters can increase command-execution risk in reminder scripts. <br>
Mitigation: Do not use habit names containing quotes, backticks, dollar signs, semicolons, pipes, or command substitutions. <br>


## Reference(s): <br>
- [Habit Science Reference](references/habit_science.md) <br>
- [HabitChat Project Homepage](https://github.com/Dinesh18S/dailyping) <br>
- [HabitChat ClawHub Page](https://clawhub.ai/Dinesh18S/habitchat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts and stores habit data under ~/.habitchat/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
