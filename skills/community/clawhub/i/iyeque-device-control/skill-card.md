## Description: <br>
Expose safe device actions (volume, brightness, open/close apps) for personal automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyeque](https://clawhub.ai/user/iyeque) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to let an agent adjust local volume or brightness and open or close local applications across Linux, macOS, Windows, and WSL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch local programs and force-close matching processes on the user's computer. <br>
Mitigation: Install and run it only where local device-control authority is acceptable, and review app-opening and app-closing requests before execution to avoid interrupting work or losing unsaved data. <br>
Risk: The security verdict is suspicious because the skill exposes local device-control actions. <br>
Mitigation: Use the skill in trusted personal automation contexts and keep requests scoped to expected volume, brightness, and application-control actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iyeque/iyeque-device-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Command-line actions and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and platform-specific utilities for some actions, including pactl or amixer on Linux, brightnessctl or brightness CLI for brightness control, and nircmd.exe for Windows or WSL volume control.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
