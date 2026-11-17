## Description:

Monitors Israeli Home Front Command alerts for configured areas and routes matching alerts through OpenClaw WhatsApp messaging, optional 3CX calls, and optional Home Assistant TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaike1](https://clawhub.ai/user/shaike1)

### License/Terms of Use:


## Use Case:

External users and developers can configure this skill to monitor Israeli Home Front Command alerts for selected areas and send timely notifications through messaging, phone, and speaker channels.

### Deployment Geography for Use:

Israel

## Known Risks and Mitigations:

Risk: The installer requests persistent system access and may collect service credentials.

Mitigation: Test in an isolated environment first, set all destinations explicitly, avoid broad Home Assistant tokens, and inspect or remove any crontab entry after testing.

Risk: The artifact claims OpenClaw-only behavior while the README and scripts reference Docker, 3CX, and optional Home Assistant integrations.

Mitigation: Review the selected integrations before installation, disable destinations that are not needed, and verify the Docker image and persistence behavior before running with elevated privileges.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [Red Alert (Israel) ClawHub release](https://clawhub.ai/shaike1/skills/openclaw-skill-red-alert)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with shell commands and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure alert areas, message destinations, optional call or TTS targets, and scheduled monitor behavior.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
