## Description: <br>
Wake-on-LAN functionality for macOS - wake devices remotely by MAC address or name <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, IT operators, and local-network users use this skill to wake, list, add, remove, and check Wake-on-LAN devices from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Wake-on-LAN packets and ping traffic on the local network, which may wake or probe unintended devices if names, MAC addresses, or broadcast addresses are wrong. <br>
Mitigation: Review the target device details and broadcast address before use, and run bulk wake commands only on device lists you trust. <br>
Risk: Saved device configuration can contain device names, MAC addresses, broadcast addresses, and optional IP addresses. <br>
Mitigation: Review or delete ~/.config/openclaw/wol-devices.json when saved devices are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Wake-on-LAN and ping commands and maintain device configuration at ~/.config/openclaw/wol-devices.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
