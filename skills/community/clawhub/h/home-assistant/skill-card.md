## Description: <br>
Control Home Assistant smart home devices, run automations, and receive webhook events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iAhmadZain](https://clawhub.ai/user/iAhmadZain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to control Home Assistant entities, scenes, scripts, automations, and webhooks through REST API calls and a shell wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over Home Assistant devices and automations. <br>
Mitigation: Use a dedicated least-privilege Home Assistant account or token where possible and review actions before allowing sensitive domains. <br>
Risk: Stored Home Assistant credentials could expose smart-home control if the config file is readable by other users. <br>
Mitigation: Restrict the Home Assistant config file to owner-only permissions and avoid sharing long-lived access tokens. <br>
Risk: Generic service calls can affect sensitive devices such as locks, covers, alarms, climate controls, scripts, automations, and webhooks. <br>
Mitigation: Require explicit confirmation for sensitive domains and avoid using the generic service caller for high-impact actions. <br>


## Reference(s): <br>
- [Home Assistant REST API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON/YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus a Home Assistant URL and long-lived access token supplied by environment variables or a local config file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
