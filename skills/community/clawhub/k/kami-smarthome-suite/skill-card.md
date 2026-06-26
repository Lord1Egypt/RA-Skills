## Description: <br>
Kami SmartHome skill bundle. One-click installer for the entire Kami SmartHome ecosystem with centralized configuration for API keys, cameras, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home operators use this skill to install and configure the Kami SmartHome suite, including RTSP camera setup, KamiClaw API configuration, notification channels, and distribution of centralized settings to the bundled skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles privacy-sensitive camera, API, and notification credentials. <br>
Mitigation: Run setup only in intended smart-home environments, avoid sharing credential-bearing RTSP URLs or command output, and review configuration files before distributing them to sub-skills. <br>
Risk: The installer can execute the user's shell startup file and install additional skills and dependencies. <br>
Mitigation: Review setup actions before execution and run setup only when you explicitly intend to install the full Kami SmartHome suite. <br>


## Reference(s): <br>
- [Kami Smarthome Suite on ClawHub](https://clawhub.ai/13681882136/kami-smarthome-suite) <br>
- [KamiClaw API registration](https://kamiclaw-skill.kamihome.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose installing six related ClawHub skills and writing centralized camera, API key, and notification settings.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
