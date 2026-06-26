## Description: <br>
Control the PomoClaw pomodoro timer on macOS by starting, pausing, stopping, configuring, and checking timer status through documented URL-scheme commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vkozlovskyi](https://clawhub.ai/user/vkozlovskyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent control a local PomoClaw menu bar timer on Mac for focus sessions, breaks, status checks, and timer configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to open local pomoclaw:// URLs that control a Mac timer app. <br>
Mitigation: Install it only when agent control of PomoClaw is desired, and keep use scoped to the documented timer, status, break, and configuration commands. <br>
Risk: The linked Mac app is a separate dependency that must be trusted by the user. <br>
Mitigation: Verify the linked PomoClaw app or release before installing or using the skill. <br>
Risk: The configuration command can enable launch at login. <br>
Mitigation: Enable launch at login only when the user explicitly wants the timer app to start automatically. <br>


## Reference(s): <br>
- [PomoClaw ClawHub page](https://clawhub.ai/vkozlovskyi/pomoclaw) <br>
- [Publisher profile](https://clawhub.ai/user/vkozlovskyi) <br>
- [PomoClaw GitHub repository](https://github.com/vkozlovskyi/PomoClaw) <br>
- [PomoClaw latest release](https://github.com/vkozlovskyi/PomoClaw/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and URL-scheme examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to read a local JSON status file written by the PomoClaw app.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
