## Description: <br>
Guides an agent to provide terminal commands for Pomodoro focus sessions, optional macOS notifications, and session logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbelJSeba](https://clawhub.ai/user/AbelJSeba) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and productivity-focused users use this skill to run Pomodoro-style focus timers, customize session duration, and review local session logs from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional logging command creates or updates ~/pomodoro.log with Pomodoro session timestamps. <br>
Mitigation: Review the log path before running the command and adjust, delete, or rotate the log according to local privacy and retention needs. <br>
Risk: The notification command uses macOS osascript and may not work on other operating systems. <br>
Mitigation: Use a platform-appropriate notification command or rely on terminal output when running outside macOS. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbelJSeba/makeovern) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local terminal commands that wait for timer duration, show macOS notifications, and optionally append timestamps to ~/pomodoro.log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
