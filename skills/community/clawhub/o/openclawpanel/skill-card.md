## Description: <br>
Control an OpenClaw LED panel (64x32 HUB75 on ESP32-S3) over HTTP - display text, graphics, shapes, play sounds, and read status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaquinckronoset](https://clawhub.ai/user/joaquinckronoset) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send HTTP commands to a controlled local LED panel for short text, graphics, dashboard panels, sound playback, and device status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can change what appears on the configured panel and play sounds. <br>
Mitigation: Install only when you control the panel and local network, and verify OPENCLAW_PANEL_IP before use. <br>
Risk: Panel display control can briefly interrupt the normal timeline or leave temporary content visible. <br>
Mitigation: Use the documented lock and unlock workflow, and unlock or reset the panel after temporary displays. <br>
Risk: Brightness and volume changes can persist across reboots. <br>
Mitigation: Keep brightness and volume within the documented 0-100 range and restore preferred values after tests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joaquinckronoset/openclawpanel) <br>
- [OpenClaw Panel Project](https://github.com/joaquinckronoset/openclawpanel) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and OPENCLAW_PANEL_IP for a panel on the same local network.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
