## Description:

Kami SmartHome skill bundle. One-click installer for the entire Kami SmartHome ecosystem with centralized configuration for API keys, cameras, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13681882136](https://clawhub.ai/user/13681882136)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to install and centrally configure the Kami SmartHome ecosystem for RTSP camera monitoring, notifications, visual search, and event detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow downloads additional skills and dependencies and may request broad install authority.

Mitigation: Review setup.sh and configure.py before installation, run the installer in a controlled environment, and grant elevated permissions only after confirming the requested package actions.

Risk: Camera URLs, API keys, and notification credentials may be stored in local plaintext configuration or exposed through command-line history and terminal output.

Mitigation: Avoid passing secrets on the command line, restrict file permissions on local configuration files, treat setup output as sensitive, and rotate any secret that may have been exposed.

Risk: RTSP camera streams and notification snapshots can contain sensitive home or workplace imagery.

Mitigation: Configure only trusted cameras and notification channels, limit access to generated outputs, and confirm that camera use complies with the deployment environment's privacy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13681882136/skills/kami-smarthome-suite)
- [KamiClaw API portal](https://kamiclaw-skill.kamihome.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local Kami configuration and distribute it to installed sub-skills.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
