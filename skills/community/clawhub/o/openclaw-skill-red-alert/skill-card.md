## Description: <br>
Monitors Israeli Home Front Command alerts for selected areas and routes notifications through OpenClaw WhatsApp messaging, optional 3CX calls, and Home Assistant TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaike1](https://clawhub.ai/user/shaike1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators in Israel can configure monitored areas and notification destinations for emergency alert routing. The skill is intended to help an agent install and operate a persistent alert monitor that sends messages, voice announcements, and optional phone-call notifications. <br>

### Deployment Geography for Use: <br>
Israel <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a suspicious security verdict because the main skill description under-discloses Docker, Home Assistant, 3CX calling, credential storage, and background persistence. <br>
Mitigation: Review the installer and monitor before execution, confirm each destination explicitly, inspect the reboot crontab entry, and run only on a trusted host. <br>
Risk: Default or stale notification settings could route emergency messages, phone calls, or speaker announcements to unintended recipients or areas. <br>
Mitigation: Replace hard-coded defaults, verify monitored areas and recipient identifiers in `.env`, and test notification routes with non-emergency messages before relying on the monitor. <br>
Risk: Home Assistant tokens and notification endpoints may be stored in local configuration for a persistent process. <br>
Mitigation: Restrict `.env` file permissions, provide a Home Assistant token only when speaker announcements are needed, and rotate credentials if the host or file permissions are uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaike1/openclaw-skill-red-alert) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational setup and monitoring guidance for alert routing; does not produce a trained model or dataset.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
