## Description:

Control Nest thermostat, doorbell, and cameras via the Google Smart Device Management (SDM) API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tag-assistant](https://clawhub.ai/user/tag-assistant)

### License/Terms of Use:


## Use Case:

Developers and technically capable Nest device owners use this skill to configure OAuth access, inspect device state, control thermostats and fans, generate camera streams or event images, and monitor real-time Nest events through Pub/Sub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Nest thermostats and fans, access camera streams or event images, and read household device state.

Mitigation: Install it only for accounts and homes where this level of device access is intended, and review commands before execution.

Risk: OAuth refresh tokens and Pub/Sub credentials are stored locally and used to access Google SDM and cloud resources.

Mitigation: Store token files with restrictive permissions, avoid broad cloud-platform credentials where possible, and rotate or revoke credentials when access is no longer needed.

Risk: Event logs and optional Telegram alerts can expose household activity patterns.

Mitigation: Restrict log access, configure retention deliberately, and enable Telegram forwarding only when sending these alerts to Telegram is acceptable.

Risk: The security scan flags unsafe python3 -c interpolation patterns in scripts that process local configuration and API data.

Mitigation: Review and fix those scripting patterns before running the skill with real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tag-assistant/skills/nest-sdm)
- [Publisher profile](https://clawhub.ai/user/tag-assistant)
- [Google Nest Device Access Console](https://console.nest.google.com/device-access)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token)
- [Google Smart Device Management API endpoint](https://smartdevicemanagement.googleapis.com/v1/enterprises/${PROJECT_ID})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; may create local OAuth token files and Nest event logs when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
