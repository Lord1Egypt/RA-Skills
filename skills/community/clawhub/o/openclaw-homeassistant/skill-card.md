## Description: <br>
Control smart home devices via Home Assistant: lights, climate, media, covers, scenes, sensors, automations, and more. 34 tools with readOnly and domain-level safety guards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homeofe](https://clawhub.ai/user/homeofe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent read Home Assistant state and control smart-home devices, scenes, scripts, automations, notifications, and history. It is suited for connected-home automation where the operator can restrict write access and allowed device domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad smart-home control primitives, including device writes, service calls, events, templates, notifications, scripts, scenes, and automations. <br>
Mitigation: Install only for trusted agents, prefer readOnly mode unless writes are required, and restrict allowedDomains to the smallest practical Home Assistant domains. <br>
Risk: A broad Home Assistant token could allow unintended changes if an agent is misused or compromised. <br>
Mitigation: Use a dedicated low-privilege Home Assistant account, protect the token, and revoke or rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/homeofe/openclaw-homeassistant) <br>
- [Home Assistant documentation](https://www.home-assistant.io/) <br>
- [README](artifact/README.md) <br>
- [Security policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance] <br>
**Output Format:** [JSON tool responses and Home Assistant service calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Home Assistant URL and long-lived access token; readOnly and allowedDomains can limit write operations and device domains.] <br>

## Skill Version(s): <br>
0.2.1 (source: package.json, openclaw.plugin.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
