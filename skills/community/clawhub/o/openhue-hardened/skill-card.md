## Description: <br>
Control Philips Hue lights/scenes via the OpenHue CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and home automation users use this skill to generate safe OpenHue CLI commands for reading Hue Bridge state and controlling Philips Hue lights, scenes, rooms, brightness, and color. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenHue discovery and setup can scan the local network or modify Hue Bridge pairing state. <br>
Mitigation: Only propose or run `openhue discover` or `openhue setup` when the user explicitly requests discovery or setup. <br>
Risk: Bridge IP addresses, API keys, serial numbers, device IDs, and room layouts can expose sensitive home infrastructure. <br>
Mitigation: Do not include those details in responses, and keep OpenHue command output local. <br>
Risk: Piping OpenHue output to network tools or remote endpoints can exfiltrate sensitive Hue device data. <br>
Mitigation: Do not transmit OpenHue output with commands such as `scp`, `curl`, or other network-facing tools. <br>
Risk: The skill depends on the OpenHue Homebrew package and a local Hue Bridge environment. <br>
Mitigation: Install only when the OpenHue package is trusted and the user intends agent-assisted local Hue device control. <br>


## Reference(s): <br>
- [OpenHue CLI documentation](https://www.openhue.io/cli) <br>
- [Openhue Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/openhue-hardened) <br>
- [Faberlens openhue safety evidence](https://faberlens.ai/explore/openhue) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OpenHue output and Hue infrastructure details should remain local and should not be transmitted to network endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
