## Description: <br>
Control Nest smart home devices (thermostat, cameras, doorbell) via the Device Access API. Use when asked to check or adjust home temperature, view camera feeds, check who's at the door, monitor rooms, or set up temperature schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amogower](https://clawhub.ai/user/amogower) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart home operators use this skill to configure Google Device Access credentials, inspect Nest devices, control thermostat settings, generate camera stream URLs, and optionally run event alerts for doorbell or person detections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amogower/nest-devices) <br>
- [Publisher profile](https://clawhub.ai/user/amogower) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Google Nest Device Access Console](https://console.nest.google.com/device-access) <br>
- [Cloudflared release download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with shell commands, Python examples, JSON responses, and systemd or YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run API calls against Google Device Access, expose a webhook for Pub/Sub events, and send Nest event images or alerts to Telegram and Clawdbot when configured.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
