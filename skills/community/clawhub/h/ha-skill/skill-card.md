## Description: <br>
Controls Home Assistant climate, light, switch, and sensor entities through the Home Assistant REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query and control Home Assistant devices such as thermostats, lights, switches, and sensors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad, persistent control over real Home Assistant devices through a long-lived local token. <br>
Mitigation: Install only when that control is intended, protect the token file with restrictive permissions, and revoke the token if it may have been exposed. <br>
Risk: Device-control actions can affect the physical environment, including thermostats, lights, and switches. <br>
Mitigation: Review the target entity and requested service before execution, and use the least-privileged Home Assistant account or token available. <br>
Risk: Unencrypted Home Assistant URLs can expose token-bearing requests on the network. <br>
Mitigation: Prefer HTTPS for Home Assistant access, especially when the instance is reachable beyond a trusted local network. <br>


## Reference(s): <br>
- [HA Skill on ClawHub](https://clawhub.ai/ricanwarfare/ha-skill) <br>
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/) <br>
- [Home Assistant Climate Integration](https://www.home-assistant.io/integrations/climate/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, json, guidance] <br>
**Output Format:** [Terminal text and optional JSON responses from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus a local Home Assistant URL and long-lived access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
