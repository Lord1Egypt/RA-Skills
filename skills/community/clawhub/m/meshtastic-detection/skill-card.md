## Description: <br>
Receive DETECTION_SENSOR_APP alerts from Meshtastic LoRa devices via USB. When the remote sensor GPIO triggers (preset target detected), store the event and alert the user immediately. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autume](https://clawhub.ai/user/autume) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor Meshtastic LoRa detection-sensor events from a USB-connected device, store local event records, and trigger near-real-time Feishu alerts through OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may make privileged host changes and can fall back to downloading pip bootstrap code during installation. <br>
Mitigation: Review setup.sh before running it, use a controlled Python environment when possible, and avoid the automatic sudo or get-pip fallback unless those host and supply-chain changes are acceptable. <br>
Risk: Alert delivery can send sender IDs and detection text to Feishu. <br>
Mitigation: Replace every Feishu open_id with a verified recipient and decide whether the alert contents are appropriate for a third-party chat system before enabling cron delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autume/meshtastic-detection) <br>
- [Setup Guide](references/SETUP.md) <br>
- [Configuration Reference](CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON alert outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, a USB-connected Meshtastic-compatible device, local JSONL storage, and OpenClaw cron configuration for Feishu alerts.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
