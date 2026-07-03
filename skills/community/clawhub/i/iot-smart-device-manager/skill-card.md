## Description: <br>
IoT智能设备管理 helps manage smart-home and industrial IoT devices by producing monitoring, protocol-adaptation, troubleshooting, automation, and energy-optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation engineers use this skill to plan IoT device onboarding, protocol configuration, automation rules, fault diagnosis, and energy analysis for smart-home and industrial IoT environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests shell execution for IoT diagnostics without clear boundaries for when commands may run. <br>
Mitigation: Require explicit user confirmation before running commands, especially commands involving local networks, device control, credentials, or configuration changes. <br>
Risk: IoT troubleshooting and automation guidance can affect real devices, network behavior, credentials, or operational settings. <br>
Mitigation: Review proposed diagnostics and configuration changes before applying them, and prefer read-only checks until the target device, protocol, and expected impact are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/iot-smart-device-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown with configuration examples, decision trees, reports, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device topology, MQTT topic trees, YAML automation configuration, troubleshooting decision trees, and energy reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
