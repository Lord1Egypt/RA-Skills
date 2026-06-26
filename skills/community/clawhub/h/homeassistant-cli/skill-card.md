## Description: <br>
Advanced Home Assistant control using the official hass-cli tool, with auto-completion, event monitoring, history queries, and rich output formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonesChi](https://clawhub.ai/user/JonesChi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use this skill to operate and inspect Home Assistant devices through hass-cli, especially for interactive device discovery, service calls, event monitoring, and history queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a long-lived Home Assistant token that can expose smart-home control if copied into logs, screenshots, shell history, or version-controlled files. <br>
Mitigation: Use a restricted Home Assistant account when possible and keep HASS_TOKEN out of shared output, command history, screenshots, and checked-in configuration. <br>
Risk: hass-cli service calls can affect real devices, including alarms, locks, covers, climate systems, appliances, and security-related automations. <br>
Mitigation: Require explicit confirmation before running commands that affect safety, access, climate, appliances, or security-sensitive automations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JonesChi/homeassistant-cli) <br>
- [Home Assistant CLI project](https://github.com/home-assistant-ecosystem/home-assistant-cli) <br>
- [PyPI package: homeassistant-cli](https://pypi.org/project/homeassistant-cli/) <br>
- [Homebrew formula: homeassistant-cli](https://formulae.brew.sh/formula/homeassistant-cli) <br>
- [Examples](references/examples.md) <br>
- [Auto-completion setup](references/autocomplete.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hass-cli commands, environment variable setup, and output-format guidance for table, YAML, or JSON CLI output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
