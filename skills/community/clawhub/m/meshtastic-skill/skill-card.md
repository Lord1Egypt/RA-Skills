## Description: <br>
Send and receive messages via Meshtastic LoRa mesh networks for off-grid messaging, mesh network status, recent message review, and LoRa radio texting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukevr](https://clawhub.ai/user/lukevr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and field teams use this skill to connect AI agents to Meshtastic-compatible LoRa hardware for sending messages, monitoring mesh traffic, checking node status, and producing alerts or digests when internet access is unavailable or optional. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map publishing or MQTT bridging can expose mesh traffic or approximate location data beyond the local radio network. <br>
Mitigation: Keep map publishing disabled unless intentionally needed, use fuzzy positioning, avoid precise location in messages, and review MQTT broker settings before operation. <br>
Risk: Local mesh message logs and node caches are written under /tmp and may expose message content or position-derived metadata to local users. <br>
Mitigation: Protect or relocate message logs and node cache files, apply restrictive file permissions, and avoid storing sensitive messages in shared temporary paths. <br>
Risk: Device control features can send messages, broadcast position, forward digests externally, or reboot the connected Meshtastic device. <br>
Mitigation: Require explicit operator confirmation for sends, position broadcasts, external alert delivery, and device reboot actions. <br>
Risk: Broad serial-device permissions can make the Meshtastic device writable by unintended local users. <br>
Mitigation: Avoid broad chmod settings such as 666 and use a restricted device group or udev rule for least-privilege access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lukevr/meshtastic-skill) <br>
- [Meshtastic Documentation](https://meshtastic.org/docs/) <br>
- [Meshtastic MQTT Integration](https://meshtastic.org/docs/configuration/module/mqtt/) <br>
- [Meshtastic Hardware Options](https://meshtastic.org/docs/hardware/) <br>
- [Setup Guide](references/SETUP.md) <br>
- [Claude Desktop MCP Example](references/claude_desktop_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON socket commands, Python scripts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command guidance and bridge/MCP interaction patterns for Meshtastic hardware, MQTT traffic, logs, alerts, and digests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
