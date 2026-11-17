## Description:

Controls the PomoClaw macOS menu bar pomodoro timer through URL-scheme commands for starting, stopping, pausing, configuring, and checking timers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vkozlovskyi](https://clawhub.ai/user/vkozlovskyi)

### License/Terms of Use:


## Use Case:

External users and automation developers use this skill to control a local PomoClaw timer on macOS from an agent, including timer commands, configuration, status checks, and pomodoro completion events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to run macOS shell commands that open PomoClaw URL-scheme commands.

Mitigation: Use only documented PomoClaw URL commands, quote command inputs, and reject malformed or unexpected text instead of placing it into a shell command.

Risk: Timer configuration values and sound names could be invalid or outside the supported ranges.

Mitigation: Limit timer durations to documented numeric ranges and restrict sounds to the documented allowed names before issuing configuration commands.

Risk: The skill depends on local macOS app state and a status file under the user's home directory.

Mitigation: Confirm PomoClaw is running before control commands and read status only from the expected ~/.pomoclaw/status.json path.

## Reference(s):

- [PomoClaw ClawHub skill page](https://clawhub.ai/vkozlovskyi/skills/pomoclaw)
- [PomoClaw GitHub repository](https://github.com/vkozlovskyi/PomoClaw)
- [PomoClaw latest release](https://github.com/vkozlovskyi/PomoClaw/releases/latest)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and URL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the PomoClaw URL scheme and may read JSON timer status from ~/.pomoclaw/status.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
