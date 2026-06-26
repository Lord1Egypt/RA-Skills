## Description: <br>
Build daily habits with streak tracking, reminders, and progress charts. Use when starting habits, maintaining streaks, or analyzing completion rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to install and operate a local command-line utility for recording habit-related activity, reviewing recent entries, checking simple stats, and exporting local data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a habit tracker, while the security evidence describes the script as a generic local data logger. <br>
Mitigation: Review the command behavior before installation and use it only when generic local logging matches the intended workflow. <br>
Risk: Habit, routine, or personal details entered into the CLI may be stored in plain text under ~/.local/share/habit and exposed through search, recent, stats, or export commands. <br>
Mitigation: Avoid entering sensitive health or personal details, and inspect or remove local log and export files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/habit) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output as plain text; exports as JSON, CSV, or TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local logs and exports under ~/.local/share/habit.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
